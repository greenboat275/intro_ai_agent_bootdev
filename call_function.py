import json

from collections.abc import Callable
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    """
    Calls the appropriate function based on the tool_call object.

    Args:
        tool_call: The tool call object containing the function name and arguments.
        verbose: If True, prints additional information.

    Returns:
        A dictionary containing the result of the function call.
    """
    function_name = tool_call.function.name
    function_args = tool_call.function.arguments or "{}"
    
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    print(f" - Calling function: {function_name}")
    
    # Convert the arguments from JSON string to a dictionary
    args_dict = json.loads(function_args)

    if function_name not in function_map:
        return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"Error: Unknown function: {function_name}",
    }

    # Inject the working_directory argument
    args_dict["working_directory"] = "./calculator" # set the working directory to the calculator folder, so that no other files can be accessed

    # Call the appropriate function based on the function name and arguments
    result = function_map[function_name](**args_dict)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }