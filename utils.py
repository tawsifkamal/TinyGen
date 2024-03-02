from typing import Union, List, Dict

def get_file(file_paths: Union[List[str], str], repo_files: List[Dict[str, str]]):
    """
    Get the contents of multiple files given their relative file paths from a list of repository files.
    
    Args:
    - file_paths (Union[List[str], str]): List of relative paths to the files or a single file path as a string.
    - repo_files (List[Dict[str, str]]): List of dictionaries with 'file_path' and 'contents' keys representing files in a repository.
    
    Returns:
    - List[Dict[str, str]]: A list of dictionaries, each containing the file path and its contents.
    """
    
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    file_contents = []

    for file_path in file_paths:
        # Search for the file_path in repo_files
        matched_files = [f for f in repo_files if f['file_path'] == file_path]
        if matched_files:
            # Assuming only one match should be found, take the first one.
            file_contents.append(matched_files[0])
        else:
            # If the file isn't found, append an entry with an empty contents.
            file_contents.append({'file_path': file_path, 'contents': ''})
            print(f'Warning! The file {file_path} was not found in the repository.')

    return file_contents
