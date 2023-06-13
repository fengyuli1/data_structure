from binarySearchTree import BST
from binaryTree import BinNode


class AVL(BST):
    @staticmethod
    def balanced(node):
        """
        判断节点是否为理想平衡
        :param node:
        :return:
        """
        return node.lChild.height == node.rChild.height

    @staticmethod
    def __balFac(node):
        """
        计算节点平衡因子
        :param node:
        :return:
        """
        if not node.lChild and not node.rChild:
            height = 0
        elif not node.rChild:
            height = node.lChild.height + 1
        elif not node.lChild:
            height = -1 - node.rChild.height
        else:
            height = node.lChild.height - node.rChild.height
        return height

    def avlBalanced(self, node):
        """
        AVL树平衡条件
        :param node:
        :return:
        """
        return -2 < self.__balFac(node) < 2

    @staticmethod
    def tallerChild(node: BinNode):
        """
        返回子树高度更大的那个孩子
        :param node:
        :return:
        """
        if not node.lChild and not node.rChild:
            return None
        elif not node.rChild:
            return node.lChild
        elif not node.lChild:
            return node.rChild
        else:
            return (
                node.lChild if node.lChild.height > node.rChild.height else node.rChild
            )

    def __rotateAt(self, node: BinNode):
        """
        复衡操作
        :param node:
        :return:
        """
        node_p = node.parent  # 父亲
        node_gp = node_p.parent  # 祖父
        self._hot = node_gp.parent  # 曾祖父
        if node_gp.lChild == node_p:  # zig
            if node_p.lChild == node:  # zig-zig
                self._update_node(node_gp, node_p)  # 向上级联
                return self.connect34(
                    node,
                    node_p,
                    node_gp,
                    node.lChild,
                    node.rChild,
                    node_p.rChild,
                    node_gp.rChild,
                )
            else:  # zig-zag
                self._update_node(node_gp, node)  # 向上级联
                return self.connect34(
                    node_p,
                    node,
                    node_gp,
                    node_p.lChild,
                    node.lChild,
                    node.rChild,
                    node_gp.rChild,
                )
        else:  # zag
            if node_p.lChild == node:  # zag-zig
                self._update_node(node_gp, node)  # 向上级联
                return self.connect34(
                    node_gp,
                    node,
                    node_p,
                    node_gp.lChild,
                    node.lChild,
                    node.rChild,
                    node_p.rChild,
                )
            else:  # zag-zag
                self._update_node(node_gp, node_p)  # 向上级联
                return self.connect34(
                    node_gp,
                    node_p,
                    node,
                    node_gp.lChild,
                    node_p.lChild,
                    node.lChild,
                    node.rChild,
                )

    def connect34(
        self,
        a: BinNode,
        b: BinNode,
        c: BinNode,
        t0: BinNode,
        t1: BinNode,
        t2: BinNode,
        t3: BinNode,
    ):
        """
        3+4重构
        :param a:
        :param b:
        :param c:
        :param t0:
        :param t1:
        :param t2:
        :param t3:
        :return:
        """
        a.lChild = t0
        if t0:
            t0.parent = a
        a.rChild = t1
        if t1:
            a.rChild = t1
        self.update_height(a)
        c.lChild = t2
        if t2:
            t2.parent = c
        c.rChild = t3
        if t3:
            t3.parent = c
        self.update_height(c)
        b.lChild = a
        a.parent = b
        b.rChild = c
        c.parent = b
        self.update_height(b)
        return b  # 返回子树新的根节点

    def insert(self, val):
        """
        AVL树的插入
        :param val:
        :return:
        """
        if not self.empty():  # 如果树不存在,创建根节点
            node = BinNode(val)
            self.root = node
            return node
        node = self._find(val)  # 查找插入位置
        if node:  # 如果节点存在
            return node
        if val < self._hot.data:  # 插入节点
            node = self._hot.insert_lChild(val)
        else:
            node = self._hot.insert_rChild(val)
        self._size += 1
        g = node.parent  # g初始化为插入节点的父节点
        while g:  # 如果g节点存在
            if not self.avlBalanced(g):  # g失衡
                self.__rotateAt(
                    self.tallerChild(self.tallerChild(g))
                )  # 复衡操作，入参为子树高度更高的孙子
                break  # g复衡后，局部子树高度必然复原；其祖先高度变不会变化，故调整结束
            else:  # 否则，在依然平衡的祖先处
                self.update_height(g)  # 更新其高度（平衡性虽然不变，高度却可能改变）
                g = g.parent  # g指向父节点，进入下一次循环
        return node  # 返回新节点，至多只需一次调整

    def remove(self, val):
        """
        AVL树的删除
        :param val:
        :return:
        """
        node = self._find(val)  # 定位目标节点
        if not node:  # 如果节点不存在
            return False  # 返回
        self.removeAt(node)  # 分两大类情况实施删除
        self._size -= 1  # 更新全树规模
        g = self._hot  # g初始化为删除节点的父亲
        while g:  # 如果g节点存在
            if not self.avlBalanced(g):  # g失衡
                self.__rotateAt(
                    self.tallerChild(self.tallerChild(g))
                )  # 复衡操作，可能需要做O(logn)次调整,入参为子树高度更高的孙子
            self.update_height(g)  # 更新其高度，无论是否做过调整，全树高度均可能下降；
            g = g.parent  # g指向父节点，进入下一次循环,
        return True  # 删除成功


if __name__ == "__main__":
    tree = AVL([4, 6, 7, 9, 2, 1, 3, 5, 8])
    tree.trav_in_i1(tree.root)
    print(11111111111111111)
    tree.trav_pre_i1(tree.root)
    print(2222222222222222)
    tree.tarv_post_i1(tree.root)
    print(tree.root.height)
