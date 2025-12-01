from matplotlib import pyplot as plt
import random
from matplotlib import font_manager

# 设置中文字体
my_font = font_manager.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

x = range(0,120)
y = [random.randint(20,35) for i in range(120)]

plt.plot(x,y)

# 调整x轴的刻度
'''[expression for item in iterable]
    expression: 对每个元素进行的操作或计算
    item: 迭代变量
    iterable: 可迭代对象（如列表、元组、范围等）'''
_xtick_labels = ['10点{}分'.format(i) for i in range(60)]  # 列表推导式
_xtick_labels += ['11点{}分'.format(i) for i in range(60)]  # 拼接列表

'''plt.xticks(ticks, labels, **kwargs)
    ticks: 刻度位置(数值坐标)
    labels: 对应位置的显示文本
    **kwargs: 其他可选参数（如旋转角度、颜色等）'''
plt.xticks(list(x)[::9], _xtick_labels[::9], rotation= 45, fontproperties= my_font)

plt.yticks(y)

# 添加描述信息
plt.xlabel('时间', fontproperties= my_font)
plt.ylabel('温度 单位(℃)', fontproperties= my_font)
plt.title('10点到12点每分钟的气温变化情况', fontproperties= my_font)

plt.show()
