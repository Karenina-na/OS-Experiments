import numpy as np
import pandas as pd


class Resource:
    def __init__(self, n, m):
        """
        资源分配图
        :param n: n个进程
        :param m: m个资源
        """
        self.n = n
        self.m = m
        self.available = [0 for i in range(m)]  # 可用资源
        self.max = [[0 for i in range(m)] for j in range(n)]  # 最大需求
        self.allocation = [[0 for i in range(m)] for j in range(n)]  # 已分配
        self.need = [[0 for i in range(m)] for j in range(n)]  # 需求
        self.isFinish = [False for i in range(n)]  # 是否完成

    def init(self):
        """
        初始化
        :return: None
        """
        print("请输入可用资源向量：")
        self.available = [int(i) for i in input().split()]

        print("请输入最大需求矩阵：")
        for i in range(self.n):
            self.max[i] = [int(i) for i in input().split()]

        print("请输入T0时刻已分配矩阵：")
        for i in range(self.n):
            self.allocation[i] = [int(i) for i in input().split()]

        for i in range(self.n):
            for j in range(self.m):
                self.need[i][j] = self.max[i][j] - self.allocation[i][j]

        print("初始化成功！--------------------------")

    def show(self):
        """
        进程名  Max    Allocation    Need    Available
              A B C     A B C       A B C     A B C
        P0    1 2 5     9 8 1       8 6 4     3 3 2
        P1    8 2 3     3 2 2       5 0 1     None
        P2    3 2 4     4 0 2       1 2 2     None
        ...
        :return:
        """
        # 构建列索引
        columns = [[]]
        for i in range(self.m):
            columns[0].append('    Max')
        for i in range(self.m):
            columns[0].append('    Alloc')
        for i in range(self.m):
            columns[0].append('    Need')
        for i in range(self.m):
            columns[0].append('    Avail')
        columns.append([])
        for i in range(4):
            for j in range(self.m):
                columns[1].append(chr(65 + j))

        # 构建数据
        data = []
        for i in range(self.n):
            data.append([])
            for j in range(self.m):
                data[i].append(self.max[i][j])
            for j in range(self.m):
                data[i].append(self.allocation[i][j])
            for j in range(self.m):
                data[i].append(self.need[i][j])
            if i == 0:
                for j in range(self.m):
                    data[i].append(str(self.available[j]))
            else:
                for j in range(self.m):
                    data[i].append(np.NAN)

        df = pd.DataFrame(data=data, columns=columns, index=['P' + str(i) for i in range(self.n)])

        print(df)




if __name__ == '__main__':
    n = int(input("请输入进程数："))
    m = int(input("请输入资源数："))
    resource = Resource(n, m)
    # resource.init()
    resource.available = [12, 6, 8]
    resource.max = [[6, 4, 3], [3, 2, 4], [9, 0, 3], [2, 2, 2], [3, 4, 3]]
    resource.allocation = [[1, 1, 0], [2, 0, 1], [4, 0, 2], [2, 1, 1], [0, 1, 2]]
    resource.need = [[5, 3, 3], [1, 2, 3], [5, 0, 1], [0, 1, 1], [3, 3, 1]]
    resource.isFinish = [False, False, False, False, False]

    # print(resource.available)
    # print(resource.max)
    # print(resource.allocation)
    # print(resource.need)
    # print(resource.isFinish)

    resource.show()
