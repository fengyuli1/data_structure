from queue import Queue


class Vertex:
    """
    顶点类
    """

    def __init__(self, data):
        self.data = data  # 数据
        self.inDegree = 0  # 入度, 当前顶点与多少个顶点相连
        self.outDegree = 0  # 出度
        self.status = "UNDISCOVERED"  # 状态（三种）
        self.dTime = -1  # 时间标签
        self.fTime = -1  # 时间标签
        self.priority = "INT_MAX"  # 在遍历树中的优先级（最短通路、极短跨边等）
        self.parent = -1  # 父节点

    def show(self):
        print(f"{self.data}的状态为{self.status},dTime为{self.dTime},fTime为{self.fTime}")

    def reset(self):
        """
        恢复默认
        :return:
        """
        self.status = "UNDISCOVERED"  # 状态（三种）
        self.dTime = -1  # 时间标签
        self.fTime = -1  # 时间标签
        self.priority = "INT_MAX"  # 在遍历树中的优先级（最短通路、极短跨边等）
        self.parent = -1  # 父节点


class Edge:
    """
    边类
    """

    def __init__(self, data, weight):
        self.data = data  # 数据
        self.weight = weight  # 权重
        self.status = "UNDETERMINED"  # 类型（5种）

    def reset(self):
        """
        恢复默认值
        :return:
        """
        self.status = "UNDETERMINED"


class GraphMatrix:
    """
    邻接矩阵
    """

    def __init__(self):
        self.vertex = list()  # 顶点集
        self.edge = list()  # 边集
        self.n = len(self.vertex)  # 顶点个数
        self.e = 0  # 边数
        self.clock = 0  # 时间标签

    def thisClock(self):
        self.clock += 1
        return self.clock

    def reset(self):
        """
        恢复默认
        :return:
        """
        self.clock = 0
        for v in self.vertex:
            v.reset()
        for es in self.edge:
            for e in es:
                if e:
                    e.reset()

    def nextNbr(self, i, j):
        """
        枚举任意顶点i的所有邻接顶点
        :param i:
        :param j:
        :return:
        """
        j = j - 1
        while j > -1 and not self.edge[i][j]:  # 逆向顺序查找，O(n)
            if self.edge[i][j]:
                return j
            j = j - 1
        return j

    def firstNbr(self, i):
        """
        任意顶点i的首个邻居
        :param i:
        :return:
        """
        return self.nextNbr(i, self.n)

    def exists(self, i, j):
        """
        判断边（i, j）是否存在
        :param i:
        :param j:
        :return:
        """
        return 0 <= i < self.n and 0 <= j < self.n and self.edge[i][j]

    def edgeData(self, i, j):
        """
        边（i, j）的数据
        :param i:
        :param j:
        :return:
        """
        return self.edge[i][j].data

    def edgeWeight(self, i, j):
        """
        边（i, j）的权重
        :param i:
        :param j:
        :return:
        """
        return self.edge[i][j].weight

    def insertEdge(self, data, w, i, j):
        """
        边插入
        :param data:
        :param w:
        :param i:
        :param j:
        :return:
        """
        if self.exists(i, j):  # 忽略已有的边
            return
        self.edge[i][j] = Edge(data, w)  # 创建边
        self.e += 1  # 更新边计数
        self.vertex[i].outDegree += 1  # 更新关联顶点i的出度
        self.vertex[j].inDegree += 1  # 更新关联顶点j的入度

    def removeEdge(self, i, j):
        """
        边删除
        :param i:
        :param j:
        :return:
        """
        edge = self.edge[i][j]
        self.edge[i][j] = None
        self.e -= 1
        self.vertex[i].outDegree -= 1
        self.vertex[j].inDegree -= 1
        return edge

    def insertVertex(self, vertex):
        """
        顶点插入
        :param vertex:
        :return:
        """
        self.vertex.append(vertex)  # 插入顶点集
        self.edge.append(list([None] * self.n))  # 插入边集
        self.n += 1  # 顶点个数+1
        for i in self.edge:  # 每个顶点边+1
            i.append(None)  # 边值默认为None
        return self.n  # 返回顶点个数

    def removeVertex(self, i):
        """
        删除顶点及其关联边，返回该顶点信息
        :param i:
        :return:
        """
        for j in (0, self.n):  # 删除所有出边
            if self.exists(i, j):
                self.vertex[j].inDegree -= 1
        del self.edge[i]  # 删除第i行
        self.n -= 1  # 顶点数-1
        for j in (0, self.n):  # 删除所有入边以及第i列
            if self.exists(j, i):
                self.vertex[j].outDegree -= 1
            del self.edge[j][i]
        vertex = self.vertex[i]
        del self.vertex[i]  # 删除顶点i
        return vertex  # 返回被删除的顶点信息

    def bfs(self, i):
        """
        广度优先搜索，时间复杂度O(n+e)，e=边数
        :param i:
        :return:
        """
        q = Queue()  # 辅助队列
        self.vertex[i].status = "DISCOVERED"  # 初始化顶点i状态
        self.vertex[i].dTime = self.thisClock()  # 时间标签+1
        print(self.vertex[i].data)  # 访问该顶点
        q.put(i)  # 顶点i进队
        while not q.empty():  # 反复地
            i = q.get()  # 取出队首顶点，并
            u = self.firstNbr(i)  # 获取i的第一个邻居
            while -1 < u:  # 考察i的每一个邻居u
                if self.vertex[u].status == "UNDISCOVERED":  # 如果未被发现，则
                    self.vertex[u].status = "DISCOVERED"  # 发现该顶点，并
                    self.vertex[u].dTime = self.thisClock()  # 时间标签+1
                    print(self.vertex[u].data)  # 访问该顶点
                    q.put(u)  # 入队
                    self.edge[i][u].status = "TREE"  # 引入树边
                    self.vertex[u].parent = self.vertex[i]  # 设置i为u的父节点
                else:  # 若u已被发现，则
                    self.edge[i][u].status = "CROSS"  # （i, u）归为跨边
                u = self.nextNbr(i, u)  # 获取下一个邻居
            self.vertex[i].status = "VISITED"  # 顶点访问完毕，状态置为VISITED

    def multBFS(self):
        """
        广度优先搜索，多连通域情况，遍历所有连通域
        :return:
        """
        self.reset()
        for i in range(self.n):
            if self.vertex[i].status == "UNDISCOVERED":
                self.bfs(i)

    def dfs(self, i):
        self.vertex[i].status = "DISCOVERED"  # 初始化顶点i状态
        self.vertex[i].dTime = self.thisClock()  # 开始时间标签+1
        print(self.vertex[i].data)  # 访问该顶点
        u = self.firstNbr(i)  # 获取i的第一个邻居
        while -1 < u:  # 考察i的每一个邻居u
            if self.vertex[u].status == "UNDISCOVERED":  # u尚未发现，意味着支撑树可在此拓展
                self.edge[i][u].status = "TREE"  # 边为树边
                self.vertex[u].parent = self.vertex[i]  # 设置i为u的父节点
                self.dfs(u)  # 递归
            elif self.vertex[u].status == "DISCOVERED":  # u已被发现但尚未访问完毕，应为被后代指向的祖先
                self.edge[i][u].status = "BACKWARD"  # 边为回边
            else:  # u已访问完毕（VISITED）,视承袭关系分为前向边或跨边
                self.edge[i][u].status = (
                    "FORWARD"
                    if self.vertex[i].dTime < self.vertex[u].dTime
                    else "CROSS"
                )
            u = self.nextNbr(i, u)
        self.vertex[i].status = "VISITED"  # 顶点访问完毕，状态置为VISITED
        self.vertex[i].fTime = self.thisClock()  # 结束时间标签+1

    def multDFS(self):
        self.reset()
        for i in range(self.n):
            if self.vertex[i].status == "UNDISCOVERED":
                self.dfs(i)

    def showEdge(self):
        for edge in self.edge:
            print("=======================")
            for ed in edge:
                if ed:
                    print(ed.status)


