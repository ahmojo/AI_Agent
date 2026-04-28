import os

def get_files_info(working_directory, directory="."):
    try:
        

        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'
        all_items = []
        for item in os.listdir(target_dir):
            itempath = os.path.join(target_dir, item)
            name = item
            isdir = os.path.isdir(itempath)
            size = os.path.getsize(itempath)
            all_items.append(f"- {name}: file_size={size} bytes, is_dir={isdir}")

        return "\n".join(all_items)

    except Exception as e:
        return f"Error: {e}"
    