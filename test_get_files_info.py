from functions.get_files_info import get_files_info

# test1
print(get_files_info("calculator","."))

# test2
print(get_files_info("calculator","pkg"))

# test3
print(get_files_info("calculator","/bin"))

# test4
print(get_files_info("calculator","../"))
