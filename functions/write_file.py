import os

def write_file(working_directory, file_path, content):
    
    abs_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path, file_path))

    valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
    
    if valid_target_dir == False:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    try:
        parents = os.path.dirname(target_dir)
        os.makedirs(parents, exist_ok=True)
        
        with open(target_dir, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
        
        
        
        
        
        
        
        
        
        
        
        
    except Exception as e:
        return f"Error: {e}"
    