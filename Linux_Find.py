"""
Linux find command
The find command in Unix is a command-line utility that searches for files in a directory hierarchy.

Problem statement:
Design Unix File Search API to search file with different arguments as "extension", "name", "size" ...
The design should be maintainable to add new contraints.

Use Specification pattern
Why specification and not Strategy?

Follow up: How would you handle if some contraints should support AND, OR conditionals.
"""

from abc import ABC, abstractmethod
from typing import List
from collections import deque

class File:
    def __init__(self, name: str, size: int):
        self.name = name.split(".")[0] if "." in name else name
        self.extension = name.split(".")[1] if "." in name else ""
        self.is_directory = "." not in name
        self.children = []
        self.size = size #in kb
    
    def __str__(self):
        return f"{self.name}.{self.extension}"
    
    def addChildren(self, file):
        self.children.append(file)

# An blue print class for the filter classes
# It gives flexibitly to use filter.apply -> on all while checking
# If we use a standalone function --> Lose of consistency, and scaling issues(Have to manage too many standalone functions)
class Filter(ABC):
    @abstractmethod
    def apply(self, file: File) -> bool:
        pass

class NameFilter(Filter):
    def __init__(self, name):
        self.name = name
        
    def apply(self, file):
        return file.name == self.name
        
class ExtensionFilter(Filter):
    def __init__(self, extension):
        self.extension = extension
        
    def apply(self, file):
        return file.extension == self.extension
        
class MinSizeFilter(Filter):
    def __init__(self, size):
        self.size = size
        
    def apply(self, file):
        return file.size >= self.size
        
class LinuxFindAPI:
    def __init__(self):
        self.filters = []
        
    def addFilter(self, filter: Filter):
        if isinstance(filter, Filter):
            self.filters.append(filter)
            
    # Why root in arguments?
    # Can operate onany directories, and files irrespective of structure
    # Stateless --> Thread Safe --> As it operates independently without depending on any other state
    def apply_AND_Filter(self, root: File) -> List[File]:
        
        foundFiles = []
        queue = deque([root])
        
        while queue:
            curr = queue.popleft()
            
            if curr.is_directory:
                queue.extend(curr.children)
            else:
                if all(filter.apply(curr) for filter in self.filters):
                    foundFiles.append(curr)
                    print(curr.name +"."+ curr.extension)
                    
        return foundFiles
        
    def apply_OR_Filter(self, root: File) -> List[File]:
        
        foundFiles = []
        queue = deque([root])
        
        while queue:
            curr = queue.popleft()
            
            if curr.is_directory:
                queue.extend(curr.children)
            else:
                if any(filter.apply(curr) for filter in self.filters):
                    foundFiles.append(curr)
                    print(curr.name +"."+ curr.extension)
                    
        return foundFiles
        
        
if __name__=="__main__":
    
    root = File("Files", 3000)
    
    movies = File("Movies", 1000)
    songs = File("Songs", 1000)
    subtitles = File("Subtitles", 1000)
    
    root.addChildren(movies)
    root.addChildren(songs)
    root.addChildren(subtitles)
    
    movies.children =[
        File("Interstellar.mp4", 200),
        File("RRR.mp4", 150),
        File("Bahubali.mp4", 250),
        File("Mad Max.mp4", 170),
        File("Dune.mp4", 200)
        ]
        
    songs.children =[
        File("APT.mp3", 200),
        File("anirudh.mp3", 150),
        File("thaman.mp3", 250),
        File("DSP.mp3", 170)
        ]
    
    subtitles.children =[
        File("Interstellar.srt", 10),
        File("RRR.srt", 15),
        File("Bahubali.srt", 25),
        File("Mad Max.srt", 17),
        File("Dune.srt", 20)
        ]
    
    filter = LinuxFindAPI()
    filter.addFilter(NameFilter("Interstellar"))
    filter.addFilter(MinSizeFilter(200))

    filter.apply_AND_Filter(root)
    print("----")
    filter.apply_OR_Filter(root)