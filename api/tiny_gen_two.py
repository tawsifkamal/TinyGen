from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser


from api.db import insert_to_supabase
from api.utils import get_file
from api.utils import get_file
from api.db import insert_to_supabase
from api.github_file_loader import GithubFileLoader

from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
ACCESS_TOKEN = os.getenv('OPENAI_API_KEY')




class TinyGenTwo:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4-0125-preview", max_tokens=4096, temperature=0, streaming=True, openai_api_key=ACCESS_TOKEN)
        self.llm_gpt_3 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", max_tokens=4096, openai_api_key=ACCESS_TOKEN)

    def call(self, repoUrl, prompt):
        # Load files
        loader = GithubFileLoader(repo_url=repoUrl)
        self.repo_files = loader.load()
        self.prompt = prompt

        # summarize files
        self.repo_files_with_summaries = self.summarize_files(self.repo_files)

        # Initialize the chains (three chains = code conversion -> generate diff -> reflection on diff)
        tiny_gen_chain = self.initialize_and_combine_chains(self.repo_files, self.prompt)

        response = tiny_gen_chain.invoke({"files_list": self.repo_files_with_summaries, "user_query": self.prompt})
        # Insert Data to supabase
        insert_to_supabase(prompt, repoUrl, response, "tiny_gen_two_calls")

        return response
    
    async def stream(self, repoUrl, prompt):

        loader = GithubFileLoader(repo_url=repoUrl)

        yield "Processing files...\n"
        files_generator = loader.load_stream()
        self.repo_files = []
        for file in files_generator:
            self.repo_files.append(file)
            if len(self.repo_files) < 6:
                yield "File Name: " + file['file_path'] + "\n"
            elif len(self.repo_files) == 6:
                yield "Processing the rest... please wait.\n"
        yield "Done processing files!\n\n"
        self.prompt = prompt

        # summarize files
        yield f'Summarizing files...\nMaking a batch call to summarize file chain for {len(self.repo_files)} files...\n'
        self.repo_files_with_summaries = self.summarize_files(self.repo_files)
        yield "Done summarizing all files!\n\n"

    
        # Initialize rest of the chains 
        # Four Chain = identify relevant files -> code conversion -> generate diff -> reflection on diff)
        tiny_gen_chain = self.initialize_and_combine_chains(self.repo_files, self.prompt)


        response = tiny_gen_chain.astream_events(
            {"files_list": self.repo_files_with_summaries, "user_query": self.prompt},
            version="v1",
            include_types=["chat_model"]
        )

        async for event in response:
            kind = event['event']
            chain = event["name"]

            if kind == "on_chat_model_stream":
                yield str(event['data']['chunk'].content)
            elif kind == "on_chat_model_start" and chain == "identify_relevant_files_chain":
                yield str("##### Starting Identify Relevant Files Chain...\n\n")
            elif kind == "on_chat_model_start" and chain == "code_conversion_chain":
                yield str("##### Starting Code Conversion Chain...\n\n")
            elif kind == "on_chat_model_start" and chain == "generate_diff_chain":
                yield str("\n\n##### Starting Generate Diff Chain...\n\n")
            elif kind == "on_chat_model_start" and chain == "reflection_chain":
                yield str("\n\n##### Starting Reflection Chain...\n\n")
        
        # Insert Data to supabase after all streaming is finished!
        insert_to_supabase(prompt, repoUrl, response, "tiny_gen_one_calls")
    
    def summarize_files(self, repo_files):
        ############ 
        # 1. Summary Chain: summarize all files 
        ############
        summarize_prompt = PromptTemplate.from_template(
            """
            Here is the given contents from a file:
            <contents>
            {contents}
            </contnets>

            Here is the given file path for this file:
            <file_path>
            {file_path}
            </file_path>

            Generate me a detailed summary of the purpose of this file in the context.
            Every file must have a clear and very detailed (must be minimum of 4 sentences but can be more) summary. 
            It must be very clear so that even developers who just moved to this project can understand this file by analyzing the generated summary
            without additional questions.
            """
        )
        summary_chain = summarize_prompt | self.llm_gpt_3 | StrOutputParser()

        summarize_files = (
            summary_chain.map()
            | self.transform_summary_chain_output
        )       
        
        return summarize_files.invoke(repo_files)

    def transform_summary_chain_output(self, summaries):
        files_with_summaries = []
        for i, summary in enumerate(summaries):
            file_and_summary = {"file_path": self.repo_files[i]['file_path'], 'file_summary': summary}     
            files_with_summaries.append(file_and_summary)

        return files_with_summaries

    def transform_relevant_files_chain_output(self, relevant_file_paths: dict[str, List]):
        relevant_files = get_file(relevant_file_paths["files"], self.repo_files)
        return relevant_files

    def transform_conversion_chain_output(self, code_changes: dict[str, List]): 
        original_files = []
     
        for code_change in code_changes["code_changes"]:
            original_file_path = code_change["original_file_path"]
            original_file = get_file(original_file_path, self.repo_files)
            original_files.append({"file_path": original_file_path, "contents": original_file})
            
        return {"original_files": original_files, "changed_files": code_changes}

    def initialize_and_combine_chains(self, repoUrl, prompt):
        ############
        # 2. Identify Relevant Files Chain: given a summary of each file, identify relevant files to the user prompt
        ############
        identify_relevant_files_prompt = PromptTemplate.from_template(
            """
            You're a senior software developer implementing changes in files the project.
            Based on the provided instructions, all file paths, and summary of each file, identify the file
            that needs to be modified to solve the user's issue or request.

            <files_list>
            {files_list}
            </files_list>

            <user_query>
            {user_query}
            </user_query>

            There may be just a single file OR there maybe multiple files. You decide which files you think are relevant. If there are multiple files, 
            make sure each path is in a new line. think carefully and output all relevant files!

            Output *ONLY* the file path(s), relative to project root, as a list
            without any comments or explanation, like this:

            ```json
            {{"files": [path/to/file, path/to/file]}}
            ```
            """
        )

        identify_relevant_files_chain = (
            identify_relevant_files_prompt 
            | self.llm.with_config({"run_name": "identify_relevant_files_chain"})  
            | JsonOutputParser()
        )
        ############ 
        # 3. Code Conversion Chain: Given all of the files, generate the code that would fix the user's issue in the file
        ############
        code_conversion_prompt = PromptTemplate.from_template(
            """
            You are an expert at solving user issues in the code base. Given a user query defined under <user_query><user_query/>,
            You are given the relevant files needed to solve the user's issue that he/she is having for the given repository
            These are the relevant files given to you under <relevant_files><relevant_files>

            <relevant_files>
            {relevant_files}
            </relevant_files>

            Given these files, do the following step by step:
                1. Identify what changes need to be made in the files
                2. update the code so that the user's issue is solved
            
            <user_query>
            {user_query}
            </user_query>

            Return the name of the file(s) that was updated,
            and also the updated file in a json format like this:
            {{
                "code_changes": [
                    {{
                        "original_file_path: path of original file
                        "new_file_path": path of the new file,
                        "updated_contents": new_file_contents,
                        "what_changed": simple description of what was added
                    }},
                    {{
                        "original_file_path: path of original file
                        "new_file_path": path of the new file,
                        "updated_contents": new_file_contents,
                        "what_changed": simple description of what was added
                    }}
                ]
            }}
            
           

            Important: Return only the json and no other text! Make sure to escape any string literals so that the json is valid!
            """
        )
        code_conversion_chain = (
            code_conversion_prompt
            | self.llm.with_config({"run_name": "code_conversion_chain"}) 
            | JsonOutputParser()
        )


        ############ 
        # 4. Generate Diff: Given the changed file and the original file, generate the unified diff
        ############
        generate_diff_prompt = PromptTemplate.from_template(
            """
            You are an expert at generating diffs given the original files and the modified files. You are given the original file paths and content.
            You are also given the changed files and possible reason for the changes. There may be just one file that was modified or more than one.

            Generate the unified diff for the changes that were made!

            Return only the diff and nothing else

            <original_files>
            {original_files}
            </original_files>

            <changed_file>
            {changed_files}
            </changed_file>
            """
        )
        generate_diff_chain = (
            generate_diff_prompt
            | self.llm.with_config({"run_name": "generate_diff_chain"}) 
            | StrOutputParser()
        )

        ############ 
        # 5. Reflection Chain: Given the generated diff, user query, original file and changed file, check to see if the diff is correct. Return the diff if correct, or regenerate it again
        ############
        reflection_prompt = PromptTemplate.from_template(
            """
            You are given a diff please check to make sure that the diff is correct!
            Ensure that it's compilable and also solves the user's query. If its correct,
            then don't change it and return the diff and only the diff.
            If it's incorrect, then generate a new diff based on the changed files.

            Return only the diff! If it was correct, then just return the original diff and nothing else. if it was incorrect,
            then return the new diff and nothing else!
            
            <original_files>
            {original_files}
            </original_file>

            <changed_file>
            {changed_files}
            </changed_files>

            <diff>
            {diff}
            </diff>

            <user_query>
            {user_query}
            </user_query>
            """

        )
        reflection_chain = (
            reflection_prompt 
            | self.llm.with_config({"run_name": "reflection_chain"}) 
            | StrOutputParser()
        )

        identify_relevant_files = (
            identify_relevant_files_chain
            | self.transform_relevant_files_chain_output
        )

        convert_code = (
            code_conversion_chain
            | self.transform_conversion_chain_output
        )

        final_chain = (
            RunnablePassthrough.assign(relevant_files=identify_relevant_files)
            .pick(["user_query", "relevant_files"])
            .pipe(convert_code)
            .assign(user_query=lambda x: prompt, diff=generate_diff_chain)
            .pick(["user_query", "diff", "original_files", "changed_files"])
            .pipe(reflection_chain)
        )

        return final_chain

