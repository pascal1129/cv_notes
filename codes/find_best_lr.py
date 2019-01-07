# ref: https://sgugger.github.io/how-do-you-find-a-good-learning-rate.html

import os 
import time 
import json 
import torch 
import random 
import warnings
warnings.filterwarnings('ignore')
import torchvision
import numpy as np 
import pandas as pd 

from utils import *
from data import HumanDataset
from config import config
from models.model import*
from torch import nn,optim
from collections import OrderedDict
from torch.autograd import Variable
from torch.utils.data import DataLoader

import matplotlib.pyplot as plt
import math
from tqdm import tqdm 


# 1、设置随机种子
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)

# 2、设置GPU0可见，只使用一个GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
torch.backends.cudnn.benchmark = True

                                                                                                
def find_lr(init_value = 1e-8, final_value=10., beta = 0.98):
    # 1. load dataset
    all_files = pd.read_csv(config.CSV_TRAIN)
    train_data_list, _  = multilabel_stratification(all_files, test_size=0.2, random_state=42)
    train_gen = HumanDataset(train_data_list,config.train_data,mode="train")
    train_loader = DataLoader(train_gen,batch_size=config.batch_size,shuffle=True,pin_memory=True,num_workers=8)  

    # 2. get the model, and set the optimizer and criterion
    model = get_net()
    model.cuda()
    optimizer = optim.SGD(model.parameters(),lr = init_value,momentum=0.9,weight_decay=1e-4)
    criterion = nn.BCEWithLogitsLoss(opt_class_weight).cuda()

    # 3.set init value
    num = len(train_loader) - 1                             # num = samples_per_epoch / batch_size
    mult = (final_value / init_value) ** (1/num)            # init_value * (mult)**num ==> final_value

    lr = init_value
    optimizer.param_groups[0]['lr'] = lr
    avg_loss = 0.
    best_loss = 0.
    batch_num = 0
    losses = []
    log_lrs = []

    best_lr = 111

    model.train()
    model.zero_grad()
    
    for i,(images,target) in enumerate(train_loader):
        batch_num += 1

        # 0. get the loss of this batch
        images = images.cuda(non_blocking=True)
        target = torch.from_numpy(np.array(target)).float().cuda(non_blocking=True)
        output = model(images)
        loss = criterion(output,target)

        # 1. Compute the smoothed loss
        avg_loss = beta * avg_loss + (1-beta) *loss.item()
        smoothed_loss = avg_loss / (1 - beta**batch_num)

        # 2. Stop if the loss is exploding
        if batch_num > 1 and smoothed_loss > 4 * best_loss:
            return log_lrs, losses
        # 3. Record the best loss
        if smoothed_loss < best_loss or batch_num==1:
            best_loss = smoothed_loss
            best_lr = lr
        # 4. Store the values
        losses.append(smoothed_loss)
        log_lrs.append(math.log10(lr))


        # 5. Do the SGD step
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # 6. Update the lr for the next step
        lr *= mult
        optimizer.param_groups[0]['lr'] = lr

        print('%d:  factor:%.3f  smoothed_loss:%f best_loss:%f lr:%f best_lr: %f'%(i,smoothed_loss/best_loss, smoothed_loss, best_loss, lr, best_lr))
    return log_lrs, losses
    
if __name__ == "__main__":
    logs,losses = find_lr()
    plt.plot(logs[10:-5],losses[10:-5])
    plt.show()