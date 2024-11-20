import csv
import random
import os, sys, re

### IF YOU HAVE COME UP ACROSS THIS FILE, READ BELOW
# This is a python script for hoi4 modding purposes, this script creates new RGB colors that do not overlap with the current colors.
# It reads the file 'definition.csv' wich stores provinces data like RGB colors, using this list and a random RGB picker will generate as many new colors as the user asks.
# And the new colors are stored in a file created in the same folder called 'new_colors.csv'
# Case use: instead of generating new colors one by one you can generate 50 or more colors and assign them the province data faster.
# Example:
# 13925;66;55;129
# 13926;251;84;229
# 13927;38;71;199
# 13928;242;21;240
# 13929;171;129;218
# It generates province IDs that don't overlap and chooses RGB colors that don't overlap either.

CurrentDirectory = str(os.path.dirname(__file__)) # TEMP FOLDER
if getattr(sys, 'frozen', False):executable_dir = os.path.dirname(sys.executable) # EXECUTABLE RELATIVE FOLDER
else:executable_dir = CurrentDirectory
os.chdir(executable_dir)
sys.path.append(os.getcwd())

# Function to read the CSV and extract RGB values and the last ID
def read_csv_extract_rgb_and_last_id(file_path):
    used_rgb = set()  # Store unique RGB values
    last_id = 0       # Track the last ID found
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            if len(row) >= 4:  # Ensure there are enough columns for ID, R, G, B
                try:
                    # Extract RGB values
                    r = int(row[1])
                    g = int(row[2])
                    b = int(row[3])
                    # Add RGB tuple to the set
                    used_rgb.add((r, g, b))
                    
                    # Extract the last ID and update last_id
                    current_id = int(row[0])
                    if current_id > last_id:
                        last_id = current_id
                except ValueError:
                    print(f"Skipping row {row} due to invalid data")
    
    return used_rgb, last_id

# Function to generate random RGB values that aren't already used
def generate_random_colors(used_rgb, num_colors):
    generated_colors = []
    while len(generated_colors) < num_colors:
        # Generate a random RGB value
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        if (r, g, b) not in used_rgb:  # Ensure it's not already used
            generated_colors.append((r, g, b))
            used_rgb.add((r, g, b))  # Add it to the used list
    return generated_colors

# Function to write new colors to a CSV file with new IDs
def write_new_colors_to_csv(file_path, start_id, new_colors):
    with open(file_path, 'a', newline='') as file:  # Open in append mode
        csv_writer = csv.writer(file, delimiter=';')
        current_id = start_id
        for color in new_colors:
            r, g, b = color
            csv_writer.writerow([current_id, r, g, b])
            current_id += 1

# Main function
def main():
    input_file_path = CurrentDirectory + '\definition.csv'
    output_file_path = CurrentDirectory + '\\new_colors.csv'

    # Read the input CSV to extract used RGB values and the last ID
    used_rgb, last_id = read_csv_extract_rgb_and_last_id(input_file_path)

    # Ask user how many random colors to generate
    num_colors = int(input("How many random colors to generate? "))

    # Generate new colors
    new_colors = generate_random_colors(used_rgb, num_colors)

    # Write new colors to the output CSV file, starting from the next ID
    next_free_id = last_id + 1
    write_new_colors_to_csv(output_file_path, next_free_id, new_colors)

    print(f"{num_colors} new random colors (RGB) with IDs starting from {next_free_id} have been written to {output_file_path}.")

if __name__ == "__main__":
    main()
