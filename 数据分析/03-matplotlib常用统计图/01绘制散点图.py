from matplotlib import pyplot as plt
from matplotlib import font_manager

'''绘制北京3,10月份每天白天的最高气温散点图'''

my_font = font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

day_3 = range(1,32)
day_10 = range(51,82)
tem3 = [11,17,16,11,12,11,12,6,6,7,8,9,12,15,14,17,18,21,16,17,20,14,15,15,15,19,21,22,22,22,23]
tem10 = [26,26,28,19,21,17,16,19,18,20,20,19,22,23,17,20,21,20,22,15,11,15,5,13,17,10,11,13,12,13,6]

plt.scatter(day_3, tem3, label= '3月份')
plt.scatter(day_10, tem10, label= '10月份')

# 调整x轴刻度
_x = list(day_3) + list(day_10)
x_labels = ['3月第{}天'.format(i) for i in day_3]
x_labels += ['10月第{}天'.format(i) for i in day_3]
plt.xticks(_x[::3], x_labels[::3], rotation= 45, fontproperties= my_font)

# 添加图例
plt.legend(loc='upper left', prop=my_font)

# 添加描述信息
plt.xlabel('时间', fontproperties= my_font)
plt.ylabel('温度 单位(℃)', fontproperties= my_font)
plt.title('北京3,10月份每天白天的最高气温散点图', fontproperties= my_font)

# 展示
plt.show()