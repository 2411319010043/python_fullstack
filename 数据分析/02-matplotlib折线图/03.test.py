from matplotlib import pyplot as plt
from matplotlib import font_manager

x = range(11,31)
y1 = [1,0,1,1,2,4,3,2,3,4,4,5,6,5,4,3,3,1,1,1]
y2 = [1,0,3,1,2,2,3,3,2,1,2,1,1,1,1,1,1,1,1,1]

# 设置中文字体
my_font = font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

_xtick_labels = ['{}岁'.format(i) for i in range(11,31)]

plt.xticks(list(x), _xtick_labels, rotation= 45, fontproperties= my_font)
plt.yticks(y1)

plt.xlabel('年龄', fontproperties = my_font)
plt.ylabel('个数', fontproperties = my_font)

plt.plot(x,y1,label='自己',color='orange',linestyle=':')
plt.plot(x,y2,label='同桌',color='cyan',linestyle='-.')

# 绘制网格
plt.grid(alpha= 0.4) # 设置网格透明度

# 添加图例
plt.legend(prop = my_font)

plt.show()




