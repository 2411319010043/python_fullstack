'''
示例：通过KNN算法实现 鸢尾花的 分类操作。

回顾：机器学习的研发流程
    1. 加载数据
    2. 数据的预处理
    3. 特征工程(特征提取，特征的预处理....)
    4. 模型训练
    5. 模型评估
    6. 模型预测

'''

# 导包
from sklearn.datasets import load_iris  # 加载鸢尾花测试集
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split  # 分割训练集和测试集
from sklearn.preprocessing import StandardScaler  # 数据标准化
from sklearn.neighbors import KNeighborsClassifier  # KNN算法 分类对象
from sklearn.metrics import accuracy_score  # 模型评估的，计算模型预测的准确率

# 1. 定义函数，加载鸢尾花数据集，并查看数据集
def dm01_load_iris():
    # 1. 加载鸢尾花数据集
    iris_data = load_iris()
    # 2. 查看数据集
    print('数据集：\n', iris_data)  # 字典形态
    # print(f'数据集的类型：\n{type(iris_data)}')  # <class 'sklearn.utils._bunch.Bunch'>
    # 3. 查看数据集所有的键
    print(f'数据集所有的键：{iris_data.keys()}')
    # 4. 查看数据集的键对应的值
    print(f'数据集所有的值：{iris_data.data[:5]}')  # 有150条数据，每条数据有四个特征，只看前5条
    # 5. 查看数据集的标签
    print(f'数据集所对应的标签：{iris_data.target[:5]}') 
    # 6. 查看数据集的标签对应的名称
    print(f'数据集所对应的标签对应的名称：{iris_data.target_names[:5]}')  # ['setosa' 'versicolor' 'virginica']
    # 7. 查看数据集的特征对应的名称
    print(f'数据集特征对应的名称：{iris_data.feature_names[:5]}')

# 2. 定义函数，绘制数据集的散点图
def dm02_show_iris():
    # 1. 加载数据集
    iris_data = load_iris()
    # 2. 把鸢尾花数据集封装成 DataFrame对象
    iris_df = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
    # 3. 给df对象新增一列 ---> 标签列
    iris_df['lable'] = iris_data.target
    print(iris_df)
    # 4. 通过 Seaborn绘制散点图
    # 参1：数据集，参2：x轴，参3：y轴，参4：分组字段，参5：是否显式拟合回归线
    sns.lmplot(data=iris_df, x= 'sepal length (cm)', y='sepal width (cm)', hue='lable', fit_reg=False)
    # 5. 设置标题,显式
    plt.title('iris data')
    plt.tight_layout()  # 自动调整子图参数，使整个图像的边界与子图匹配
    plt.show()

# 3. 定义函数，切分训练集和测试集
def dm03_split_train_test():
    # 1. 加载数据集
    iris_data = load_iris()
    # 2. 数据的预处理：从150个特征和标签中，按照 8：2的比例，切分训练集和测试集
    # 参1：特征，参2：标签，参3：测试集的占比，参4：随机种子
    # 返回值：训练集的特征数据，测试集的特征数据，训练集的标签数据，测试集的标签数据
    x_train, x_test, y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.2,random_state=23)
    # 3. 打印切割后的结果
    print(f'训练集的特征：{x_train}，个数：{len(x_train)}')
    print(f'训练集的标签：{y_train}，个数：{len(y_train)}')
    print(f'测试集的特征：{x_test}，个数：{len(x_test)}')
    print(f'测试集的标签：{y_test}，个数：{len(y_test)}')

# 4. 定义函数，实现鸢尾花完整案例--->加载数据，数据预处理，特征工程，模型训练，模型评估，模型预测
def dm04_iris_evaluate_test():
    # 1. 加载数据集
    iris_data = load_iris()
    # 2. 数据的预处理，这里是150条数据，按照 8：2的比例，切分训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.2, random_state=23)
    # 3. 特征工程
    # 思考1：特征提取：因为源数据只有4个特征列，且都是我们用的，所以这里无需做特征提取
    # 思考2：特征预处理：因为源数据的4列特征差值不大，所以我们无需做特征预处理，但是，加入特征预处理会让我们的代码更完善，所以加入
        # 3.1 创建标准化对象
    transfer = StandardScaler()
        # 3.2 对特征列进行标准化，即：x_train:训练集的特征数据，x_test:测试集的特征数据
        # fit_transform: 兼具fit和transform的功能，即：训练，转换，该函数适用于：第一次进行标准化的时候使用，一般用于处理：训练集
    x_train = transfer.fit_transform(x_train)
        # transform: 只有转换，该函数适用于：重复进行标准化动作时使用，一般用于对测试集进行标准化
    x_test = transfer.transform(x_test)
    # 4. 模型训练
        # 4.1 创建模型对象
    estimator = KNeighborsClassifier(n_neighbors=3)
        # 4.2 具体的训练模型的动作
    estimator.fit(x_train, y_train)  # 传入训练集的特征，训练集的标签
    # 5. 模型预测
        # 场景1：对刚才切分的
    # 6. 模型评估

# 5. 测试
if __name__ == '__main__':
    dm01_load_iris()
    dm02_show_iris()
    dm03_split_train_test()
    dm04_iris_evaluate_test()