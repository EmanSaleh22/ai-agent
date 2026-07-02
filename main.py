import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt

from functions.call_function import call_function
from functions.call_function import available_functions 
def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")


    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not in .env")

    

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    finished = False
   
    for _ in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.usage_metadata is None:
            raise RuntimeError("no (usage_metadata)")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # if response.function_calls:

        #  for function_call in response.function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")

    #  else:
        # print(response.text)

        

        function_responses = []

    
        if response.function_calls:
            messages.append(response.candidates[0].content)

            for function_call in response.function_calls:

                function_call_result = call_function(
                    function_call,
                    verbose=args.verbose,
                )
                

                if not function_call_result.parts:
                    raise RuntimeError(
                        "Function call returned no parts."
                    )

                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError(
                        "Missing function response."
                    )

                if (
                    function_call_result.parts[0]
                    .function_response.response
                    is None
                ):
                    raise RuntimeError(
                        "Missing function response data."
                    )
                result=function_call_result.parts[0].function_response.response
                result_message = types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                function_response={
                                "name":function_call.name,
                                "response":result}
                            )
                        ]
                    )



                messages.append(result_message)

                function_responses.append(
                    function_call_result.parts[0]
                )

                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )

        else:
            print(response.text)
            finished = True
            break

    if not finished :
        print("Error: model did not produce a final response within 20 iterations.")
        exit(1)


if __name__ == "__main__":
    main()
