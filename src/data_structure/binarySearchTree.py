from binaryTree import BinNode, BinTree


class BST(BinTree):
    def __init__(self, li=None):
        super().__init__()
        self._hot = None  # 目标节点的父节点
        if li:  # 传入一个列表，初始化为二叉树
            for val in li:
                self.insert(val)

    def _find(self, val):
        """
        查找具体方法，时间复杂度最多为树的高度O(h)
        :param val: 需要查找的值
        :return:
            node：查找到的节点
        """
        if not self.empty():  # 如果树不存在
            return None, None  # 返回空
        node = self.root  # 从根节点开始查找
        self._hot = node.parent  # 初始化为node的父节点
        while node:  # node存在
            if val == node.data:  # 是否是需要查找的值
                return node
            elif val < node.data:  # 比目标值大，继续查询左子树
                self._hot = node
                node = node.lChild
            else:  # 比目标值小，查询右子树
                self._hot = node
                node = node.rChild
        # 如果未查询到，那么node=None，self._hot为待插入节点位置的父节点
        return node

    def search(self, val):
        """
        查找算法
        :param val: 需要查找的值
        :return: 查找到的节点
        """
        node = self._find(val)
        return node

    def insert(self, val):
        """
        插入算法
        :param val: 待插入值
        :return: 插入或查询到的节点
        """
        if not self.empty():  # 如果树不存在,创建根节点
            node = BinNode(val)
            self.root = node
            return node
        node = self._find(val)  # 查找插入位置
        if node:  # 如果节点存在
            return node
        self.insert_child(self._hot, val)
        return node

    def remove(self, val):
        """
        删除节点接口
        :param val: 待删除的目标值
        :return:
        """
        node = self._find(val)  # 定位目标节点
        if not node:  # 如果节点不存在
            return False  # 返回
        self.removeAt(node)  # 分两大类情况实施删除
        self._size -= 1  # 更新全树规模
        self.update_height_above(self._hot)  # 更新历代祖先的高度
        return True

    def removeAt(self, node):
        """
        删除历程
        :param node:
        :return:
        """
        if not node.lChild:  # 如果待删除节点没有左孩子或者为叶子节点
            succ = node.rChild  # 删除后的孩子节点succ=待删除节点右孩子（可以为None）
            self._update_node(node, succ)  # 删除节点
        elif not node.rChild:  # 如果待删除节点没有右孩子
            succ = node.lChild  # 删除后的孩子节点succ=待删除节点左孩子
            self._update_node(node, succ)  # 删除节点
        else:  # 节点有左右孩子
            x = self.succ(node)  # x=待删除节点中序遍历的直接后继
            node.data, x.data = x.data, node.data  # 互换待删除节点与直接后继的data
            self._hot = x.parent  # _hot更新为x的父亲
            self.removeAt(x)  # 删除x

    def _update_node(self, node, succ):
        """
        更新节点关联关系，succ顶替node与self._hot进行关联
        :param node:
        :param succ:
        :return:
        """
        if not self._hot:  # 如果_hot为None，待删除节点为根节点
            self.root = succ  # 更新根节点
        else:
            if node == self._hot.lChild:  # 如果节点是父节点的左孩子
                self._hot.lChild = succ  # 父节点左孩子指向新节点
            else:  # 否则
                self._hot.rChild = succ  # 父节点右孩子指向新节点
        if succ:  # 如果succ不为None
            succ.parent = self._hot  # 更新succ的父节点为_hot


if __name__ == "__main__":
    tree = BST([4, 6, 7, 9, 2, 1, 3, 5, 8])
    tree.trav_in_i1(tree.root)
    tree.remove(4)
    tree.trav_in_i1(tree.root)
    print(tree.root.height)
