import sys
import mmap
sys.path.append('C:/Program Files/Truxton/SDK')
import truxton

def main():
  with open(sys.argv[1], mode="r") as input_file:
    with mmap.mmap(input_file.fileno(), length=0, access=mmap.ACCESS_READ) as memory_buffer:
      b = memory_buffer.read()
      file_type = truxton.identify(b)
      print( "File Type is " + str(file_type) )
      details = truxton.details(file_type, b)
      print( details )

if __name__ == "__main__":
    main()