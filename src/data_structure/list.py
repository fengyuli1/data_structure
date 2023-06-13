class ListNode:
    def __init__(self, data, pred=None, succ=None):
        self.data = data
        self.pred = pred
        self.succ = succ

    def insertAsPred(self, e):
        """前驱插入"""
        x = ListNode(e, self.pred, self)
        self.pred.succ = x
        self.pred = x
        return x

    def insertAsSucc(self, e):
        """后继插入"""
        x = ListNode(e, self, self.succ)
        self.succ.pred = x
        self.succ = x
        return x


class List:
    def __init__(self):
        self._size = 0
        self._header = ListNode(None)
        self._trailer = ListNode(None)
        self._header.succ = self._trailer
        self._trailer.pred = self._header

    def find(self, e, n=None, p=None):
        """无序列表查找
        在节点p（可能是trailer）的n个真前驱中，找到等于e的最后者"""
        if not p:
            p = self._trailer
        if not n:
            n = self._size
        while n > 0 and p.pred.data:  # n=0或者已经没有前驱，退出循环
            if e == p.pred.data:
                return p.pred
            else:
                p = p.pred
                n -= 1
        return None

    def first(self):
        return self._header.succ

    def last(self):
        return self._trailer.pred

    def insertFirst(self, e):
        return self.insertBefore(self.first(), e)

    def insertLast(self, e):
        return self.insertBefore(self.last(), e)

    def insertBefore(self, p, e):
        """在p节点前插入"""
        self._size += 1
        return p.insertAsPred(e)

    def insertAfter(self, p, e):
        """在p节点后插入"""
        self._size += 1
        return p.insertAsSucc(e)

    def remove(self, p):
        """删除节点"""
        e = p.data
        p.pred.succ = p.succ
        p.succ.pred = p.pred
        self._size -= 1
        return e

    def deduplicate(self):
        """无序列表去重，返回列表规模变化"""
        if self._size < 2:  # 最多只有一个元素，直接返回
            return 0
        oldsize = self._size
        p = self.first().succ  # 初始指向第二个元素
        n = 1
        while p != self._trailer:
            q = self.find(p.data, n, p)  # 查找p的n个前驱中是否有雷同
            if q:  # 如果有
                self.remove(q)  # 删除该节点
            else:  # 如果没有
                n += 1  # 秩递增
            p = p.succ  # p指向下一个元素
        return oldsize - self._size  # 返回规模变化

    def uniquify(self):
        """有序列表去重，返回列表规模变化"""
        if self._size < 2:  # 最多只有一个元素，直接返回
            return 0
        oldsize = self._size
        p = self.first()  # 初始指向第一个元素
        while p != self._trailer:  # 考察紧邻的节点对
            if p.data == p.succ.data:  # 若雷同，删除后者
                self.remove(p.succ)
            else:  # 否则，指向下一区段
                p = p.succ
        return oldsize - self._size

    def search(self, e, n=None, p=None):
        """有序列表查找
        在节点p（可能是trailer）的n个真前驱中，找到不大于于e的最后者"""
        if not p:
            p = self._trailer
        if not n:
            n = self._size
        p = p.pred
        while n > 0 and p.pred:  # n=0或者已经没有前驱，退出循环
            if p.data <= e:
                break
            else:
                p = p.pred
                n -= 1
        return p

    def selectSort(self):
        """选择排序,时间复杂度O(n^2)
        每次循环找出最大值放至列表末尾"""
        p = self.last()
        head = self.first()
        n = self._size
        while p != head:
            max = self._selectMax(head, n)
            max.data, p.data = p.data, max.data
            p = p.pred
            n -= 1

    def _selectMax(self, p, n):
        """选择排序，查询最大值所在的node"""
        max = p
        while n > 1:
            if max.data <= p.succ.data:
                max = p.succ
            p = p.succ
            n -= 1
        return max

    def insertionSort(self):
        """插入排序"""
        p = self.first().succ
        n = 1
        while p != self._trailer:
            x = self.search(p.data, n, p)
            self.insertAfter(x, p.data)
            p = p.succ
            self.remove(p.pred)
            n += 1


li = List()
la = []
print(li.last())
print(li.first())
print("=======================")
la.append(li.insertFirst(5))
la.append(li.insertAfter(la[0], 4))
la.append(li.insertAfter(la[1], 3))
la.append(li.insertAfter(la[2], 6))
la.append(li.insertAfter(la[3], 1))
la.append(li.insertAfter(la[4], 8))
la.append(li.insertAfter(la[5], 7))
la.append(li.insertAfter(la[6], 2))
la.append(li.insertAfter(la[7], 9))
a = li.first()
print(a, end=",")
print(a.data)
for i in range(8):
    a = a.succ
    print(a, end=",")
    print(a.data)
print("11111111111111111111111")
li.insertionSort()
a = li.first()
print(a, end=",")
print(a.data)
for i in range(8):
    a = a.succ
    print(a, end=",")
    print(a.data)
print("")
print("22222222222222222222222")
