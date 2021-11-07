from PIL import Image
import random
import numpy as np
from tqdm import tqdm


img = Image.open("Image.jpg", 'r')
pixels = list(img.getdata())

k=4
centers = []

for i in range(k):
    r_val = random.randint(0, 255)
    g_val = random.randint(0, 255)
    b_val = random.randint(0, 255)
    centers.append([r_val, g_val, b_val])
    

def distance(center):
    diff = np.array(pixels)-center
    distances = [i[0]**2+i[1]**2+i[2]**2 for i in diff]
    return distances

pixels_clusters = np.zeros(len(pixels))

def assign_pixel_clusters():
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
            
        
def find_new_centers():
    for i in range(k):
        indices = np.where(pixels_clusters==i)
        mean = np.array(pixels)[indices].mean(axis=0)
        mean = mean.astype(np.int32())
        centers[i] = mean
        
        
for itr in tqdm(range(10)):
    assign_pixel_clusters()
    find_new_centers()


def segmented_image():
    new_pixels = []
    for i in pixels_clusters:
        new_pixels.append(tuple(centers[int(i)]))
    new_image = Image.new(img.mode,img.size)
    new_image.putdata(new_pixels)
    new_image.save("result_"+str(k)+".png")

segmented_image()
