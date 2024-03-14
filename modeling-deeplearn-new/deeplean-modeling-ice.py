#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed

import json
import os

torch.set_default_dtype(torch.float64)


def normalization(y):
    min_y = torch.min(y)
    max_y = torch.max(y)
    return min_y, max_y, (y - min_y) / (max_y - min_y)

def de_normalization(y, min_y, max_y):
    return (max_y - min_y) * y + min_y
    

x = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
# y = torch.tensor([8., 16, 24, 32, 48,  64, 96, 128, 192, 256, 384, 512, 768, 1024])
y = torch.tensor([648053816836,	407723774319,287959373101,	207071072463,153187178741,121094583791,
                  96994835398, 68705395470, 51546717288, 44440623593, 32004804913, 41238061828, 21748941348, 20343976669])
y = y / 2.1e9

print('y/2e9:', y)
# y/2e9: tensor([308.5971, 194.1542, 137.1235,  98.6053,  72.9463,  57.6641,  46.1880,
#          32.7169,  24.5461,  21.1622,  15.2404,  19.6372,  10.3566,   9.6876])




min_y, max_y, y = normalization(y)

# print('x:\n', x)
print('y-after-normal:\n', y)
# y-after-normal:
#  tensor([1.0000, 0.6171, 0.4263, 0.2975, 0.2116, 0.1605, 0.1221, 0.0770, 0.0497,
#         0.0384, 0.0186, 0.0333, 0.0022, 0.0000])
 
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)

# print('x:\n', x)
print('y:\n', y)

plt.plot(x, y, "y-")
plt.scatter(x, y, c='black')
plt.show()


# # batch_size = 10
# # input_size = 1
# # output_size = 1
num_epochs = 500
learning_rate = 0.01


model = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
    
)

loss_func = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# 训练模型
for i in range(num_epochs):
    y_pred = model.forward(x)
    loss = loss_func(y_pred, y)
    optimizer.zero_grad()

    loss.backward()
    optimizer.step()
    if i % 100 == 0:
        print(f"epoch: {i}, loss: {loss}")

# plt.plot(x.data, y.data, "g*")
# plt.plot(x.data, model.forward(x).data, "r-")
plt.plot(x.data, de_normalization(y.data, min_y, max_y).data, "g*")
plt.plot(x.data, de_normalization(model.forward(x).data, min_y, max_y).data, "r-")
plt.show()



# 测试一个数据
print('==================测试一个数据=============================')      
# x = torch.tensor([300])
tensorX = torch.tensor([430.])  # tensor([[0.0095]])
tensorX = tensorX.reshape(-1, 1)
preY = model.forward(tensorX).data
print(preY)
print(de_normalization(model.forward(tensorX).data, min_y, max_y))
print('===============================================')      

# 保存模型
print('======================Test Save Model=========================')
# print(model.state_dict())
torch.save(model.state_dict(), 'model.ice.pt')


# # 把min_y, max_y写道文件里，为了在调优的时候，能够还原数据
# # 使用真实的数据进行的调优

## step1: 读取文件
filename = "models_max_min.json"

if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('{}')
    
with open(filename, 'r') as file:
    file_content = file.read()

## step2: 读取文件后，转成json，写入需要的json数据 
model_min_max_val_json_data = json.loads(file_content)   
        
model_min_max_val_json_data['ice'] = {}
model_min_max_val_json_data['ice']['min'] = min_y.tolist()
model_min_max_val_json_data['ice']['max'] = max_y.tolist()



## step3: 将 JSON 数据写回文件
with open(filename, 'w') as file:
    json.dump(model_min_max_val_json_data, file, indent=2)
    print(f"JSON 数据已成功写回文件 {filename}")