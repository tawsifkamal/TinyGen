from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from api.github_file_loader import GithubFileLoader
from api.utils import get_file
from api.db import insert_to_supabase

from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv('OPENAI_API_KEY')

class TinyGenOne:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4-0125-preview", max_tokens=4096, temperature=0, streaming=True, openai_api_key=ACCESS_TOKEN)
   

    def call(self, repoUrl, prompt):

        # Load files
        loader = GithubFileLoader(repo_url=repoUrl)
        self.repo_files = loader.load()
        self.prompt = prompt

        # Initialize the chains (three chains = code conversion -> generate diff -> reflection on diff)
        tiny_gen_chain = self.initialize_and_combine_chains(self.repo_files, self.prompt)

        response = tiny_gen_chain.invoke({"repository": self.repo_files, "user_query": self.prompt})

        # Insert Data to supabase
        insert_to_supabase(prompt, repoUrl, response, "tiny_gen_one_calls")

        return response

    def transform_chain_output(self, code_changes):
        
        file_path = code_changes["file_path"]
        original_file = get_file(file_path, self.repo_files)
        return {"original_file": {"file_path": file_path, "contents": original_file}, "changed_file": code_changes}

    def initialize_and_combine_chains(self, repoUrl, prompt):
        ############ 
        # 1. Code Conversion Chain: Given all of the files, generate the code that would fix the user's issue in the file
        ############
        code_conversion_prompt = PromptTemplate.from_template(
            """
            You are an expert at solving user issues in the code base. Given a user query defined under <user_query><user_query/>,
            you can identify the files that you need to update to solve the problem/issue that the user is having. 
            These files are given as context to you in between <repository></repository>.

            <repository>
            {repository}
            </repository>

            Given these files, do the following step by step:
            1. Identify what files need to be changed to solve user's query
            2. Identify what changes need to be made in the files
            3. update the code so that the user's issue is solved
            
            <user_query>
            {user_query}
            </user_query>

            Return the name of the file that was updated,
            and also the updated file in a json format like this:

            ```json
            {{
                "file_path": path of the file,
                "updated_contents": new_file_contents,
                "what_changed": simple description of what was added
            }} 
            ```

            return only the json!
            """
        )
        code_conversion_chain = (
            code_conversion_prompt
            | self.llm
            | JsonOutputParser()
        )


        ############ 
        # 2. Generate Diff: Given the changed file and the original file, generate the unified diff
        ############
        generate_diff_prompt = PromptTemplate.from_template(
            """
            You are an expert at generating diffs given two files. You are given the original file path and content.
            You are also given the changed file and possible reason for the changes.

            Generate the unified diff for the changes that were made!

            Return only the diff and nothing else

            <original_file>
            {original_file}
            </original_file>


            <changed_file>
            {changed_file}
            </changed_file>
            """
        )
        generate_diff_chain = (
            generate_diff_prompt
            | self.llm
            | StrOutputParser()
        )


        ############ 
        # 3. Reflection Chain: Given the generated diff, user query, original file and changed file, check to see if the diff is correct. Return the diff if correct, or regenerate it again
        ############
        reflection_prompt = PromptTemplate.from_template(
            """
            You are given a diff please check to make sure that the diff is correct!
            Ensure that it's compilable and also solves the user's query. If its correct,
            then don't change it and return the diff and only the diff.
            If it's incorrect, then generate a new diff based on the changed files.

            Return only the diff! If it was correct, then just return the original diff and nothing else. if it was incorrect,
            then return the new diff and nothing else!
           
            <original_file>
            {original_file}
            </original_file>

            <changed_file>
            {changed_file}
            </changed_file>

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
            | self.llm 
            | StrOutputParser()
        )



        tiny_gen_chain = (
            code_conversion_chain
            | RunnableLambda(self.transform_chain_output)
            | RunnablePassthrough.assign(
                diff=generate_diff_chain,
                user_query=lambda x: prompt
            )
            | reflection_chain
        )

        return tiny_gen_chain

        






