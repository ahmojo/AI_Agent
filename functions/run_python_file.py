import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        
        if valid_target_dir == False:
                    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        isfile = os.path.isfile(target_dir)
        if isfile == False:
                    return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_dir.endswith('.py') == False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]

        if args != None:
            command.extend(args)
        sub = subprocess.run(command, cwd=working_directory, timeout=30,  capture_output=True, text=True)
        parts = []
        if sub.returncode != 0:
            parts.append(f"Process exited with code {sub.returncode}")
        if not sub.stdout and not sub.stderr:
            parts.append("No output produced")
        if sub.stdout:
            parts.append(f"STDOUT: {sub.stdout}")
        if sub.stderr:
            parts.append(f"STDERR: {sub.stderr}")
        return "\n".join(parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"