import os
import subprocess
from google.genai import types
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        apath=os.path.abspath(working_directory)
        fpath = os.path.abspath(os.path.normpath(os.path.join(apath, file_path)))
       
        valid_target_dir = os.path.commonpath([apath, fpath]) == apath
        
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        

        if not os.path.isfile(fpath):
           return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not fpath.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", fpath]
        if args:
           command.extend(args)

        strres=""
        res=subprocess.run(command,cwd=apath,capture_output=True,text=True,timeout=30)
        
        if res.returncode !=0:
            strres += f"Process exited with code {res.returncode}\n"

        if not res.stdout and  not res.stderr :
            strres+="No output produced"

        else:
            if res.stdout :
                strres += f"STDOUT:\n{res.stdout}\n"
            if   res.stderr:
                    strres += f"STDERR:\n{res.stderr}\n"
        
        return strres
    except Exception as e:
        return f"Error: executing Python file: {e}"  

run_python_file_schema = {
    "name": "run_python_file",
    "description": "run py file",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "path"
            },
            "args": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "input"
            }
        },
        "required": ["file_path"]
    }
}