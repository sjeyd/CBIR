import os
import shutil

def copy_images_to_database(output_folder, database_folder):
    # Create the database folder if it doesn't exist
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    
    # Dictionary to keep track of the count of images copied for each frame
    frame_counts = {}
    
    # Iterate through each frameX subfolder in the output folder
    for frame_folder in os.listdir(output_folder):
        frame_folder_path = os.path.join(output_folder, frame_folder)
        
        # Check if the item in the output folder is a directory and starts with "frame"
        if os.path.isdir(frame_folder_path) and frame_folder.startswith("frame"):
            frame_number = int(frame_folder[5:])
            
            # Initialize the count of images copied for this frame
            frame_counts[frame_number] = 0
            
            crop_folder_path = os.path.join(frame_folder_path, 'crops')
            
            # Check if the 'crops' subfolder exists within the frameX folder
            if os.path.exists(crop_folder_path):
                # Iterate through each subfolder in the 'crops' folder
                for subfolder in os.listdir(crop_folder_path):
                    subfolder_path = os.path.join(crop_folder_path, subfolder)
                    
                    # Check if the item in the crops folder is a directory and starts with "person"
                    if os.path.isdir(subfolder_path) and subfolder.startswith("person"):
                        # Iterate through each file in the 'person' subfolder
                        for file_name in os.listdir(subfolder_path):
                            file_path = os.path.join(subfolder_path, file_name)
                            
                            # Check if the file is an image file
                            if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                                # Increment the count of images copied for this frame
                                frame_counts[frame_number] += 1
                                
                                # Construct the new filename
                                new_file_name = f"{frame_folder}_image_{frame_counts[frame_number]}.jpg"
                                
                                # Copy the image to the database folder with the new filename
                                shutil.copy(file_path, os.path.join(database_folder, new_file_name))

# Example usage
output_folder = 'output'
database_folder = 'database'
copy_images_to_database(output_folder, database_folder)
