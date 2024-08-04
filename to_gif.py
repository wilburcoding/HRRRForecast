import os
import imageio
path = "./output"
dir_list = os.listdir(path)
print("Gif Creator")
ms = int(input("Delay (ms):"))
images = []
for filename in dir_list:
    images.append(imageio.imread("./output/" + filename))
imageio.mimsave('output.gif', images, duration=float(ms/1000))
