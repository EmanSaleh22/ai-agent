from functions.get_files_info import get_files_info

#print(get_files_info("calculator", "."))

#print(get_files_info("calculator", "pkg"))
#print(get_files_info("calculator", "/bin"))
#print(get_files_info("calculator", "../"))
print(
   get_file_content({'file_path': 'main.py'})
)

print(
   write_file({'file_path': 'main.txt', 'content': 'hello'})
)

print(
  get_files_info({'directory': 'pkg'})
)