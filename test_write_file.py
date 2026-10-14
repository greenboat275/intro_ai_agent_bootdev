from functions.write_file import write_file

# test1
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

# test2
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

# test3
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))