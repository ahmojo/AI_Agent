import sys
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import call_function

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="takes working directory and path as inputs and return content of that file parameters:  file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path for the file it runs on",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content in to a file. parameters = file_path, content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="points to the file",
            ),
            "content": types.Schema(
            type=types.Type.STRING,
            description="The content to write into the file",
),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file. parameters = file_path, args=None",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path points to a python file that gets ran",
            ),
            "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description="optional argument for the command",)
        },
    ),
)


def main():
    
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_write_file, schema_get_file_content, schema_run_python_file],
)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY was not found.")
    
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for i in range(22):
        
        if i == 21:
            
            print("Max iterations reached")
            sys.exit(1)
        
        response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
        ))  
        
        if not response.candidates:
            continue
        for candidate in response.candidates:
            messages.append(candidate.content)
        usage = response.usage_metadata
        if usage is not None and  args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
            
       
        
        list_of_calls = response.function_calls
        
        list_of_function_call = []
        if list_of_calls is not None:
            for fn in list_of_calls:
                function_call_result = call_function(fn, args.verbose)
                if not function_call_result.parts:
                    raise Exception("empty function call result")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("empty function call result")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("empty function call result")
                list_of_function_call.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=list_of_function_call))
        
        else:
            print(response.text)
            return
            
        
            
        
            
 


if __name__ == "__main__":
    main()
