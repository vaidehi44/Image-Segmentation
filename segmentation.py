from PIL import Image
import random
import numpy as np

img = Image.open("Image.jpg", 'r')
pixels = list(img.getdata())

k=4
centers = []

for i in range(k):
    r_val = random.randint(0, 255)
    g_val = random.randint(0, 255)
    b_val = random.randint(0, 255)
    centers.append([r_val, g_val, b_val])
    
def distance(center, data_pt):
    dis=0
    for i in range(3):
        diff = center[i]-data_pt[i]
        dis += diff**2

    return dis

pixels_clusters = np.zeros(len(pixels))

def assign_pixel_clusters():
    for i in range(len(pixels)):
        cluster = 0
        min_dis = distance(centers[0], pixels[i])
        for j in range(1,k):
            dis = distance(centers[j], pixels[i])
            if dis<min_dis:
                min_dis=dis
                cluster=j
        pixels_clusters[i]=cluster
        
def find_new_centers():
    for i in range(k):
        count=0
        add=np.array([0,0,0])
        for j in range(len(pixels_clusters)):
            if pixels_clusters[j]==i:
                count+=1
                add+=pixels[j]
        mean = add/count
        print(mean)
        mean = mean.astype(np.int32())
        print(mean)
        centers[i]=mean
        
for itr in range(20):
    assign_pixel_clusters()
    find_new_centers()


new_pixels = []

def segmented_image():
    for i in pixels_clusters:
        new_pixels.append(tuple(centers[int(i)]))
    new_image = Image.new(img.mode,img.size)
    new_image.putdata(new_pixels)
    new_image.save("result.png")

segmented_image()
        
