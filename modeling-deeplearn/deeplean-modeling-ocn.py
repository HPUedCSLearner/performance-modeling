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
y = torch.tensor([26208396035170., 14125095233571, 9499624724564, 7332661699610, 4969123787708, 3922271353408, 2678558663290, 
                        2128286801327, 1447494492105, 1119992491206,  815502882802, 788519722917,  495173769367, 408134497783])

# y = torch.tensor([8., 9, 8, 8, 8,  8, 8, 7, 8, 8, 8, 8, 8, 8])
# min_y = torch.min(y)
# max_y = torch.max(y)
# y = (y - min_y) / (max_y - min_y)
min_y, max_y, y = normalization(y)



# print('in_x.shape: ', in_x.shape)
# print('in_x.reshape(-1, 1).shape: ', in_x.reshape(-1, 1).shape)
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
print('x:\n', x)
print('x.type:\n', x.type)
print('y:\n', y)

plt.plot(x, y, "y-")
plt.scatter(x, y, c='black')
plt.show()


# batch_size = 10
# input_size = 1
# output_size = 1
num_epochs = 500
learning_rate = 0.01

# # x = torch.linspace(0, 1, batch_size).reshape(-1, 1)
# # print(x)
# # y = x ** 2 + 1
# # print(y)

model = nn.Sequential(
    # nn.Linear(1, 1),
    # nn.Sigmoid(),
    # nn.Linear(1, 1),
    # nn.Sigmoid(),
    # nn.Linear(1, 1),
    # nn.Sigmoid(),
    # nn.Linear(1, 1),
    # nn.Sigmoid(),
    # nn.Linear(1, 1)
    
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

for i in range(num_epochs):
    # print('x:', x)
    # print('x.shape: ', x.shape)
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

plt.plot(x.data, y.data, "g*")
plt.plot(x.data, model.forward(x).data, "r-")
plt.plot(x.data, abs(model.forward(x).data - y.data), "y-")
plt.show()


# 测试一个数据
# x = torch.tensor([300])
x = torch.tensor([300.])  # tensor([[0.0259]])
x = x.reshape(-1, 1)
print(model.forward(x).data)
print(de_normalization(model.forward(x).data, min_y, max_y))
print('===============================================')

# 保存模型
print('======================Test Save Model=========================')
# print(model.state_dict())
torch.save(model.state_dict(), 'model.ocn.pt')

# # 加载模型
# # new_net = model.load_state_dict(torch.load('model.pt'))
# # new_net = torch.load('model.pt')
# # new_net.eval()

# new_net = model.load_state_dict(torch.load('model.pt'))
# # 使用模型
# # print(new_net.forward(x).data)
# print(new_net(x))


# 把min_y, max_y写道文件里，为了在调优的时候，能够还原数据
# 使用真实的数据进行的调优

## step1: 读取文件
filename = "models_max_min.json"

if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('{}')
    
with open(filename, 'r') as file:
    file_content = file.read()

## step2: 读取文件后，转成json，写入需要的json数据 
model_min_max_val_json_data = json.loads(file_content)   
        
model_min_max_val_json_data['ocn'] = {}
model_min_max_val_json_data['ocn']['min'] = min_y.tolist()
model_min_max_val_json_data['ocn']['max'] = max_y.tolist()

# print(min_y)              # tensor(383372109773)
# print(min_y.tolist())     # 383372109773


## step3: 将 JSON 数据写回文件
with open(filename, 'w') as file:
    json.dump(model_min_max_val_json_data, file, indent=2)
    print(f"JSON 数据已成功写回文件 {filename}")