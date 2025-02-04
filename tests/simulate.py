import random

cnt_f=0
cnt_m=0

times=1000000

for i in range(times):
    flag=0
    while flag<2:
        sex=random.choice(['male','female'])
        if sex =='male':
            cnt_m+=1
            flag+=1
        else:
            cnt_f+=1

print(f"男性比例为{cnt_m/times},女性比例为{cnt_f/times},男女比例为{cnt_m/cnt_f}")