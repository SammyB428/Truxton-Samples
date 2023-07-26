import sys
sys.path.append('C:/Program Files/Truxton/SDK')
import truxton

def main():
  t = truxton.create()
  print("Truxton Version: " + t.version)
  return None

if __name__ == "__main__":
  main()
