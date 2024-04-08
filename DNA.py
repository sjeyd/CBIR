import numpy as np
import cv2
import sys
import os
import pandas as pd
np.set_printoptions(threshold=sys.maxsize)


def Image2Amino(image):
    image = np.bitwise_and(image, 252)
    row, col = image.shape
    ctr = 0
    for x in range(row):
        for y in range(col):
            ch = 0
            p = image[x, y]
            if p == 0 or p == 4:
                ch = 1
            elif p == 12 or p == 8:
                ch = 2
            elif 16 <= p <= 28:
                ch = 3
            elif p == 48 or p == 52:
                ch = 4
            elif p == 56 or p == 60 or p == 44:
                ch = 23
            elif p == 32 or p == 36:
                ch = 5
            elif p == 40:
                ch = 6
            elif 64 <= p <= 76:
                ch = 7
            elif 80 <= p <= 92:
                ch = 8
            elif p == 112 or p == 116:
                ch = 9
            elif p == 124 or p == 120:
                ch = 10
            elif 96 <= p <= 108:
                ch = 11
            elif p == 192 or p == 196 or p == 204:
                ch = 12
            elif p == 200:
                ch = 23
            elif 208 <= p <= 220:
                ch = 13
            elif p == 240 or p == 244:
                ch = 14
            elif p == 248 or p == 252:
                ch = 15
            elif p == 224 or p == 228:
                ch = 16
            elif p == 232 or p == 236:
                ch = 17
            elif 128 <= p <= 140:
                ch = 18
            elif 144 <= p <= 156:
                ch = 19
            elif p == 176 or p == 180:
                ch = 20
            elif p == 184 or p == 188:
                ch = 21
            elif 160 <= p <= 172:
                ch = 22
            
            if ctr == 0:
                am = ch
            else:
                am = np.append(am, ch)
            
            ctr += 1
    
    return am


def calulate_feature_vector(arr, alpha):
    # Calculate the length of each part
    part_length = len(arr) // alpha
    
    # Initialize an empty list to store the frequency counts
    probability_counts = []
    
    # Divide the array into alpha parts and calculate probability counts for each part
    for i in range(alpha):
        start_index = i * part_length
        end_index = (i + 1) * part_length if i < alpha - 1 else None
        part = arr[start_index:end_index]
        
        # Use np.histogram with specified bins to ensure counts for all numbers from 1 to 23
        counts, _ = np.histogram(part, bins=np.arange(1, 25))
        
        # Calculate total elements in the part
        total_elements = part.size
        
        # Calculate probability for each element
        probability = counts / total_elements
        
        # Append the probabilities to the probability_counts list
        probability_counts.append(probability)
    
    # Combine all the probability arrays into a single feature vector
    feature_vector = np.concatenate(probability_counts)
    
    return feature_vector


directory = 'database_person'
files = os.listdir(directory)

for alpha in range(1,11):
    data = []
    image_counter = 0
    for file in files:
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
            if image_counter%8==0:    
                image_path = os.path.join(directory, file)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                amino_sequence = Image2Amino(image)
                feature_vector = calulate_feature_vector(amino_sequence,alpha)
                data.append([file] + feature_vector.tolist())
            image_counter+=1
    df = pd.DataFrame(data)
    output_file = os.path.join('FeatureExtraction', f'feature_vectors_alpha_{alpha}.csv')
    df.to_csv(f'feature_vectors_alpha_{alpha}.csv', index=False)    

 