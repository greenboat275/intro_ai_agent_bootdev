import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file in the specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Arguments to pass to the Python file",
                }
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # valid_target_file is True or False
        valid_target_file = (os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs)
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # subprocess
        command = ["python", target_file]

        if args:
            command.extend(args)

        completed = subprocess.run(command, capture_output=True, text=True, timeout = 30)

        output_str = ""
        if completed.returncode != 0:
            exit_code = completed.returncode
            output_str += f"Process exited with code {exit_code}\n"

        if (completed.stdout is None) and (completed.stderr is None):
            output_str += "No output produced\n"
        else:
            output_str += f"STDOUT:{completed.stdout}\n"
            output_str += f"STDERR:{completed.stderr}\n"

        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"

    