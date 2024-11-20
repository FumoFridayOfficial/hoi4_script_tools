import re, os, sys

### IF YOU HAVE COME UP ACROSS THIS FILE, READ BELOW
# This is a python script for hoi4 modding purposes, this script takes every .txt file so you must put your MODDED strategicregion folder, it will read each file and change the numbers by your parameters.
# If a strategic region has provinces that matches your criteria it will sum the provided amount of steps(offset)
# Use cases: To change each file in strategicregions folder instead of one by one, considering each one could have 5 or more provinces to change
# Example:
# 5233 6742 14576 to -> 5233 6742 14579

CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
else:executable_dir = CurrentDirectory
os.chdir(executable_dir)
sys.path.append(os.getcwd())

def update_strategic_regions(file_path, start_id, offset):
    updated_lines = []
    provinces_pattern = re.compile(r"\b\d+\b")  # Match numeric values (provinces)
    inside_provinces_block = False  # Track whether we're inside a provinces block

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "provinces={" in line:
            inside_provinces_block = True
            updated_line = line  # Start with the same line to preserve formatting
            # Extract and update provinces inline
            updated_line = re.sub(
                provinces_pattern,
                lambda x: str(int(x.group()) + offset) if int(x.group()) >= start_id else x.group(),
                updated_line
            )
            updated_lines.append(updated_line)
        elif inside_provinces_block:
            # Handle multiline provinces blocks
            if "}" in line:  # End of provinces block
                inside_provinces_block = False
            updated_line = re.sub(
                provinces_pattern,
                lambda x: str(int(x.group()) + offset) if int(x.group()) >= start_id else x.group(),
                line
            )
            updated_lines.append(updated_line)
        else:
            # For all other lines, keep them as is
            updated_lines.append(line)

    # Write the modified lines back to the file
    with open(file_path, 'w') as f:
        f.writelines(updated_lines)

    print(f"Updated strategic regions in {file_path}")

def process_directory(directory_path, start_id, offset):
    # Walk through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if the file is a valid file (not a directory)
        if os.path.isfile(file_path) and filename.endswith(".txt"):  # assuming .txt files
            update_strategic_regions(file_path, start_id, offset)

if __name__ == "__main__":
    try:
        directory_path = input("Enter the directory path to scan: ").strip()
        start_id = int(input("Enter the starting province ID to update: "))
        offset = int(input("Enter the number of new provinces added (offset): "))
        process_directory(directory_path, start_id, offset)
    except ValueError:
        print("Invalid input. Please provide numeric values for the starting ID and offset.")
