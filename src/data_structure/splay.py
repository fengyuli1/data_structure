from binarySearchTree import BST
from binaryTree import BinNode


class Splay(BST):
    def _splay(self, node):
        """
        伸展算法
        :param node:
        :return:
        """
        while node.parent and node.parent.parent:  # 如果父亲和祖父存在
            node_p = node.parent  # 父亲
            node_gp = node_p.parent  # 祖父
            self._hot = node_gp.parent  # 曾祖父，可能不存在
            if node_gp.lChild == node_p:  # zig
                if node_p.lChild == node:  # zig-zig
                    self._attach_as_lChild(node_gp, node_p.rChild)
                    self._attach_as_lChild(node_p, node.rChild)
                    self._attach_as_rChild(node_p, node_gp)
                    self._attach_as_rChild(node, node_p)
                else:  # zig-zag
                    self._attach_as_rChild(node_p, node.lChild)
                    self._attach_as_lChild(node_gp, node.rChild)
                    self._attach_as_rChild(node, node_p)
                    self._attach_as_lChild(node, node_gp)
            else:  # zag
                if node_p.lChild == node:  # zag-zig
                    self._attach_as_rChild(node_gp, node.lChild)
                    self._attach_as_lChild(node_p, node.rChild)
                    self._attach_as_rChild(node, node_gp)
                    self._attach_as_lChild(node, node_p)
                else:  # zag-zag
                    self._attach_as_rChild(node_gp, node_p.lChild)
                    self._attach_as_rChild(node_p, node.lChild)
                    self._attach_as_lChild(node_p, node_gp)
                    self._attach_as_lChild(node, node_p)
            self._update_node(node_gp, node)  # 向上级联,此时node为子树树根
            self.update_height(node_gp)  # 更新高度
            self.update_height(node_p)  # 更新高度
            self.update_height(node)  # 更新高度
        if node.parent:  # 双层伸展结束，如果父节点不为空，则需要进行一次单旋
            node_p = node.parent
            if node_p.lChild == node:  # zig
                self._attach_as_lChild(node_p, node.rChild)
                self._attach_as_rChild(node, node_p)
            else:  # zag
                self._attach_as_rChild(node_p, node.lChild)
                self._attach_as_lChild(node, node_p)
            self.update_height(node_p)  # 更新高度
            self.update_height(node)  # 更新高度
            node.parent = None
            self.root = node
        return node

    def search(self, val):
        pass

    def insert(self, val):
        pass

    def remove(self, val):
        pass
