import numpy as np
import os
import torch
from torch import nn

torch.set_default_dtype(torch.float64)


def normalization(y):
    min_y = torch.min(y)
    max_y = torch.max(y)
    return min_y, max_y, (y - min_y) / (max_y - min_y)

def de_normalization(y, min_y, max_y):
    return (max_y - min_y) * y + min_y


    
x = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
y = torch.tensor([21574682170053,	10871091037222,	7229198685780,	5532881759770,	3760004748574,	2862789605369,	2014817236926,	1631597316073,	
1083329794043,	848300420078,	612215782404,	628790336252,	405035379070,	383372109773])


min_y, max_y, y = normalization(y)


net = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)


net.load_state_dict(torch.load('model.atm.pt'))


# 放大因子： amplify factor
amplification_factor = 1

def getNetVal(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net.forward(ten).data
    res = res.reshape(-1)
    print("In getNetVal: ", x, res.numpy()[0] * amplification_factor)
    return res.numpy()[0] * amplification_factor

# 测试一个数据
pre_y = getNetVal(8)
print(pre_y)
print(de_normalization(pre_y, min_y, max_y))