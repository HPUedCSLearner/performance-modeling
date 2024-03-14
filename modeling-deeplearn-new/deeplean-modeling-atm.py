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
y = torch.tensor([21574682170053,	10871091037222,	7229198685780,	5532881759770,	3760004748574,	2862789605369,	2014817236926,	1631597316073,	
1083329794043,	848300420078,	612215782404,	628790336252,	405035379070,	383372109773])

y = y / 2.1e9

print('y/2e9:', y)
# y/2e9: tensor([10273.6582,  5176.7100,  3442.4756,  2634.7056,  1790.4785,  1363.2331,
#           959.4368,   776.9511,   515.8713,   403.9526,   291.5313,   299.4240,
#           192.8740,   182.5581])


min_y, max_y, y = normalization(y)

# print('x:\n', x)
print('y-after-normal:\n', y)
# y-after-normal:
#  tensor([1.0000, 0.4949, 0.3230, 0.2430, 0.1593, 0.1170, 0.0770, 0.0589, 0.0330,
#         0.0219, 0.0108, 0.0116, 0.0010, 0.0000])
 
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
torch.save(model.state_dict(), 'model.atm.pt')


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
        
model_min_max_val_json_data['atm'] = {}
model_min_max_val_json_data['atm']['min'] = min_y.tolist()
model_min_max_val_json_data['atm']['max'] = max_y.tolist()

# print(min_y)              # tensor(383372109773)
# print(min_y.tolist())     # 383372109773


## step3: 将 JSON 数据写回文件
with open(filename, 'w') as file:
    json.dump(model_min_max_val_json_data, file, indent=2)
    print(f"JSON 数据已成功写回文件 {filename}")