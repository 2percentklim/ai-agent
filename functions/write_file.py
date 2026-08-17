import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory. If the file does not exist, it will be created along with any necessary parent directories.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_dir_path, file_path))

        # Check if the target path is within the working directory
        if not target_path.startswith(absolute_working_dir_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        #Check if the target path is a directory
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Make sure that all parent directories of the file_path exist. You can use os.makedirs() with the exist_ok=True argument to create any missing directories. If the necessary directory structure already exists, this will do nothing – which is what we want.
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # Write the content to the file
        with open(target_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: An unexpected error occurred while writing to the file: {str(e)}"