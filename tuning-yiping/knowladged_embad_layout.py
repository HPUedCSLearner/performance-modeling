import json
import bisect
import random

pes_meta = [pow(2,i) for i in range(0, 10 + 1)]
pes_meta.insert(0, 0)
print(pes_meta)

kownladged_pes = []

# 元素中0，那么组合三次，就包含了组合两次和组合一次的结果
# 组合三次
for i in range(0, len(pes_meta)):
    for j in range(0, len(pes_meta)):
        for k in range(0, len(pes_meta)):
            kownladged_pes.append(pes_meta[i] + pes_meta[j] + pes_meta[k])

# 排序
kownladged_pes.sort()

# 去重
kownladged_pes = list(set(kownladged_pes))
kownladged_pes.sort()
print(kownladged_pes)

# 去质数
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

for pes in kownladged_pes:
    if(is_prime(pes)):
        print("[info]:", "removing ", pes)
        kownladged_pes.remove(pes)

# 移除0
kownladged_pes.remove(0)

print("[info]:", "After remove prive, and remove '0'")
print(kownladged_pes)



# -----------Test find_closest_number---------------
import bisect
# find_closest_number
def find_closest_number(sorted_list, target):
    # 找到插入位置
    pos = bisect.bisect_left(sorted_list, target)
    
    # 检查插入位置及其左右元素
    if pos == 0:
        return sorted_list[0]
    if pos == len(sorted_list):
        return sorted_list[-1]
    
    before = sorted_list[pos - 1]
    after = sorted_list[pos]
    
    # 返回最接近的元素
    if after - target < target - before:
        return after
    else:
        return before
    
print("[info]:", "----------------test  find_closest_number----------------")
num = find_closest_number(kownladged_pes, 346)
print(num)
num = find_closest_number(kownladged_pes, 500)
print(num)
num = find_closest_number(kownladged_pes, 1024)
print(num)
print("[info]:", "----------------test  find_closest_number End...----------------\n")


# /home/feng/github/performance-modeling/tuning-yiping/patterns/pattern_4.out
# best_mintime_pattern: [(1,), (2,), (3,), (4,)]
# best_mintime_time: 323.48927374303935
# best_mintime_individual: [0, 346, 523, 392, 413, 16, 321, 108]
# best_mincost_pattern: [(1,), (2,), (3,), (4,)]
# best_mincost_time: 258394.74553357004
# best_mincost_individual: [0, 280, 282, 250, 96, 38, 145, 132]
# layout execution time: 4.932739019393921 seconds
# ([0, 346, 523, 392, 413, 16, 321, 108], [0, 280, 282, 250, 96, 38, 145, 132])
# run time:  4.932823181152344 s


## 获取调优结果
models = ['atm', 'ocn', 'ice', 'lnd']
best_mintime_individual = [0, 346, 523, 392, 413, 16, 321, 108]



best_mintime_individual[1] = find_closest_number(kownladged_pes, best_mintime_individual[1] )
best_mintime_individual[3] = find_closest_number(kownladged_pes, best_mintime_individual[3] )
best_mintime_individual[5] = find_closest_number(kownladged_pes, best_mintime_individual[5] )
best_mintime_individual[7] = find_closest_number(kownladged_pes, best_mintime_individual[7] )


print("best_mintime_individual:", best_mintime_individual)
layout = {
        "atm_root": best_mintime_individual[0],
        "atm_pes": best_mintime_individual[1],
        "cpl_root": best_mintime_individual[0],
        "cpl_pes": best_mintime_individual[1],
        "oce_root": best_mintime_individual[2],
        "oce_pes": best_mintime_individual[3],
        "ice_root": best_mintime_individual[4],
        "ice_pes": best_mintime_individual[5],
        "lnd_root": best_mintime_individual[6],
        "lnd_pes": best_mintime_individual[7],
    }

j_data = json.dumps(layout, indent=4)
print(j_data)


