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
y = torch.tensor([6298413504., 4753988487, 2079772120, 1456997499, 950613983, 798704403, 568216873, 
                  445728349, 391681093, 266357942, 282541210, 317868333, 310957847, 296442477])

y = y / 2.1e9

print('y/2e9:', y)
# y/2e9: tensor([2.9992, 2.2638, 0.9904, 0.6938, 0.4527, 0.3803, 0.2706, 0.2123, 0.1865,
#         0.1268, 0.1345, 0.1514, 0.1481, 0.1412])



min_y, max_y, y = normalization(y)

# print('x:\n', x)
print('y-after-normal:\n', y)
# y-after-normal:
#  tensor([1.0000, 0.7440, 0.3006, 0.1974, 0.1134, 0.0883, 0.0500, 0.0297, 0.0208,
#         0.0000, 0.0027, 0.0085, 0.0074, 0.0050])
 
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
torch.save(model.state_dict(), 'model.rof.pt')


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
        
model_min_max_val_json_data['rof'] = {}
model_min_max_val_json_data['rof']['min'] = min_y.tolist()
model_min_max_val_json_data['rof']['max'] = max_y.tolist()

# print(min_y)              # tensor(383372109773)
# print(min_y.tolist())     # 383372109773


## step3: 将 JSON 数据写回文件
with open(filename, 'w') as file:
    json.dump(model_min_max_val_json_data, file, indent=2)
    print(f"JSON 数据已成功写回文件 {filename}")