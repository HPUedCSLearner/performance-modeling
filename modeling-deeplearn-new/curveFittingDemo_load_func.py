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
    
################################################################
#                                                              #
# 对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致   #
#                                                              #
################################################################


# ==============这个在使用模型的时候，不是必要的=====================
# num_epochs = 500
# learning_rate = 0.01


# ==============这个在使用模型的时候，这个必须对应上保存的模型数据=====================
net1 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

net2 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

net3 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

net4 = nn.Sequential(
    nn.Linear(1, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 10),
    nn.Sigmoid(),
    nn.Linear(10, 1)
)

# ==============这个在使用模型的时候，不是必要的=====================
# loss_func = torch.nn.MSELoss()
# optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)


#=#=#==#=#==#=#==#=#=对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致=#=#==#=#==#=#==#=#==#=#==#=#=
# 加载模型 
net1.load_state_dict(torch.load('model.atm.pt'))
net2.load_state_dict(torch.load('model.lnd.pt'))
net3.load_state_dict(torch.load('model.ice.pt'))
net4.load_state_dict(torch.load('model.ocn.pt'))

# 测试一个数据
# x = torch.tensor([300])
# x = torch.tensor([300.])
# x = x.reshape(-1, 1)
# print(net.forward(x).data)
# print('===============================================')

# 保存模型
# print('======================Test Save Model=========================')
# # print(model.state_dict())
# torch.save(model.state_dict(), 'model.pt')


# #=#=#==#=#==#=#==#=#=对于加载模型，只需要模型网格 和 所保存的 模型参数的key-val 一致=#=#==#=#==#=#==#=#==#=#==#=#=
# # 加载模型 
# net.load_state_dict(torch.load('model.pt'))

# # 使用模型
# print('======================Test Use Model=========================')
# print(net.forward(x).data) # tensor([[0.0259]])
# # print(new_net.forward(x).data) # error: -> '_IncompatibleKeys' object has no attribute 'forward'

# 放大因子： amplify factor
amplification_factor = 1e4

def getNet1Val(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net1.forward(ten).data
    res = res.reshape(-1)
    print("In getNet1Val: ", x, res.numpy()[0] * amplification_factor)
    return res.numpy()[0] * amplification_factor

def getNet2Val(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net2.forward(ten).data
    res = res.reshape(-1)
    print("In getNet2Val: ", x, res.numpy()[0] * amplification_factor)
    return res.numpy()[0] * amplification_factor

def getNet3Val(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net3.forward(ten).data
    res = res.reshape(-1)
    print("In getNet3Val: ", x, res.numpy()[0] * amplification_factor)
    return res.numpy()[0] * amplification_factor

def getNet4Val(x):
    ten = torch.as_tensor(x, dtype=torch.float64)
    ten = ten.reshape(-1, 1)
    res = net4.forward(ten).data
    res = res.reshape(-1)
    print("In getNet3Val: ", x, res.numpy()[0] * amplification_factor)
    return res.numpy()[0] * amplification_factor


def target(x):
    return getNet1Val(x[0]) + getNet2Val(x[1])  + getNet2Val(x[2])  + getNet2Val(x[3])


print('======================Test Use minimize with Net=========================')
from scipy.optimize import minimize
import numpy as np

# ======================================================================
# 设置初始猜测值
# x0 = np.asarray(1.5)
# x0 = np.asarray(0.2)
# x0 = np.asarray(100)
# x0 = np.asarray(400)
# x0 = np.asarray(250)

# x0 = np.asanyarray((0.5, 0.5, 0.5, 0.5))
# x0 = np.asanyarray((500, 500, 500, 500))
x0 = np.asanyarray((5000, 5000, 5000, 5000))



#设置限制条件
def con(args):
    # 约束条件 分为eq 和ineq
    # eq表示 函数结果等于0 ； ineq 表示 表达式大于等于0  
    x0bound, x1bound, x2bound, x3bound = args
    x1min, x1max = x0bound
    x2min, x2max = x1bound
    x3min, x3max = x2bound
    x4min, x4max = x3bound
    # x1min, x1max, x2min, x2max, x3min, x3max, x4min, x4max = args
    cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - x1min},
            {'type': 'ineq', 'fun': lambda x: -x[0] + x1max},
            {'type': 'ineq', 'fun': lambda x:  x[1] - x2min},
            {'type': 'ineq', 'fun': lambda x: -x[1] + x2max},
            {'type': 'ineq', 'fun': lambda x:  x[2] - x3min},
            {'type': 'ineq', 'fun': lambda x: -x[2] + x3max},
            {'type': 'ineq', 'fun': lambda x:  x[3] - x4min},
            {'type': 'ineq', 'fun': lambda x: -x[3] + x4max}
            )
    return cons


# 设置参数范围/约束条件
# bound_args = (200, 1024,    200, 1000,  200, 1024,   200, 1024)  # x1min, x1max, x2min, x2max, x3min, x3max, x4min, x4max
bound_args = ((200, 1024), (200, 1000), (200, 1024), (200, 1300))  # x1min, x1max, x2min, x2max, x3min, x3max, x4min, x4max
cons = con(bound_args)


# ======================================================================
# res = minimize(func(net), x0, method='SLSQP', constraints=my_cons)
# res = minimize(getNetVal, x0, method='SLSQP', bounds=my_bnds)

# res = minimize(target, x0, method='SLSQP', bounds=my_bnds)
res = minimize(target, x0, method='SLSQP', constraints=cons)

print(res.fun)
print(res.success)
print(res.x)