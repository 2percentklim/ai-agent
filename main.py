import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions import *
from call_function import available_functions, call_function
import json
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Chat with OpenRouter API")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    model = "openrouter/free"
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt
        },
    ]



    max_iterations: int = 20

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=available_functions
        )
        if response.usage is None:
            raise RuntimeError("Usage information is not available")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")


        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls == None or message.tool_calls == []:
            print(message.content)
            return
        else:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, verbose=args.verbose)
                if result_message["content"] == None:
                    raise Exception("Function call returned no content")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
    print(f"Model unable to produce final response given {max_iterations} max iterations.")
    sys.exit(1)

main()