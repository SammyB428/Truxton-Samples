import sys
from enum import Enum
sys.path.append('C:/Program Files/Truxton/SDK')
import truxton

def main() -> None:
  t = truxton.create()
  print("Truxton Version: " + t.version)
  return None

if __name__ == "__main__":
  sys.exit(main())
