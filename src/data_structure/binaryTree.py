from queue import Queue


class BinNode:
    def __init__(self, data=None):
        self.data = data
        self.lChild = None  # 左孩子
        self.rChild = None  # 右孩子
        self.parent = None  # 父节点
        self._height = self.get_height()

    @property
    def height(self):
        return self._height

    def insert_lChild(self, data):
        """
        将节点作为左孩子插入
        :param data:
        :return: 左孩子对象
        """
        self.lChild = BinNode(data)
        self.lChild.parent = self
        return self.lChild

    def insert_rChild(self, data):
        """
        将节点作为右孩子插入
        :param data:
        :return: 右孩子对象
        """
        self.rChild = BinNode(data)
        self.rChild.parent = self
        return self.rChild

    def _size(self):
        """
        子树规模
        :return: 子树规模
        递归计算孩子节点子树规模，时间复杂度O(n)
        """
        s = 1
        if self.lChild:
            s += self.lChild._size()
        if self.rChild:
            s += self.rChild._size()
        return s

    def get_height(self):
        if not self.data:
            self._height = -1
        elif not self.lChild and not self.rChild:
            self._height = 0
        elif not self.rChild:
            self._height = 1 + self.lChild.height
        elif not self.lChild:
            self._height = 1 + self.rChild.height
        else:
            self._height = (
                1 + self.lChild.height
                if self.lChild.height > self.rChild.height
                else 1 + self.rChild.height
            )
        return self._height


