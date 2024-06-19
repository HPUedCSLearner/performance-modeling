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
print("[info]:", "----------------test  find_closest_number end...----------------")


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

models = ['atm', 'ocn', 'ice', 'lnd']
best_mintime_individual = [0, 346, 523, 392, 413, 16, 321, 108]

best_mintime_individual[1] = find_closest_number(kownladged_pes, best_mintime_individual[1] )
best_mintime_individual[3] = find_closest_number(kownladged_pes, best_mintime_individual[3] )
best_mintime_individual[5] = find_closest_number(kownladged_pes, best_mintime_individual[5] )
best_mintime_individual[7] = find_closest_number(kownladged_pes, best_mintime_individual[7] )


print("best_mintime_individual:", best_mintime_individual)
layout = {
    {
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
}