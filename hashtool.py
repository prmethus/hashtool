#!/usr/bin/env python

import os
import hashlib
from getpass import getpass
import argparse

example_text = """\
Supported Hash Functions: %s

Examples:
	hashtool --hash="sha512"
	hashtool --hash="md5" --salt="sdfA!c"
	hashtool --hash="whirlpool" --salt="12as!c" --output="/home/username/Documents/hashed_data.txt
	hashtool --hash="md5" --encode
"
""" % ", ".join(
    hashlib.algorithms_available
)

parser = argparse.ArgumentParser(
    description="Hashtool, a command-line tool that uses python's hashlib module for hashing algorithms.",
    epilog=example_text,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("--hash", type=str, help="Hash Function", required=True)
parser.add_argument(
    "--salt", "-s", type=str, default="", help="Salt. Write it in quotes."
)
parser.add_argument(
    "--output",
    "-o",
    type=str,
    help="File Path. Saves the output in a file",
    default=None,
)
parser.add_argument(
    "--encode",
    "-e",
    type=bool,
    help="Encodes the output instead of converting it to String",
    default=False,
)

args = vars(parser.parse_args())

def main():
    hash_func = args["hash"]
    try:   
        _ = hashlib.new(hash_func) # For checking if the hash function is valid

    except ValueError:
        print(
            "Unknown Hash Function. The supported Hash functions are: %s"
            % ", ".join(hashlib.algorithms_available)
        )
        exit()

    salt = args["salt"]
    output_path = args["output"]
    encode = args['encode']
    conversion_method = "hexdigest" if encode == False else "digest"
    data = (getpass("Data: ") + salt).encode("utf-8")
    if hash_func.startswith("shake_"):
        length = int(getpass("Length: "))
        hashed_data = getattr(hashlib.new(hash_func, data), conversion_method)(
            length
        )
    else:
        hashed_data = getattr(hashlib.new(hash_func, data), conversion_method)()
    if output_path == None:
        print(hashed_data)
    else:
        mode = "w" if encode == False else 'wb'
        if os.path.exists(output_path):
            x = (
                input(
                    "The file already exists. Do you want to OVERWRITE the file or APPEND or CANCEL? [o/a/c]: "
                )
                .strip()
                .lower()
            )

            if x == "o":
                pass
            elif x == "a":
                mode = "a" if encode == False else 'ab'
            elif x == "c" or x not in ["o", "a"]:
                print("Cancelling Operation")
                exit()

        with open(output_path, mode) as f:
            if mode == "a":
                f.write("\n")
            f.write(hashed_data)


if __name__ == "__main__":
    main()
