import csv
import platform
import sys
import argparse


def print_file_content(file):
    with open(file) as opened_file:
        content = opened_file.readlines()

    for line in content:
        print(line.strip().split(','))


def write_list_to_file(output_file, *lst):
    if platform.system() == 'Windows':
        newline = ''
    else:
        newline = None

    with open(output_file, 'a', newline=newline) as file:
        output_writer = csv.writer(file)

        for element in lst:
            output_writer.writerow(element)


def read_csv(input_file):
    with open(input_file) as file:
        content = file.readlines()

    lst = []

    for line in content:
        lst.append(line)

    return(lst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for Week 2 Excercise 1")
    parser.add_argument("input_file", help="The path to the file to consume")
    parser.add_argument("--file", dest="file_name",
                        help="The path to the file to print to(prints to console if no file is given)", required=False)

    args = parser.parse_args()

    if not (args.file_name):  # Output file not provoided
        print_file_content(args.input_file)
    else:
        write_list_to_file(args.file_name, read_csv(args.input_file))
