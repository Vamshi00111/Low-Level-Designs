"""
unix tail -N command
The tail command takes a file as input and prints the last N lines of the file. 
The output is similar to the output of the head command, but in reverse order.

with open(file_name, "r", encoding = "utf-8") as f:
    Open the file in read mode and create a file object
    Also closes the file automatically after the block of code is executed
f.read() - read the entire file
f.readlines() - read the entire file and return a list of lines
f.readline() - read the next line of the file
f.read(n) - read n bytes from the file

# After every read operation, the file pointer moves to the end of the read data

f.seek(offset, whence) - whence: 0 (start of file), 1 (current position), 2 (end of file)
"""
import sys

def tail(file_name, n):

    with open(file_name, "r", encoding = "utf-8") as f:
        
        f.seek(0, 2)
        file_size = f.tell() # Get the size of the file
        lines = []
        buffer = ""
        
        # Start reading from the end of the file
        while len(lines) < n and file_size > 0:
            
            f.seek(file_size)
            nxt = f.read(1)
            file_size -= 1

            if nxt == "\n":
                lines.append(buffer)
                buffer = ""
            else:
                buffer = nxt + buffer

        lines.reverse()

        return lines
     
    
    # O(N), O(N) - Not efficient for large files
    with open(file_name) as f:
        lines = f.readlines()
        return lines[-n:]
    
if __name__ == "__main__":
    file_name = "text.txt"
    n = 3
    print(tail(file_name, n)) # ['line 3\n', 'line 4\n', 'line 5\n']