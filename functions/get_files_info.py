import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    # the directory parameter will be treated as a relative path within the working_directory
    try:
        absolute_working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_dir_path, directory))

        valid_target_dir = os.path.commonpath([absolute_working_dir_path, target_path]) == absolute_working_dir_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
        
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory.'

        # After the path validation succeeds, iterate over the items in the target directory. For each item, record:
        # The name
        # The file size
        # Whether it's a directory 
        items_list: list[(str, str, str)] = []
        try:
            for item_name in os.listdir(target_path):
                item_path = os.path.join(target_path, item_name)
                items_list.append(
                    (
                        item_name,
                        os.path.getsize(item_path),
                        True if os.path.isdir(item_path) else False
                    )
                )
            # Use that data to build and return a string representing the contents of the target directory. It should use this format:
            # - README.md: file_size=1032 bytes, is_dir=False
            # - src: file_size=128 bytes, is_dir=True
            # - package.json: file_size=1234 bytes, is_dir=False
            formatted_items_list: list[str] = []
            for item_name, file_size, is_dir in items_list:
                formatted_items_list.append(
                    f'- {item_name}: file_size={file_size} bytes, is_dir={is_dir}'
                )
            return "\n".join(formatted_items_list)
        # If any errors are raised by the standard library functions that you call, catch them and instead return a string describing the error. When returning an error string, always prefix it with Error:
        except Exception as e:
            return f"Error: An unexpected error occurred while listing the directory contents: {str(e)}"
            
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

