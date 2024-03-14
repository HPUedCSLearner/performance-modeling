import numpy as np
import os
import torch
from torch import nn
import json


model_file = "model.ice.pt"
minmaxflag = "ice"

torch.set_default_dtype(torch.float64)

def readMaxMin():
    with open('./models_max_min.json', 'r') as f:
        return json.loads(f.read())
    
minmax = readMaxMin()
# print(minmax[minmaxflag]['min'])
min = minmax[minmaxflag]['min']
max = minmax[minmaxflag]['max']

def normalization(y):
    min_y = torch.min(y)
    max_y = torch.max(y)
    return min_y, max_y, (y - min_y) / (max_y - min_y)

def de_normalization(y, min_y, max_y):
    return (max_y - min_y) * y + min_y


net = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)


net.load_state_dict(torch.load(model_file))


def getNetVal(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    print(ten)
    ten = ten.reshape(-1, 1)
    res = net.forward(ten).data
    res = res.reshape(-1)
    # print("In getNetVal: ", x, res.numpy()[0])
    return res.numpy()[0]

# 测试一个数据
pre_y = getNetVal(430)
print(pre_y)
print(de_normalization(pre_y, min, max))

# yy = de_normalization(pre_y, min, max)
# print(yy.numpy())