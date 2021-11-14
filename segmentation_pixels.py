from PIL import Image
import random
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


img = Image.open("Image.jpg", 'r')
pixels = list(img.getdata())

def initialize_centers(k):
    centers = []
    for i in range(k):
        r_val = random.randint(0, 255)
        g_val = random.randint(0, 255)
        b_val = random.randint(0, 255)
        centers.append([r_val, g_val, b_val])
    return centers
        

def distance(center):
    diff = np.array(pixels)-center
    distances = [i[0]**2+i[1]**2+i[2]**2 for i in diff]
    return distances


def assign_pixel_clusters(k, centers, pixels_clusters):
    distances = []
    for c in range(k):
       distances.append(distance(centers[c]))
    for i in range(len(pixels)):
        cluster = 0
        min_dis = distances[0][i]
        for j in range(1,k):
            dist = distances[j][i]
            if dist<min_dis:
                min_dis = dist
                cluster = j
        pixels_clusters[i] = cluster
            
        
def find_new_centers(k, centers, pixels_clusters):
    for i in range(k):
        indices = np.where(pixels_clusters==i)
        mean = np.array(pixels)[indices].mean(axis=0)
        mean = mean.astype(np.int32())
        centers[i] = mean
        

def segmented_image(k):
    print("K = ",k)
    centers = initialize_centers(k)
    pixels_clusters = np.zeros(len(pixels))

    for itr in tqdm(range(10)):
        assign_pixel_clusters(k, centers, pixels_clusters)
        find_new_centers(k, centers, pixels_clusters)
    new_pixels = []
    for i in pixels_clusters:
        new_pixels.append(tuple(centers[int(i)]))
    new_image = Image.new(img.mode,img.size)
    new_image.putdata(new_pixels)
    plt.figure(figsize=(17,6))
    plt.suptitle("K-Means Clustering wrt pixel values, K=%d"%(k), fontsize=22)
    plt.subplot(1,2,1)
    plt.imshow(img)
    plt.title('Original Image', fontsize=18)
    plt.xticks([]), plt.yticks([])
    plt.subplot(1,2,2)
    plt.imshow(new_image)
    plt.title('Segmented Image', fontsize=18)
    plt.xticks([]), plt.yticks([])
    plt.show()
    
print("Segmentation using only pixel colour values as features")

segmented_image(2)
segmented_image(3)
segmented_image(5)
segmented_image(7)
segmented_image(10)


