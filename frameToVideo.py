# import cv2
# import os

# image_folder = 'final_output'
# video_name = 'video.avi'

# images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape

# video = cv2.VideoWriter(video_name, 0, 10, (width,height))

# for image in images:
#     video.write(cv2.imread(os.path.join(image_folder, image)))

# cv2.destroyAllWindows()
# video.release()

import cv2
import os

def sorted_frames(folder):
    frames = [f for f in os.listdir(folder) if f.startswith('frame')]
    return sorted(frames, key=lambda x: int(x[5:-4]))

def frames_to_video(input_folder, output_file, fps):
    frame_files = sorted_frames(input_folder)

    frame = cv2.imread(os.path.join(input_folder, frame_files[0]))
    frame_height, frame_width, _ = frame.shape
    frame_size = (frame_width, frame_height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    for frame_file in frame_files:
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()

# Example usage
input_folder = 'final_output'
output_file = 'output_video.mp4'
fps = 30
frames_to_video(input_folder, output_file, fps)

