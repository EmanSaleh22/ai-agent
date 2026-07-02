import os
from google.genai import types



def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        apath=os.path.abspath(working_directory)
        fpath= os.path.normpath(os.path.join(apath,directory))

        valid_target_dir = os.path.commonpath([apath, fpath]) == apath
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        #if not os.path.isdir(directory):
        #    return f'Error: "{directory}" is not a directory'
                



        items=os.listdir(fpath)
        res=[]
        for i in items:
            name=os.path.join(fpath, i)
            size=os.path.getsize(name)
            isdir=os.path.isdir(name)
            res.append(f"- {i}: file_size={size} bytes, is_dir={isdir}")


        return "\n".join(res)   
        
        
    except Exception as e:
        return f"Error: {str(e)}"
    

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
