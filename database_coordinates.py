import os
import pandas as pd

def txt_to_csv(output_folder, output_csv):
    # Initialize an empty DataFrame
    all_data = pd.DataFrame()

    # Iterate through each frameX subfolder in the output folder
    for frame_folder in os.listdir(output_folder):
        frame_folder_path = os.path.join(output_folder, frame_folder)
        
        # Check if the item in the output folder is a directory and starts with "frame"
        if os.path.isdir(frame_folder_path) and frame_folder.startswith("frame"):
            labels_folder_path = os.path.join(frame_folder_path, 'labels')
            
            # Check if the 'labels' subfolder exists within the frameX folder
            if os.path.exists(labels_folder_path):
                # Iterate through each file in the 'labels' subfolder
                for file_name in os.listdir(labels_folder_path):
                    if file_name.endswith('.txt'):
                        # Read the contents of the text file
                        with open(os.path.join(labels_folder_path, file_name), 'r') as file:
                            lines_of_data = file.readlines()
                        # Convert data to DataFrame
                        df = pd.DataFrame([line.split() for line in lines_of_data])
                        # Add a column with the filename
                        df.insert(0, 'Frame', [f'{frame_folder}_image_{i+1}' for i in range(len(df))])
                        # Append DataFrame to the main DataFrame
                        all_data = pd.concat([all_data, df], axis=0)

    # Write the DataFrame to a CSV file
    all_data.to_csv(output_csv, index=False)

# Example usage
output_folder = 'output'
output_csv = 'database_coordinates/output.csv'
txt_to_csv(output_folder, output_csv)
