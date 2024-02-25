import os

def get_files_and_contents(folder_path):
    files_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as file_content:
                    content = file_content.read()
                    files_list.append({"filePath": file_path, "contents": content})
            except Exception as e:  # Handling files that cannot be read (binary files, permissions, etc.)
                files_list.append({"filePath": file_path, "contents": f"Error reading file: {e}"})
    return files_list