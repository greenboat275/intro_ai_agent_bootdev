from functions.run_python_file import run_python_file

# test1
print(run_python_file("calculator", "main.py"))

# test2
print(run_python_file("calculator", "main.py",["3 + 5"]))

# test3
print(run_python_file("calculator", "tests.py"))

# test4
print(run_python_file("calculator", "../main.py"))

# test5
print(run_python_file("calculator", "nonexistent.py"))

# test6
print(run_python_file("calculator", "lorem.txt"))