import os
import shutil
import unittest

from src.leaf import DirectoryObject, FileObject


class Tests(unittest.TestCase):
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')

    @classmethod
    def setUp(cls):
        os.mkdir(Tests.root)

    @classmethod
    def tearDown(cls):
        shutil.rmtree(Tests.root)

    def test_creates_root(self):
        # arrange
        root = DirectoryObject(self.root)

        # assert
        self.assertEqual(os.path.normpath(root.full_path), os.path.normpath(self.root))

    def test_creates_file(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        root.add_file('test.json')

        # assert
        self.assertTrue(os.path.isfile(os.path.join(self.root, 'test.json')))

    def test_creates_dir(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        root.add_directory('test')

        # assert
        self.assertTrue(os.path.isdir(os.path.join(self.root, 'test')))

    def test_creates_inner_dir(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        d1.add_directory('test2')

        # assert
        self.assertTrue(os.path.isdir(os.path.join(self.root, 'test', 'test2')))

    def test_creates_inner_file(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        d1.add_file('test.json')

        # assert
        self.assertTrue(os.path.isfile(os.path.join(self.root, 'test', 'test.json')))

    def test_lists_children(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        f = d1.add_file('test.json')

        # assert
        self.assertEqual(list(d1.children), [f])

    def test_where(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        f = d1.add_file('test.json')

        # assert
        self.assertEqual(list(root.where(lambda o: o.name == 'test.json', recursive=True)), [f])
        self.assertEqual(list(d1.where(lambda o: o.name == 'test.json')), [f])

    def test_first_or_default(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        f = d1.add_file('test.json')

        # assert
        self.assertEqual(root.first_or_default(lambda o: o.name == 'test.json', recursive=True), f)
        self.assertEqual(d1.first_or_default(lambda o: o.name == 'test.json'), f)

    def test_delete_file(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        f = d1.add_file('test.json')
        f.delete()

        # assert
        self.assertTrue(not os.path.isfile(os.path.join(self.root, 'test', 'test.json')))

    def test_lists_directories(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')

        # assert
        self.assertEqual(list(root.directories)[0], d1)

    def test_lists_files(self):
        # arrange
        root = DirectoryObject(self.root)

        # act
        d1: DirectoryObject = root.add_directory('test')
        f1: FileObject = d1.add_file('test.json')

        # assert
        self.assertEqual(list(d1.files)[0], f1)


if __name__ == '__main__':
    unittest.main()
