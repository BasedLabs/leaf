<h1 align="center">LEAF (beta)</h1>

<b>Leaf</b> is a little (just two .py files) in-memory on-demand graph filesystem database.

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
```