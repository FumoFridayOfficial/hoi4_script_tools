import os, sys
import re

### IF YOU HAVE COME UP ACROSS THIS FILE, READ BELOW
# This is a python script for hoi4 modding purposes, this script takes every state file and fixes the provices inside, it works by reading every line and then finds for a number that is the same or higher to your
# provided province number, if let's say province 13300 is where your custom provinces start, then you provide it the id 13301 and it will go for each state file and change the provinces that matches the number or higher.
# Case use: TO change provinces inside state without going one by one.
# Examples:
# Updated provinces in 995-StateName.txt
# -
# There's 4 provinces in this state, 4522, 1353, 5566, 14140
# And you give it province ID 13301, it will find the number wich is equal or above and sum it the given amount of steps, so if we provide an offset of 3, it will be 14143

CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
else:executable_dir = CurrentDirectory
os.chdir(executable_dir)
sys.path.append(os.getcwd())

def update_province_lines_preserving_format(start_id, offset, directory):
    # Keywords to ignore for modifications
    ignore_keywords = ["manpower=", "state=", "id="]

    # Function to check if a line should be ignored
    def should_ignore_line(line):
        return any(keyword in line for keyword in ignore_keywords)

    # Iterate through all .txt files in the specified directory
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for file in files:
        file_path = os.path.join(directory, file)
        updated_lines = []

        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            # Preserve indentation and trailing spaces
            leading_spaces = re.match(r"^\s*", line).group()
            trailing_spaces = re.match(r".*?(\s*)$", line).group(1)

            if should_ignore_line(line):
                # If the line matches any ignore keyword, leave it as is
                updated_lines.append(line)
                continue

            # Check if the line contains numbers
            if re.search(r"\b\d+\b", line):
                # Split the line into tokens to process numbers
                updated_tokens = []
                for token in line.split():
                    try:
                        # Convert token to an integer
                        number = int(token)
                        # Modify if it meets the criteria
                        if number >= start_id:
                            number += offset
                        updated_tokens.append(str(number))
                    except ValueError:
                        # If not a number, keep it unchanged
                        updated_tokens.append(token)

                # Reconstruct the line while preserving original formatting
                updated_line = leading_spaces + " ".join(updated_tokens) + trailing_spaces + "\n"
                updated_lines.append(updated_line)
            else:
                # Lines without numbers are left unchanged
                updated_lines.append(line)

        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.writelines(updated_lines)

        print(f"Updated provinces in {file}")

if __name__ == "__main__":
    # Prompt user for input
    try:
        start_id = int(input("Enter the starting province ID to update: "))
        offset = int(input("Enter the number of new provinces added (offset): "))
        directory = input("Enter the directory containing state files: ")

        update_province_lines_preserving_format(start_id, offset, directory)
    except ValueError:
        print("Invalid input. Please provide numeric values for the starting ID and offset.")
