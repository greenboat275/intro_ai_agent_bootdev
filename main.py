import os
import sys
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    #print("Hello from free-agent!")

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")

    # Initialize OpenAI client with OpenRouter API
    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    # Input prompt from command line argument
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Prepare the messages for the chat completion request
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for i in range(20):  # Limit to 20 iterations to prevent infinite loops
        # Make the API request to OpenRouter
        response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0.7,
        )

        res_message = response.choices[0].message
        messages.append(res_message) # make model aware of the response from the previous iteration

        if res_message.tool_calls:
            for tool_call in res_message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
                result_message = call_function(tool_call, verbose=args.verbose)
                messages.append(result_message) # make model aware of the response from the previous iteration
                if result_message["content"] is None:
                    raise Exception(f"Function {tool_call.function.name} returned None")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                if i >= 20:
                    print("Reached maximum iterations. Exiting.")
                    sys.exit(1)
                
        else:
            break  # No tool calls, exit the loop

    # Print the user prompt
    if args.verbose:
        print(f'User prompt: "{args.user_prompt}"')

        # Print the response and token usage
        usage_meta = response.usage
        if usage_meta is None:
            raise RuntimeError("Failed API request")

        prompt_tokens = usage_meta.prompt_tokens
        completion_tokens = usage_meta.completion_tokens
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")

    print(f"Final Response:\n{res_message.content}")



if __name__ == "__main__":
    main()