class BinTree:
    def __init__(self):
        self._size = 0  # 整颗树的规模
        self.__root = None

    @staticmethod
    def update_height(node):
        """
        更新节点高度
        :param node:
        :return:
        时间复杂度O(1)
        """
        return node.get_height()

    def update_height_above(self, node):
        """
        更新节点及节点历代祖先高度
        :param node:
        :return:
        时间复杂度O(n),n=节点深度
        """
        while node:
            before_height = node.height
            after_height = self.update_height(node)
            if before_height == after_height:
                break
            node = node.parent

    def size(self):
        """
        规模
        :return:
        """
        return self._size

    def empty(self):
        """
        判空
        :return:
        """
        return True if self.__root else False

    @property
    def root(self):
        """
        树根
        :return: 树根
        """
        return self.__root

    @root.setter
    def root(self, node):
        self.__root = node
        self._size += 1

    def insert_child(self, node, data):
        """
        插入操作
        :param node:
        :param data:
        :return:
        """
        if data < node.data:  # 插入值小于当前节点
            node.insert_lChild(data)  # 插入左孩子
        else:  # 否则
            node.insert_rChild(data)  # 插入右孩子
        self._size += 1  # 规模+1
        self.update_height_above(node)  # 更新全树高度

    def insert_lChild(self, node, data):
        """
        插入左孩子
        :param node:
        :param data:
        :return:
        """
        self._size += 1
        node.insert_lChild(data)
        self.update_height_above(node)
        return node.lChild

    def insert_rChild(self, node, data):
        """
        插入右孩子
        :param node:
        :param data:
        :return:
        """
        self._size += 1
        node.insert_rChild(data)
        self.update_height_above(node)
        return node.rChild

    @staticmethod
    def _attach_as_lChild(node_p: BinNode, node: BinNode):
        """
        连接两个节点，node为node_p的左孩子
        :param node_p:
        :param node:
        :return:
        """
        node_p.lChild = node
        if node:
            node.parent = node_p

    @staticmethod
    def _attach_as_rChild(node_p: BinNode, node: BinNode):
        """
        连接两个节点，node为node_p的右孩子
        :param node_p:
        :param node:
        :return:
        """
        node_p.rChild = node
        if node:
            node.parent = node_p

    def tarverse(self, node):
        """
        先序遍历，递归实现
        :param node:
        :return:
        """
        if not node:
            return
        print(node.data)
        self.tarverse(node.lChild)
        self.tarverse(node.rChild)

    @staticmethod
    def trav_pre_i1(node):
        """
        先序遍历,迭代实现1
        :param node:
        :return:
        """
        s = list()  # 起到栈的作用
        if node:
            s.append(node)  # 根节点入栈
        while s:  # 在栈变空前反复循环
            x = s.pop()  # 弹出栈首
            print(x.data)  # 访问当前节点
            if x.rChild:  # 右孩子先入后出
                s.append(x.rChild)
            if x.lChild:  # 左孩子后入先出
                s.append(x.lChild)

    @staticmethod
    def visit_along_left_branch(node, stack):
        """
        先序遍历迭代2历程，访问node的左侧链，右子树入栈缓存
        不需要额外判断右子树是否为空，空的情况直接空执行一次
        :param
            node: 初始节点
            stack: 栈
        :return:
        时间复杂度O(1)
        """
        while node:  # 反复地
            print(node.data)  # 访问当前节点
            stack.append(node.rChild)  # 右孩子(右子树)入栈（将来逆序出栈）
            node = node.lChild  # 沿左侧链下行

    def trav_pre_i2(self, node):
        """
        先序遍历,迭代实现2,主程序
        :param node:
        :return:
        时间复杂度O(n)
        """
        s = list()  # 辅助栈
        while True:  # 以（右）子树为单位，逐批访问节点
            self.visit_along_left_branch(node, s)  # 访问子树x的左侧链，右子树入栈缓存
            if not s:  # 栈空即退出
                break
            node = s.pop()  # 弹出下一子树的根

    @staticmethod
    def go_along_left_branch(node, stack):
        """
        中序遍历迭代历程，访问node的左侧链，根节点入栈
        不需要额外判断右子树是否为空，空的情况直接空执行一次
        :param
            node: 初始节点
            stack: 栈
        :return:
        时间复杂度O(1)
        """
        while node:  # 反复地
            stack.append(node)  # 入栈
            node = node.lChild  # 沿左侧链下行

    def trav_in_i1(self, node):
        """
        中序遍历,迭代实现,主程序
        :param node:
        :return:
        """
        s = list()  # 辅助栈
        while True:
            self.go_along_left_branch(node, s)  # 从当前节点出发，逐批入栈
            if not s:
                break  # 栈空即退出
            node = s.pop()  # 左子树或为空，或已遍历（等效于空），故可以
            print(node.data)  # 立即访问该节点
            node = node.rChild  # 指向右子树，可能为空，空跑一轮历程

    @staticmethod
    def goto_hlvfl(stack):
        """
        后续遍历迭代历程
        :param stack:
        :return:
        """
        node = stack[-1]
        while node:  # 自顶向下，反复检查栈顶
            if node.lChild:  # 尽可能向左
                if node.rChild:  # 如果有右孩子
                    stack.append(node.rChild)  # 右孩子先入栈
                stack.append(node.lChild)  # 然后左孩子入栈
            else:  # 如果没有左孩子
                stack.append(node.rChild)  # 右孩子入栈
            node = stack[-1]  # node指向栈顶
        stack.pop()  # 弹出栈顶的空节点

    def tarv_post_i1(self, node=None):
        """
        后序遍历，主程序
        :param node:
        :return:
        """
        s = list()  # 辅助栈
        if node:
            s.append(node)  # 根节点入栈
        while s:
            if s[-1] != node.parent:  # 如果栈顶非当前节点的父节点，则必为其右兄，此时需
                self.goto_hlvfl(s)  # 在以其右兄为根的子树中，找到HLVFL
            node = s.pop()  # 弹出栈顶
            print(node.data)  # 访问该节点

    def trav_level(self, node):
        """
        层次遍历
        :param node:
        :return:
        """
        x = Queue()  # 引入辅助队列
        x.put(node)  # 根节点入队列
        while not x.empty():  # 在队列空之前，反复迭代
            node = x.get()  # 取出队首节点
            print(node.data)  # 访问之
            if node.lChild:
                x.put(node.lChild)  # 左孩子入队
            if node.rChild:
                x.put(node.rChild)  # 右孩子入队

    def succ(self, node):
        """
        获取目标节点在中序遍历下的直接后继
        :param node:
        :return:
        """
        node = node.rChild  # 定位到目标节点的右子树
        while node.lChild:  # 如果有左孩子
            node = node.lChild  # 深入左孩子继续搜索
        return node


if __name__ == "__main__":
    a = BinNode("a")
    bin_tree = BinTree()
    print(bin_tree._size())
    bin_tree.root = a
    b = bin_tree.insert_lChild(a, "b")
    c = bin_tree.insert_rChild(a, "c")
    d = bin_tree.insert_lChild(c, "d")
    e = bin_tree.insert_rChild(d, "e")
    f = bin_tree.insert_rChild(c, "f")
    g = bin_tree.insert_lChild(f, "g")
    bin_tree.trav_level(a)
