# Display the contents of a file.

import argparse
import csv


def main(file_name: str):
    with open(f'{file_name}', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            print(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # The name of the file to display.
    parser.add_argument("file_name", type=str, help="Display the contents of the given file.")

    args = parser.parse_args()

    main(args.file_name)
