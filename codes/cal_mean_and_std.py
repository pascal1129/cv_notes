# ref：https://zhuanlan.zhihu.com/p/30966663
# for https://www.kaggle.com/c/human-protein-atlas-image-classification

import pandas as pd
import numpy as np
from PIL import Image

df = pd.read_csv('../input/train.csv')
# df = df[1:10]
r = 0 # r mean
g = 0 # g mean
b = 0 # b mean
y = 0

r_2 = 0 # r^2 
g_2 = 0 # g^2
b_2 = 0 # b^2
y_2 = 0

total = 0


for i in range(len(df)):
    filename = '../input/train/' + df.Id.iloc[i]
    c_r = np.array(Image.open(filename+"_red.png")).astype(np.float32) /255.
    c_g = np.array(Image.open(filename+"_green.png")).astype(np.float32) /255.
    c_b = np.array(Image.open(filename+"_blue.png")).astype(np.float32) /255. 
    c_y = np.array(Image.open(filename+"_yellow.png")).astype(np.float32) /255. 


    total += 512*512
    
    r += c_r.sum()
    g += c_g.sum()
    b += c_b.sum()
    y += c_y.sum()

    r_2 += (c_r**2).sum()
    g_2 += (c_g**2).sum()
    b_2 += (c_b**2).sum()
    y_2 += (c_y**2).sum()
    
    print(i)

r_mean = r / total
g_mean = g / total
b_mean = b / total
y_mean = y / total

r_std = np.sqrt(r_2 / total - r_mean ** 2)
g_std = np.sqrt(g_2 / total - g_mean ** 2)
b_std = np.sqrt(b_2 / total - b_mean ** 2)
y_std = np.sqrt(y_2 / total - y_mean ** 2)

print([r_mean,g_mean,b_mean,y_mean])
print([r_std, g_std, b_std, y_std])