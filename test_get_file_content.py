from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

# test1
print(get_file_content("calculator", "main.py"))

# test2
print(get_file_content("calculator", "pkg/calculator.py"))

# test3
print(get_file_content("calculator", "/bin/cat"))

# test4
print(get_file_content("calculator", "pkg/does_not_exist.py"))