## 获取进程布局库
def read_layout_lib(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    result = []

    for line in lines:
        # 移除两端的空白字符（如换行符）
        line = line.strip()
        # 使用 eval 将字符串解析为 Python 对象
        result.append(eval(line))

    # # 打印结果
    # for item in result:
    #     print(item)
    return result

## Test read layout lib
print("[info]:", "----------------test  layout_filename----------------")
layout_filename = 'layout_tempate.txt'
result = read_layout_lib(layout_filename)
for layout in result:
    # print(layout, "type:", type(layout))
    print(layout)
print("[info]:", "----------------test  layout_filename End...----------------\n")


class Utils:
    # 质数
    def is_prime(n):
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    # find_closest_number
    def find_closest_number(sorted_list, target):
        # 找到插入位置
        pos = bisect.bisect_left(sorted_list, target)
        
        # 检查插入位置及其左右元素
        if pos == 0:
            return sorted_list[0]
        if pos == len(sorted_list):
            return sorted_list[-1]
        
        before = sorted_list[pos - 1]
        after = sorted_list[pos]
        
        # 返回最接近的元素
        if after - target < target - before:
            return after
        else:
            return before



class Generate_Pes_Layout:
    def __init__(self,
                 utils: object = Utils(),
                 template_layout_lib:list[list] = [[0,],],
                 test_layout: list = [(2,), (1, 3, 4)],
                 modules: list = ['atm', 'ocn', 'ice', 'lnd'],
                 total_task: int = 1024,
                 tuning_result: list = [0, 346, 523, 392, 413, 16, 321, 108]):
        self.test_layout = test_layout
        self.modules = modules
        self.total_task = total_task
        self.tuning_result = tuning_result
        self.kownledged_pes = []
        self.utils = utils
    
    # 初始化数据结构
    def init(self):
        self.setup_kownledged_pes()

    # 设置知识嵌入的进程数
    def setup_kownledged_pes(self):
        pes_meta = [pow(2,i) for i in range(0, 10 + 1)]
        pes_meta.insert(0, 0)
        print(pes_meta)

        kownladged_pes = []

        
        # 元素中0，那么组合三次，就包含了组合两次和组合一次的结果
        # 组合三次
        for i in range(0, len(pes_meta)):
            for j in range(0, len(pes_meta)):
                for k in range(0, len(pes_meta)):
                    kownladged_pes.append(pes_meta[i] + pes_meta[j] + pes_meta[k])

        # 排序
        kownladged_pes.sort()

        # 去重
        kownladged_pes = list(set(kownladged_pes))
        kownladged_pes.sort()
        # print(kownladged_pes)

        # 去质数
        for pes in kownladged_pes:
            # if(self.utils.is_prime(pes)):
            if(is_prime(pes)):
                print("[info]:", "removing ", pes)
                kownladged_pes.remove(pes)

        # 移除0
        kownladged_pes.remove(0)
        self.kownledged_pes = kownladged_pes
    
    def is_layout_no_overlay(self, layout: list):
        total_len = 0
        for l in layout:
            total_len += len(l)
        if total_len < 4:
            print("ERROR: total_len < 4")
            return False
        if total_len == 4:
            return True
        if total_len > 4:
            print("Occur Overlap")
            print("the layout is: ", layout)
            print("the Overlap num is: ", total_len - len(self.modules))
            return False

     # 获取调优结果中对应模块的数据
    def get_knowledge_pes_of_tuning_result_of_modules(self):
        new_list = [self.tuning_result[i] for i in range(len(self.tuning_result)) if i % 2 != 0]
        print(self.tuning_result)
        print(new_list)
        return new_list
    
    # 使用领域知识，移除不符合的模板
    def remove_violate_knowledge_layout(self):
        print()
        # if(len(self.template_layout_lib) == 0):
        #     return True

    
    def res_layout(self):
        # 移除不符合的模板
        self.remove_violate_knowledge_layout()

        # 随机挑出一个
        # layout = random(self.template_layout_lib)
        layout = self.test_layout
        print(layout)

        #获取比例
        new_pes = self.get_knowledge_pes_of_tuning_result_of_modules()
        atm_pes = new_pes[0]
        ocn_pes = new_pes[1]
        ice_pes = new_pes[2]
        lnd_pes = new_pes[3]

        new_atm = int(self.total_task * atm_pes / (atm_pes + ocn_pes))
        ocn_pes = int(self.total_task * ocn_pes / (atm_pes + ocn_pes))
        
        #填充
        res_module_layout =  {
            "atm_root":0,
            "atm_pes": 0,
            "cpl_root":0,
            "cpl_pes": 0,
            "ocn_root":0,
            "ocn_pes": 0,
            "ice_root":0,
            "ice_pes": 0,
            "lnd_root":0,
            "lnd_pes": 0,
        }

        res_module_layout["atm_pes"] = new_atm
        res_module_layout["cpl_pes"] = new_atm
        res_module_layout["ocn_root"] = new_atm
        res_module_layout["ocn_root"] = ocn_pes
        res_module_layout["ice_pes"] = ice_pes
        res_module_layout["lnd_pes"] = lnd_pes

        print(res_module_layout)



print("[info]:", "----------------test  is_layout_no_overlay----------------")     
# layout_engin = Generate_Pes_Layout()
# layout_engin.is_layout_no_overlay(result[0])
# layout_engin.is_layout_no_overlay(result[1])
# layout_engin.is_layout_no_overlay(result[2])
# layout_engin.is_layout_no_overlay(result[3])
# layout_engin.is_layout_no_overlay(result[4])

layout_engin = Generate_Pes_Layout()

print(layout_engin.kownledged_pes)
layout_engin.init()
print(layout_engin.kownledged_pes)

for layout in result:
    layout_engin.is_layout_no_overlay(layout)

print("[info]:", "----------------test  is_layout_no_overlay End...----------------\n")


print("[info]:", "----------------test  get_knowledge_pes_of_tuning_result_of_modules----------------")     
layout_engin.get_knowledge_pes_of_tuning_result_of_modules()

print("[info]:", "----------------test  get_knowledge_pes_of_tuning_result_of_modules End...----------------\n")

print("[info]:", "----------------test  res_layout----------------")     
layout_engin.res_layout()

print("[info]:", "----------------test  res_layout End...----------------\n")
