
import os


def get_file_content(working_directory, file_path):
    try:
            abs_path = os.path.abspath(working_directory)
            target_dir = os.path.normpath(os.path.join(abs_path, file_path))

            valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

            if valid_target_dir == False:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

            isfile = os.path.isfile(target_dir)
            
            if isfile == False:
                return f'Error: File not found or is not a regular file: "{file_path}"'
            
            MAX_CHARS = 10000

            with open(target_dir, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                
                # After reading the first MAX_CHARS...
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    
            return file_content_string
                    
    except Exception as e:
        return f"Error: {e}"