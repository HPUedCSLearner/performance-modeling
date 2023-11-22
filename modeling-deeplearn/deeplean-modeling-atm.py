#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from IPython import embed


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
torch.save(model.state_dict(), 'model.atm.pt')

# # 加载模型
# # new_net = model.load_state_dict(torch.load('model.pt'))
# # new_net = torch.load('model.pt')
# # new_net.eval()

# new_net = model.load_state_dict(torch.load('model.pt'))
# # 使用模型
# # print(new_net.forward(x).data)
# print(new_net(x))