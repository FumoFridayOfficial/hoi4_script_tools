import os, sys, re

### IF YOU HAVE COME UP ACROSS THIS FILE, READ BELOW
# This is a python script for hoi4 modding purposes, this script takes every file inside the folder it's in and reads the filename and contents and it changes the ID number of those files.
# Case use: Imagine Paradox releases new states, and your mod has overlapping state numbers, now problem is, if you have 100+ states to modify you can take the overlapping states into a new folder, then tell the script from wich ID to start with
# and then it will automatically change each file, this only works for state files.
# Example:
# Updated 970-Oradea.txt -> 982-Oradea.txt
# Updated 971-Cluj.txt -> 983-Cluj.txt    
# Updated 972-Tulcea.txt -> 984-Tulcea.txt

CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
else:executable_dir = CurrentDirectory
os.chdir(executable_dir)
sys.path.append(os.getcwd())

def update_state_files(start_id):
    # List all .txt files in the current directory
    files = [f for f in os.listdir() if f.endswith('.txt')]
    
    # Sort files by state ID in filename
    files.sort(key=lambda x: int(re.match(r'(\d+)', x).group(1)))
    
    for file in files:
        # Extract the original state ID from the filename
        match = re.match(r'(\d+)-(.+)\.txt', file)
        if not match:
            print(f"Skipping invalid filename: {file}")
            continue
        
        old_id = int(match.group(1))
        state_name = match.group(2)
        new_id = start_id
        start_id += 1
        
        new_filename = f"{new_id}-{state_name}.txt"
        
        # Read the content of the file
        with open(file, 'r') as f:
            content = f.read()
        
        # Replace the ID and state name inside the file
        content = re.sub(rf'id={old_id}', f'id={new_id}', content)
        content = re.sub(rf'name="STATE_{old_id}"', f'name="STATE_{new_id}"', content)
        
        # Write the updated content to a new file
        with open(new_filename, 'w') as f:
            f.write(content)
        
        # Remove the old file
        os.remove(file)
        
        print(f"Updated {file} -> {new_filename}")

if __name__ == "__main__":
    # Prompt the user for the starting ID
    try:
        start_id = int(input("Enter the starting ID for the new states: "))
        update_state_files(start_id)
    except ValueError:
        print("Invalid input. Please enter a numeric value for the starting ID.")
