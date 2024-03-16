<h1 align="center">LEAF (beta)</h1>

<b>Leaf</b> is a small (just two .py files) in-memory on-demand graph filesystem database.

Example usage:

```python
from src.leaf import RootObject

# Empty directory
o = RootObject('D:/PycharmProjects/leaf/leaf/files')

print(o)
# DIRECTORY: D:/PycharmProjects/leaf/leaf/files

print(list(o.children))
# []

children = o.add_children('test.json')
print(list(o.children))
# [TEMPORAL: D:/PycharmProjects/leaf/leaf/files\test.json]

children2 = o.add_children('test.txt')
print(children.physically_exists())
# False

print(children.type)
# TEMPORAL

children.write_json({'hello': 1})
print(list(o.children))
# [TEMPORAL: D:/PycharmProjects/leaf/leaf/files\test.txt, File: D:/PycharmProjects/leaf/leaf/files\test.json]

children2.delete()
print(list(o.children))
# [FILE: D:/PycharmProjects/leaf/leaf/files\test.json]

directory1 = o.add_children('directory')
directory1.add_children('dir_test2.txt')
directory1.add_children('directory2')
directory2 = directory1.ch_first_or_default(lambda o: o.name == 'directory2')
directory2.add_children('dir_test3.txt')
directory2.ch_first_or_default(lambda o: 'txt' in o.name).write_json({'HELLO':1111})
print(list(directory1.children))
# [TEMPORAL: D:/PycharmProjects/leaf/leaf/files\directory\dir_test2.txt, DIRECTORY: D:/PycharmProjects/leaf/leaf/files\directory\directory2]
print(list(directory2.children))
# [FILE: D:/PycharmProjects/leaf/leaf/files\directory\directory2\dir_test3.txt]
```
