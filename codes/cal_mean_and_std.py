# ref：https://zhuanlan.zhihu.com/p/30966663
# for https://www.kaggle.com/c/human-protein-atlas-image-classification

import numpy as np
import os
from PIL import Image

r = 0 # r mean
g = 0 # g mean
b = 0 # b mean

r_2 = 0 # r^2 
g_2 = 0 # g^2
b_2 = 0 # b^2

total = 0

root_dir = './image'
im_names = os.listdir(root_dir)

for i,name in enumerate(im_names):
    im_path = os.path.join(root_dir, name)
    img = np.array(Image.open(im_path))
    img = img.astype('float32') / 255.
    total += img.shape[0] * img.shape[1]
    
    r += img[:, :, 0].sum()
    g += img[:, :, 1].sum()
    b += img[:, :, 2].sum()
    
    r_2 += (img[:, :, 0]**2).sum()
    g_2 += (img[:, :, 1]**2).sum()
    b_2 += (img[:, :, 2]**2).sum()

    print(i)

r_mean = r / total
g_mean = g / total
b_mean = b / total

r_var = r_2 / total - r_mean ** 2
g_var = g_2 / total - g_mean ** 2
b_var = b_2 / total - b_mean ** 2

r_std = r_var ** 0.5
g_std = g_var ** 0.5
b_std = b_var ** 0.5

print(r_mean, g_mean, b_mean)
print(r_std, g_std, b_std)


""" Reference:Imagenet

    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
"""