import os
import shutil

from leaf import DirectoryObject
from src.leaf import FileObject

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
os.mkdir(root_dir)

root = DirectoryObject(root_dir)
directory: DirectoryObject = root.add_directory('test')
print(os.path.isdir(os.path.join(root_dir, 'test'))) # True

f1: FileObject = directory.add_file('first_file.json')
f2: FileObject = directory.add_file('second_file.json')
print(os.path.isfile(os.path.join(root_dir, 'test', 'first_file.json'))) # True

# Find a file recursively
f3: FileObject | None = root.first_or_default(lambda o: o.name == 'first_file.json', recursive=True)
print(f1 == f3) # True

# Get children
for children in directory.children:
    print(children)
# FILE: D:\PycharmProjects\leaf\leaf\src\files\test\first_file.json
# FILE: D:\PycharmProjects\leaf\leaf\src\files\test\second_file.json

# Get descendants
for desc in root.descendants:
    print(desc)
# DIRECTORY: D:\PycharmProjects\leaf\leaf\src\files\test
# FILE: D:\PycharmProjects\leaf\leaf\src\files\test\first_file.json
# FILE: D:\PycharmProjects\leaf\leaf\src\files\test\second_file.json

print('heehe')
for dir in root.directories:
    print([f.name for f in dir.files])

# Write contents
f1.write_string('hello')
print(f1.read_string())
# hello

shutil.rmtree(root_dir)