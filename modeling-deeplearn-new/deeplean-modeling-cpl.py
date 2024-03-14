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
y = torch.tensor([165924998182., 76086393457, 82838387355, 44239395590, 71117989367, 83774676407, 140251432564, 
                  62644943795, 47400225387, 16804301908, 27224073729, 39385325952, 37521948660, 16174610721])

y = y / 2.1e9

print('y/2e9:', y)
# y/2e9: tensor([79.0119, 36.2316, 39.4469, 21.0664, 33.8657, 39.8927, 66.7864, 29.8309,
#         22.5715,  8.0020, 12.9638, 18.7549, 17.8676,  7.7022])
# y-after-normal:
#  tensor([1.0000, 0.4001, 0.4452, 0.1874, 0.3669, 0.4514, 0.8286, 0.3103, 0.2085,
#         0.0042, 0.0738, 0.1550, 0.1426, 0.0000])


min_y, max_y, y = normalization(y)

# print('x:\n', x)
print('y-after-normal:\n', y)
# y-after-normal:
#  tensor([1.0000, 0.4001, 0.4452, 0.1874, 0.3669, 0.4514, 0.8286, 0.3103, 0.2085,
#         0.0042, 0.0738, 0.1550, 0.1426, 0.0000])
 
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
num_epochs = 100
learning_rate = 0.01

# # # x = torch.linspace(0, 1, batch_size).reshape(-1, 1)
# # # print(x)
# # # y = x ** 2 + 1
# # # print(y)

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

# plt.plot(x.data, y.data, "g*")
# plt.plot(x.data, model.forward(x).data, "r-")
# plt.plot(x.data, abs(model.forward(x).data - y.data), "y-")
# plt.show()

#     ten = ten.reshape(-1, 1)
#     res = net.forward(ten).data
#     res = res.reshape(-1)
#     print("In getNetVal: ", x, res.numpy()[0])
#     return res.numpy()[0]

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
torch.save(model.state_dict(), 'model.cpl.pt')


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
        
model_min_max_val_json_data['cpl'] = {}
model_min_max_val_json_data['cpl']['min'] = min_y.tolist()
model_min_max_val_json_data['cpl']['max'] = max_y.tolist()

# print(min_y)              # tensor(383372109773)
# print(min_y.tolist())     # 383372109773


## step3: 将 JSON 数据写回文件
with open(filename, 'w') as file:
    json.dump(model_min_max_val_json_data, file, indent=2)
    print(f"JSON 数据已成功写回文件 {filename}")