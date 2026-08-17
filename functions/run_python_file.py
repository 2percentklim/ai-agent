import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory, optionally with command-line arguments, and returns the output as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
    ) -> str:
    try:
        absolute_working_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_working_dir_path, file_path))

        # Check if the target path is within the working directory
        if not target_path.startswith(absolute_working_dir_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        #Check if the target path is a directory and if it is not a regular file
        if os.path.isdir(target_path) or not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # If the file name doesn't end in .py return an error string
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output: str = ""
        # If the process exited with a non-zero returncode, include "Process exited with code X".
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"
        # If both stdout and stderr contained no output (both of which are attributes of CompletedProcess), add "No output produced".
        if not completed_process.stdout and not completed_process.stderr:
            output += "No output produced\n"
        #Otherwise, include any text in stdout prefixed with STDOUT:, and any text in stderr prefixed with STDERR:.
        else:
            output += f"STDOUT:\n{completed_process.stdout}\n" if completed_process.stdout else ""
            output += f"STDERR:\n{completed_process.stderr}\n" if completed_process.stderr else ""

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"