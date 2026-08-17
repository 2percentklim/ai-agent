import os
MAX_CHARS = 10000

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a specified file relative to the working directory, returning the content as a string. If the file is too large, it will be truncated to 10,000 characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read from, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    # If the file_path is outside the working_directory, return the error string below. You can reuse the same path-validation approach you wrote for get_files_info.
    # f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        absolute_working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_dir_path, file_path))

        valid_target_dir = os.path.commonpath([absolute_working_dir_path, target_path]) == absolute_working_dir_path

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'

        # If the file_path is not a file, return the error string below.
        f'Error: File not found or is not a regular file: "{file_path}"'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as f:
            content: str = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f"Error: An unexpected error occurred while reading the file: {str(e)}"