import os
import pandas as pd

def txt_to_csv_folder(folder_path, output_csv):
    # Initialize an empty list to store data from all text files
    all_data = []

    # Iterate through each file in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a text file
        if file_name.lower().endswith('.txt'):
            # Read the contents of the text file
            with open(os.path.join(folder_path, file_name), 'r') as txt_file:
                lines_of_data = txt_file.readlines()
            # Process each line of the text file
            for line in lines_of_data:
                # Split the line and append the filename to each row
                all_data.append([file_name] + line.strip().split())

    # Create a DataFrame from the list of data
    data_df = pd.DataFrame(all_data)
    data_df.sort_values(by=0, inplace=True)
    # Write the DataFrame to a CSV file
    data_df.to_csv(output_csv, index=False, header=False)

# Example usage
folder_path = 'runs/detect/predict2/labels'  # Path to the folder containing text files
output_csv = 'YOLO/coordinates.csv'         # Path to the output CSV file
txt_to_csv_folder(folder_path, output_csv)
