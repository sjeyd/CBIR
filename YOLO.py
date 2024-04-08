from ultralytics import YOLO
import os


model = YOLO('yolov8n.pt')
def process_images_in_frames(frames_folder):
    # Get a list of all files in the folder
    files = os.listdir(frames_folder)
    # Filter out only image files
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # Loop through the image files
    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(frames_folder, image_file)
        # Process the image
        model.predict(image_path, save=True, conf=0.5, classes = 0,save_crop=True, save_txt = True,project = "output", name = "frame" )


# Example usage
frames_folder = 'Frames'
process_images_in_frames(frames_folder)

