from matplotlib import pyplot as plt
from matplotlib import font_manager


interval = [0,5,10,15,20,25,30,35,40,45,60,90]  # x
width = [5,5,5,5,5,5,5,5,5,15,30,60]  # 组距
quantity = [836,2737,3723,3926,3596,1438,3273,642,824,613,215,47]  # y

# 设置x轴的刻度
_x = [i-0.5 for i in range(13)]
_xtick_labels = interval +[150]
plt.xticks(_x, _xtick_labels)

plt.bar(range(0,len(interval)),quantity,width=1)

plt.grid()
plt.show()
