import os
from google.genai import types
def get_file_content(working_directory: str, file_path: str) -> str:    
    try:
        apath=os.path.abspath(working_directory)
        fpath = os.path.abspath(os.path.normpath(os.path.join(apath, file_path)))

        valid_target_dir = os.path.commonpath([apath, fpath]) == apath
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(fpath):
           return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with  open(fpath, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):  
                    file_content_string+= (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'  )
        return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"   


get_file_content_schema = {
    "name": "get_file_content",
    "description": "قراءة محتوى ملف موجود داخل النظام",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "مسار الملف المراد قراءته"
            }
        },
        "required": ["file_path"]
    }
}     
    
    