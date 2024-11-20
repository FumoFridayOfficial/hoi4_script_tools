import os, sys, re

### IF YOU HAVE COME UP ACROSS THIS FILE, READ BELOW
# This is a python script for hoi4 modding purposes, this script takes the "adjacencies.csv" and by putting the ID province and how many steps(offset) to sum for the detected numbers in the file.
# Case use: To change many lines faster.
# Example:
# Given the province ID '13100' it will search for numbers that meet this criteria or superior, when it finds one it will change the values with the steps(offset) given, this time is 3.
# 13196;13314;sea;9092;-1;-1;-1;-1;;Northern Quebec
# To
# 13199;13317;sea;9092;-1;-1;-1;-1;;Northern Quebec

CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
else:executable_dir = CurrentDirectory
os.chdir(executable_dir)
sys.path.append(os.getcwd())

def update_adjacencies_csv(start_id, offset, file_path):
    updated_lines = []

    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Match lines with the structure: "number;number;..."
        if re.match(r"^\d+;\d+;", line):
            tokens = line.strip().split(";")  # Split the line into tokens
            try:
                # Parse the first two columns as integers
                value1 = int(tokens[0])
                value2 = int(tokens[1])

                # Update the values if they meet the criteria
                if value1 >= start_id:
                    value1 += offset
                if value2 >= start_id:
                    value2 += offset

                # Replace the first two tokens with updated values
                tokens[0] = str(value1)
                tokens[1] = str(value2)

                # Reconstruct the line
                updated_line = ";".join(tokens) + "\n"
                updated_lines.append(updated_line)
            except ValueError:
                # If parsing fails, append the line as is
                updated_lines.append(line)
        else:
            # If the line does not match the expected structure, leave it unchanged
            updated_lines.append(line)

    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(updated_lines)

    print(f"Updated adjacencies in {file_path}")

if __name__ == "__main__":
    # Prompt user for input
    try:
        start_id = int(input("Enter the starting province ID to update: "))
        offset = int(input("Enter the number of new provinces added (offset): "))
        file_path = input("Enter the path to the adjacencies.csv file: ")

        update_adjacencies_csv(start_id, offset, file_path)
    except ValueError:
        print("Invalid input. Please provide numeric values for the starting ID and offset.")
