class Node:  # 目录对象
    def __init__(self, name, type="dir"):  # 初始化对象:名称和类型；
        self.name = name
        self.type = type
        self.children = []  # 文件的下级目录，存储为一个列表
        self.parent = None  # 文件的上级目录

    def __repr__(self):  # 重写对象返回值为name
        return self.name


class FileSystemTree:  # 文件系统操作类
    def __init__(self):
        self.root = Node("/")  # 初始化对象：根目录路径
        self.now = self.root  # 当前对象路径，初始化为根目录

    def mkdir(self, name):  # 创建文件夹
        if name[-1] != "/":
            name += "/"
        node = Node(name)  # 创建一个文件夹对象
        self.now.children.append(node)  # 将文件夹对象存到当前文件的children里面
        node.parent = self.now  # 创建的文件夹对象的上级目录存储为当前目录

    def ls(self):
        return self.now.children  # 返回下级目录列表

    def cd(self, name):  # 只实现相对路径
        if name[-1] != "/":
            name += "/"
        for child in self.now.children:
            if child.name == name:  # 判断目录是否存在，如果存在指向对应目录对象
                self.now = child
                return
        raise ValueError("invalid dir")  # 如果不存在，报错


tree = FileSystemTree()
tree.mkdir("var/")
tree.mkdir("bin/")
tree.mkdir("usr/")
print(tree.ls())
tree.cd("bin/")
tree.mkdir("python/")
print(tree.ls())
