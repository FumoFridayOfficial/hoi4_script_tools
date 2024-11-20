import os, sys, re

### IF YOU HAVE COME UP ACROSS THIS FILE, READ BELOW
# This is a python script for hoi4 modding purposes, this script takes "your_provinces.csv" file, you need to provice ONLY YOUR MODDED PROVINCES, then you shall provide a name for the NEW .csv file
# and lastly ask from WICH ID start, so if you have a few provinces overlapping, let's say your mod and paradox have 13000 as province ID in the definition.csv, then you take a new file with YOUR PROVINCES and
# provide this file to the script and ask it to start from 13001, or the next avaliable ID.
# Case use: When you have a thousand provinces to change but you better off changing them all automatically
# Example:
# Enter the name of the input file (e.g., definition.csv): definition - backup.csv
# Enter the name of the output file (e.g., updated_definition.csv): definition_fix.csv      
# Enter the starting ID for the new provinces: 13366
# Updated province IDs written to definition_fix.csv.


CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
else:executable_dir = CurrentDirectory
os.chdir(executable_dir)
sys.path.append(os.getcwd())


def update_province_ids(input_file, output_file, start_id):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    updated_lines = []
    current_id = start_id
    
    for line in lines:
        # Extract the original province ID (first value in the line)
        match = re.match(r'^(\d+);', line)
        if match:
            old_id = int(match.group(1))
            # Replace the old ID with the new one
            new_line = re.sub(rf'^{old_id};', f'{current_id};', line)
            updated_lines.append(new_line)
            current_id += 1
        else:
            # If no match, retain the line unchanged (e.g., headers or invalid lines)
            updated_lines.append(line)
    
    # Write the updated lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(updated_lines)
    
    print(f"Updated province IDs written to {output_file}.")

if __name__ == "__main__":
    # Prompt the user for input file, output file, and starting ID
    input_file = input("Enter the name of the input file (e.g., definition.csv): ")
    output_file = input("Enter the name of the output file (e.g., updated_definition.csv): ")
    try:
        start_id = int(input("Enter the starting ID for the new provinces: "))
        update_province_ids(input_file, output_file, start_id)
    except ValueError:
        print("Invalid input. Please enter a numeric value for the starting ID.")
