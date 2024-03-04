# Github Access Token currently not working right now
import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv('GITHUB_API_TOKEN')


class GithubFileLoader:

    github_api_url = "https://api.github.com"
    rate_limit_url = "https://api.github.com/rate_limit"

    excluded_dirs = {'node_modules', ".git", ".vscode", "__pycache__"}  # Directories to exclude loading
    excluded_files = {'poetry.lock', 'yarn.lock', 'package-lock.json'}  # Files to exclude loading

    @property
    def headers(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        }

    def __init__(self, repo_url):
        self.repo_url = repo_url.split("https://github.com/")[-1]

    def get_file_paths(self, branch = "main"):

        try:
            base_url = (
                f"{self.github_api_url}/repos/{self.repo_url}/git/trees/"
                f"{branch}?recursive=1"
            )

            response = requests.get(base_url, headers=self.headers)
            response.raise_for_status()
            all_files = response.json()["tree"]
        
            return [
                f
                for f in all_files
                if f['type'] == "blob"
            ]
        except requests.exceptions.HTTPError as http_err:
            # Check if the error is because the branch doesn't exist or some other HTTP error
            if branch == "main":
                print(f"Main branch not found or error occurred: {http_err}. Trying 'master' branch.")
                return self.get_file_paths(branch="master")
            else:
                # If the branch is not 'main', or retrying with 'master' also failed, raise the error.
                raise http_err
          
            
            
   


    def get_file_content_by_path(self, path: str) -> str:
        try:
            base_url = f"{self.github_api_url}/repos/{self.repo_url}/contents/{path}"
            response = requests.get(base_url, headers=self.headers)
            response.raise_for_status()  # This will raise an exception for 4XX and 5XX responses
            content_encoded = response.json()["content"]
            return base64.b64decode(content_encoded).decode("utf-8")
        except Exception as e:
            return "file not readable"

    def is_file_in_excluded_files(self, file):
        # Split the file path to check each part against excluded directories and files
        path_parts = file["path"].split('/')

        # Check if any part of the path is in the excluded directories or if the file name is in the excluded files
        return any(part in self.excluded_dirs for part in path_parts) or path_parts[-1] in self.excluded_files

    def load(self):
        documents = []

        files = self.get_file_paths()
        for file in files:
         
            ## If node_modules (folder), package-lock.json, yarn.lock, etc, then don't process
            if self.is_file_in_excluded_files(file):
                continue

            content = self.get_file_content_by_path(file["path"])
            documents.append({"file_path": file["path"], "contents": content})


        return documents

    def load_stream(self):
        files = self.get_file_paths()
        for file in files:
         
            ## If node_modules (folder), package-lock.json, yarn.lock, etc, then don't process
            if self.is_file_in_excluded_files(file):
                continue

            content = self.get_file_content_by_path(file["path"])
            yield {"file_path": file["path"], "contents": content}
