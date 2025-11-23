'''
常见导入方式：
    import yyy：直接导入整个模块
    from xxx import yyy：从模块中导入特定对象
    import xxx as xx：给导入模块起别名
    from xxx import *：导入模块所有内容
    import xxx,yyy：同时导入多个模块

as的作用：
    为导入模块创建别名，防止命名冲突
    示例：import aa as AA后只能使用AA.age，原aa.age不可用
    原理：
        import执行两个操作：
            加载模块文件
            在当前模块创建变量指向加载的模块

搜索机制：
    通过sys.path列表确定搜索路径顺序
    列表顺序代表解释器搜索模块的优先级
    搜索到第一个匹配模块后即停止
    全部路径未找到则报ImportError
    默认路径：
        空字符串''表示当前目录
        Python安装目录
        site-packages第三方库目录
        用户自定义路径

动态添加路径：
    sys.path.append('/path')：添加到搜索路径末尾
    sys.path.insert(0,'/path')：插入到搜索路径开头
    应用场景：当模块安装但无法导入时使用
    注意事项：
        insert(0)可确保优先搜索指定路径
        临时修改只在当前会话有效
        永久修改需配置环境变量或修改Python路径配置

模块重载问题：
    Python默认只导入模块一次
    修改模块代码后，原进程不会自动更新
    重复import无效
    解决方案：
        使用from imp import reload
        语法：reload(module_name)
    限制条件：
        必须先成功导入模块
        仅适用于import方式导入的模块
        不适用于from...import方式
    应用场景：
        服务器程序运行时修改代码
        开发环境热更新
        动态加载配置
        
'''