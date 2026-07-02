import os
from google.genai import types
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        apath=os.path.abspath(working_directory)
        fpath = os.path.abspath(os.path.normpath(os.path.join(apath, file_path)))
       
        valid_target_dir = os.path.commonpath([apath, fpath]) == apath
        
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(fpath):
           return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(fpath), exist_ok=True)

        with open(fpath, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    

    except Exception as e:
        return f"Error: {str(e)}"  

write_file_schema = {
    "name": "write_file",
    "description": "create file write",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "path"
            },
            "content": {
                "type": "string",
                "description": "content"
            }
        },
        "required": ["file_path", "content"]
    }
}              