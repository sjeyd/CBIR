import pandas as pd
import numpy as np
import os 
import cv2
import shutil

# Function to calculate Euclidean distance between two feature vectors
def euclidean_distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))

# Read the CSV file into a Pandas DataFrame, skipping the first row
df = pd.read_csv('FeatureExtraction/feature_vectors_alpha_1.csv', header=None, skiprows=1)

# Input image name
input_image_name = 'frame100_image_1.jpg'  # Change this to the name of your input image

# Extract the feature vector of the input image
input_feature_vector = df[df.iloc[:, 0] == input_image_name].iloc[:, 1:].values.flatten().astype(float)

# Calculate Euclidean distance for each image
distances = {}
for index, row in df.iterrows():
    image_name = row.iloc[0]
    if image_name != input_image_name:
        feature_vector = row.iloc[1:].values.astype(float)
        distance = euclidean_distance(input_feature_vector, feature_vector)
        distances[image_name] = distance

# Get the top 10 minimum distances

top_10_distances = sorted(distances.items(), key=lambda x: x[1])[:20]

# # Display the top 10 minimum distances with image names
imageName_array = []

for image_name, distance in top_10_distances:
    imageName_array.append(image_name)
    #print(f"Image: {image_name}, Distance: {distance}")
#print(imageName_array)


# List to store corresponding image paths
image_paths = []

# Path to the output folder
output_folder = "output"

# Iterate over each output image name
for output_image_name in imageName_array:
    # Extract the frame number from the output image name
    frame_number = output_image_name.split("_")[0]

    # Iterate over subfolders in the output folder
    for folder_name in os.listdir(output_folder):
        if folder_name.startswith("frame"):
            # Check if the subfolder name contains the frame number
            if frame_number in folder_name:
                # Path to the subfolder
                frame_folder = os.path.join(output_folder, folder_name)
                # Look for the image file in the subfolder
                for file_name in os.listdir(frame_folder):
                    if file_name.endswith(".jpg"):
                        # Add the image path to the list
                        image_paths.append(file_name)

# Display the list of image paths
imageName_array = [image_name.replace('.jpg', '') for image_name in imageName_array]
# print(imageName_array)
# print(image_paths)




# Read the CSV file into a DataFrame, skipping the first row
df = pd.read_csv('database_coordinates/output.csv', header=None, skiprows=1)

# Dictionary to store image paths as keys and coordinates as values
image_coordinates = {}


# Iterate over the imageName_array
for image_name, image_path in zip(imageName_array, image_paths):
    # Find the corresponding row in the DataFrame
    row = df[df.iloc[:, 0] == image_name]
    
    # Extract x, y, w, h coordinates
    x, y, w, h = row.iloc[0, 2:6] 
    
    # Map coordinates to the image path
    image_coordinates[image_path] = {'x': x, 'y': y, 'w': w, 'h': h}

# Print the image coordinates
# for image_path, coordinates in image_coordinates.items():
#     print(f"Image Path: {image_path}, Coordinates: {coordinates}")




# Path to the "Frames" folder
# frames_folder = "Frames"

# # Iterate through each key-value pair in the image_coordinates dictionary
# for image_path, coordinates in image_coordinates.items():
#     # Construct the full path to the image
#     image_file = os.path.join(frames_folder, image_path)
    
#     # Check if the image file exists
#     if os.path.exists(image_file):
#         # Read the image
#         image = cv2.imread(image_file)
        
#         # Get the center coordinates and dimensions
#         x_center, y_center = coordinates['x'], coordinates['y']
#         w, h = coordinates['w'], coordinates['h']
        
#         # Convert relative coordinates to pixel coordinates
#         image_height, image_width = image.shape[:2]
#         x1 = int((x_center - w / 2) * image_width)
#         y1 = int((y_center - h / 2) * image_height)
#         x2 = int((x_center + w / 2) * image_width)
#         y2 = int((y_center + h / 2) * image_height)
        
#         # Draw the bounding box on the image
#         color = (0, 255, 0)  # Green color
#         thickness = 2
#         cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        
#         # Show or save the modified image
#         cv2.imshow("Bounding Box", image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
        
#         # Alternatively, you can save the modified image
#         # cv2.imwrite("output_image.jpg", image)
#     else:
#         print(f"Image file '{image_file}' not found.")



# Path to the "Frames" folder
frames_folder = "Frames"

# Path to the "final_output" folder
final_output_folder = "final_output"

# Create the "final_output" folder if it doesn't exist
if not os.path.exists(final_output_folder):
    os.makedirs(final_output_folder)

# Iterate through each frame in the "Frames" folder
for frame_file in os.listdir(frames_folder):
    # Construct the full path to the frame image
    frame_path = os.path.join(frames_folder, frame_file)
    
    # Check if the frame file exists and is an image
    if os.path.isfile(frame_path) and frame_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Read the frame image
        frame = cv2.imread(frame_path)
        
        # Check if the image name matches any of the image paths in image_coordinates
        image_path_matched = False
        for image_path, coordinates in image_coordinates.items():
            if frame_file == image_path:
                # Get the bounding box coordinates
                x_center, y_center = coordinates['x'], coordinates['y']
                w, h = coordinates['w'], coordinates['h']
                
                # Convert relative coordinates to pixel coordinates
                image_height, image_width = frame.shape[:2]
                x1 = int((x_center - w / 2) * image_width)
                y1 = int((y_center - h / 2) * image_height)
                x2 = int((x_center + w / 2) * image_width)
                y2 = int((y_center + h / 2) * image_height)
                
                # Draw bounding box on the frame
                color = (0, 255, 0)  # Green color
                thickness = 2
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
                
                # Set flag indicating image path match
                image_path_matched = True
                break
        
        # Copy the modified or original frame to the "final_output" folder
        if image_path_matched:
            # Save the modified frame with bounding box
            final_frame_path = os.path.join(final_output_folder, frame_file)
            cv2.imwrite(final_frame_path, frame)
        else:
            # Copy the original frame
            final_frame_path = os.path.join(final_output_folder, frame_file)
            shutil.copy(frame_path, final_frame_path)

# Print message when processing is complete
print("Frames copied to 'final_output' folder.")
