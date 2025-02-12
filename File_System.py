from datetime import datetime
from typing import Dict, Union

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.created_at = datetime.now()

class Directory:
    def __init__(self, name: str):
        self.name = name
        self.children = {}  # Forward reference for Directory

    def create_file(self, name: str, size: int):
        if name in self.children:
            raise ValueError("File or directory already exists.")
        self.children[name] = File(name, size)

    def create_directory(self, name: str):
        if name in self.children:
            raise ValueError("File or directory already exists.")
        self.children[name] = Directory(name)

    def delete(self, name: str):
        if name not in self.children:
            raise ValueError("File or directory not found.")
        del self.children[name]

    def move(self, name: str, target_directory: 'Directory'):
        if name not in self.children:
            raise ValueError("File or directory not found.")
        if name in target_directory.children:
            raise ValueError("Target directory already contains an item with the same name.")
        target_directory.children[name] = self.children.pop(name)

    def list_contents(self):
        return list(self.children.keys())

class FileSystem:
    def __init__(self):
        self.root = Directory("root")

    def get_root(self):
        return self.root

# Example Usage
fs = FileSystem()
root = fs.get_root()
root.create_directory("docs")
root.create_file("file1.txt", 100)
docs = root.children["docs"]
docs.create_file("notes.txt", 50)
print(root.list_contents())  # ['docs', 'file1.txt']
print(docs.list_contents())  # ['notes.txt']
