#!/usr/bin/python

# Method to create and run a menu allowing for user interaction

import create_instance
import create_bucket
import upload_file


# Prints menu for user interaction
def print_menu():
    print('                         \n'
          '         Welcome         \n'
          '-------------------------\n'
          '-------------------------\n'
          '- 1) Create ec2 instance \n'
          '-------------------------\n'
          '- 2) Create s3 bucket    \n'
          '-------------------------\n'
          '- 3) Upload file         \n'
          '-------------------------\n'
          '- 0) Exit                \n'
          '-------------------------\n'
          '-------------------------')


def run_menu():
    loop = True  # Ensures the menu keeps running
    while loop:
        print_menu()
        choice = input('->')

        if choice == '1':
            create_instance.main()

        if choice == '2':
            create_bucket.main()

        if choice == '3':
            upload_file.main()

        if choice == '0':
            loop = False  # Stops loop from running, exiting script


def main():
    run_menu()


if __name__ == '__main__':
    main()