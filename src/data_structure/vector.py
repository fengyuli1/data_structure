import random


class Vector:
    def __init__(self, li=None, lo=0, hi=0):
        CAPACITY = 3
        self._size = 0
        if li:
            if not hi or hi > len(li):
                hi = len(li)
            self._capacity = (hi - lo) * 2
            self._elem = [None] * self._capacity
            self.__copyFrom(li, lo, hi)
        else:
            self._capacity = CAPACITY
            self._elem = [None] * self._capacity
        print(self._elem)

    def __iter__(self):
        self.init = 0
        return self

    def __next__(self):
        if self.init < self._size:
            val = self._elem[self.init]
            self.init += 1
            return val
        else:
            raise StopIteration

    def __getitem__(self, item):
        if item < self._size:
            return self._elem[item]
        else:
            raise StopIteration

    def __copyFrom(self, li, lo, hi):
        while lo < hi:
            self._elem[self._size] = li[lo]
            self._size += 1
            lo += 1

    def __expand(self):
        if self._size < self._capacity:
            return
        self._capacity *= 2
        old = self._elem
        self._elem = [None] * self._capacity
        for i in range(0, self._size):
            self._elem[i] = old[i]

    def insert(self, e, r=None):
        self.__expand()
        if not r or r > self._size:
            r = self._size
        i = self._size
        while i > r:
            self._elem[i] = self._elem[i - 1]
            i -= 1
        self._elem[r] = e
        self._size += 1
        return r

    def remove(self, lo, hi=None):
        if lo == hi:
            return 0
        if not hi:
            hi = lo + 1
        if hi > self._size:
            hi = self._size
        while hi < self._size:
            self._elem[lo] = self._elem[hi]
            hi += 1
            lo += 1
        self._size = lo
        return hi - lo

    def find(self, e, lo=0, hi=None):
        if not hi or hi > self._size:
            hi = self._size
        while lo <= hi:
            hi -= 1
            if e == self._elem[hi]:
                return hi
        return hi

    def deduplicate(self):
        """对无序向量去重"""
        lo = 1
        old_size = self._size
        while lo < self._size:
            if self.find(self._elem[lo], 0, lo) < 0:
                lo += 1
            else:
                self.remove(lo)
        return old_size - self._size

    def traverse(self, visit):
        """遍历整个向量并对每个向量进行操作"""
        for i in range(0, self._size):
            self._elem[i] = visit(self._elem[i])

    def disordered(self):
        """判断向量是否是升序，返回逆序对的数量"""
        n = 0
        for i in range(1, self._size):
            if self._elem[i - 1] > self._elem[i]:
                # 如果前一个向量比后一个向量大，逆序对+1
                n += 1
        return n

    def uniquify(self):
        """对有序向量去重"""
        i = 0
        j = 1
        while j < self._size:
            if self._elem[i] != self._elem[j]:
                # 如果第i个元素和第j个元素不同，则将第i+1个元素赋值为第j个元素的值
                i += 1
                self._elem[i] = self._elem[j]
            j += 1
        self._size = i + 1
        return j - i - 1

    def search(self, e, lo=0, hi=None):
        """二分查找，返回右边界"""
        if not hi or hi > self._size:
            hi = self._size
        while lo < hi:
            mid = (lo + hi) // 2
            if e < self._elem[mid]:
                hi = mid
            else:
                lo = mid + 1
        return lo - 1

    def sort(self, lo=0, hi=None):
        """随机选择排序算法"""
        if not hi or hi > self._size:
            hi = self._size
        i = random.randint(1, 5)
        if i < 1:
            self.__bubbleSort(lo, hi)  # 起泡排序
        else:
            self.__mergeSort(lo, hi)  # 归并排序

    def __bubbleSort(self, lo, hi):
        """起泡排序
        最好时间复杂度O(n)
        最坏时间复杂度O(n^2)"""
        while True:
            # 每一次循环都将第hi个向量有序
            sorted = True  # 标志位，表示向量是否已经有序，初始化为True
            i = lo
            last = lo  # 记录最右侧逆序对位置，初始化为lo
            while i < hi - 1:
                if self._elem[i] > self._elem[i + 1]:
                    # 如果第i个向量比第i+1个向量大，则交换两者的值
                    self._elem[i], self._elem[i + 1] = self._elem[i + 1], self._elem[i]
                    sorted = False  # 发生了交换，将标志位置为False
                    last = i + 1  # 更新最右侧逆序对位置
                i += 1
            if sorted:
                # 优化1：如果没有发生交换，则表明向量已经有序，退出循环
                return
            hi = last  # 优化2：将hi直接置为最后发生位置交换的位置

    def __mergeSort(self, lo, hi):
        """递归调用，将向量分解为单个元素"""
        if (hi - lo) > 1:
            mid = (lo + hi) // 2
            self.__mergeSort(lo, mid)
            self.__mergeSort(mid, hi)
            self.__merge(lo, mid, hi)
        return

    def __merge(self, lo, mid, hi):
        """一次归并操作"""
        ltmp = self._elem[lo:mid]  # 临时向量，等于待归并向量的前半段
        k = mid - lo  # 临时向量长度
        i = 0
        while i < k and mid < hi:  # 比较前后段向量大小
            if ltmp[i] <= self._elem[mid]:  # 如果前段向量小，取出来放到原向量
                self._elem[lo] = ltmp[i]
                i += 1
            else:  # 如果后段向量小，取出来放到原向量
                self._elem[lo] = self._elem[mid]
                mid += 1
            lo += 1
        while i < k:  # 如果临时向量还有剩余，放到原向量末尾
            self._elem[lo] = ltmp[i]
            i += 1
            lo += 1


class C:
    def increse(self, val):
        val += 1
        return val


a = Vector()
a.insert(9)
a.insert(4)
a.insert(2)
a.insert(3)
a.insert(1)
a.insert(5)
a.insert(6)
a.insert(7)
a.insert(8)
a.insert(0)
for i in a:
    print(i, end=",")
print("")
a.sort()
for i in a:
    print(i, end=",")
print("")
