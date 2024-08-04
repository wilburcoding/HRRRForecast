import os
import imageio
path = "./output"
dir_list = os.listdir(path)
images = []
for filename in dir_list:
    images.append(imageio.imread("./output/" + filename))
imageio.mimsave('output.gif', images, duration=0.8)
