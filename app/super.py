# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
from parsers import create_argparser
from controller import services

def main():
    args = create_argparser()
    services(args)

if __name__ == "__main__":
    main()
    
