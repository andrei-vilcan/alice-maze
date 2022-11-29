import sys

# You do NOT need to include any error checking. I found this particular
# check personally helpful, when I forgot to provide a filename.

if len(sys.argv) != 2:
    print("Usage: python3 Alice.py <inputfilename>")
    sys.exit()

# Here is how you open a file whose name is given as the first argument
f = open(sys.argv[1])

# readline returns the next line from the file reader as a string
# including the linefeed
grid_size = int(f.readline())
print(grid_size)

# I found the string functions .split() and .strip() helpful when
# I was converting from my input text file representing a maze to the
# data structure representing a maze in my code