class Graph(GraphMatrix):
    pass


if __name__ == "__main__":
    s = Vertex("s")
    a = Vertex("a")
    b = Vertex("b")
    c = Vertex("c")
    d = Vertex("d")
    e = Vertex("e")
    f = Vertex("f")
    g = Vertex("g")

    # # bfs
    # lst = [s, a, b, c, d, e, f, g]
    # graphMatrix = GraphMatrix()
    # for i in lst:
    #     graphMatrix.insertVertex(i)
    # graphMatrix.insertEdge(1, 1, 0, 1)
    # graphMatrix.insertEdge(1, 1, 0, 3)
    # graphMatrix.insertEdge(1, 1, 0, 4)
    # graphMatrix.insertEdge(1, 1, 1, 0)
    # graphMatrix.insertEdge(1, 1, 1, 3)
    # graphMatrix.insertEdge(1, 1, 1, 5)
    # graphMatrix.insertEdge(1, 1, 2, 3)
    # graphMatrix.insertEdge(1, 1, 2, 4)
    # graphMatrix.insertEdge(1, 1, 2, 7)
    # graphMatrix.insertEdge(1, 1, 3, 0)
    # graphMatrix.insertEdge(1, 1, 3, 1)
    # graphMatrix.insertEdge(1, 1, 3, 2)
    # graphMatrix.insertEdge(1, 1, 4, 0)
    # graphMatrix.insertEdge(1, 1, 4, 2)
    # graphMatrix.insertEdge(1, 1, 5, 1)
    # graphMatrix.insertEdge(1, 1, 5, 6)
    # graphMatrix.insertEdge(1, 1, 5, 7)
    # graphMatrix.insertEdge(1, 1, 6, 5)
    # graphMatrix.insertEdge(1, 1, 6, 7)
    # graphMatrix.insertEdge(1, 1, 7, 2)
    # graphMatrix.insertEdge(1, 1, 7, 5)
    # graphMatrix.insertEdge(1, 1, 7, 6)
    # graphMatrix.bfs(0)
    # print(11111111111111)
    # graphMatrix.multBFS()

    # # dfs无向图
    # graphMatrix.dfs(0)
    # for i in lst:
    #     i.show()
    # graphMatrix.showEdge()

    # dfs有向图
    lst = [a, b, c, d, e, f, g]
    graphMatrix = GraphMatrix()
    for i in lst:
        graphMatrix.insertVertex(i)
    graphMatrix.insertEdge(1, 1, 0, 1)
    graphMatrix.insertEdge(1, 1, 0, 2)
    graphMatrix.insertEdge(1, 1, 0, 5)
    graphMatrix.insertEdge(1, 1, 1, 2)
    graphMatrix.insertEdge(1, 1, 3, 0)
    graphMatrix.insertEdge(1, 1, 3, 4)
    graphMatrix.insertEdge(1, 1, 4, 5)
    graphMatrix.insertEdge(1, 1, 5, 6)
    graphMatrix.insertEdge(1, 1, 6, 0)
    graphMatrix.insertEdge(1, 1, 6, 2)
    graphMatrix.dfs(0)
    print(111111111111)
    graphMatrix.multDFS()
    for i in lst:
        i.show()
    graphMatrix.showEdge()
