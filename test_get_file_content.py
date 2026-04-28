from functions.get_files_content import get_file_content

def main():
    
    result = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(result)}")
    print(f"End of content: {result[-80:]}")
    
    
    print(get_file_content("calculator", "main.py"))
    
    print(get_file_content("calculator", "pkg/calculator.py"))
    
    print(get_file_content("calculator", "/bin/cat"))
    
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()