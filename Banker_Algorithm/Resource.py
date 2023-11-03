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
        self.resource = [0 for i in range(m)]  # 资源总数
        self.available = [0 for i in range(m)]  # 可用资源
        self.max = [[0 for i in range(m)] for j in range(n)]  # 最大需求
        self.allocation = [[0 for i in range(m)] for j in range(n)]  # 已分配
        self.need = [[0 for i in range(m)] for j in range(n)]  # 需求
        self.isFinish = [False for i in range(n)]  # 是否完成

        self.flag = False  # 是否安全
        self.safe_list = []  # 安全序列

    def init(self):
        """
        初始化
        :return: None
        """
        print("请输入各类资源总数向量：")
        self.resource = [int(i) for i in input().split()]
        assert len(self.available) == self.m, "资源数与资源数不匹配！"

        print("请输入最大需求矩阵：")
        for i in range(self.n):
            self.max[i] = [int(i) for i in input().split()]
        assert len(self.max[0]) == self.m, "最大需求矩阵与资源数不匹配！"

        print("请输入T0时刻已分配矩阵：")
        for i in range(self.n):
            self.allocation[i] = [int(i) for i in input().split()]
        assert len(self.allocation[0]) == self.m, "已分配矩阵与资源数不匹配！"

        for i in range(self.n):
            for j in range(self.m):
                self.need[i][j] = self.max[i][j] - self.allocation[i][j]

        for i in range(self.m):
            self.available[i] = self.resource[i]
            for j in range(self.n):
                self.available[i] -= self.allocation[j][i]

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

    def verify(self, index, request):
        """
        验证请求是否合法
        :param index: 进程索引
        :param request: [1, 2, 3]
        :return: bool
        """

        assert len(request) == self.m, "请求资源数与资源数不匹配！"

        # 验证请求是否超过最大需求
        for i in range(self.m):
            if request[i] > self.need[index][i]:
                print("请求超过最大需求！不允许分配！")
                return False

        # 验证请求是否超过可用资源
        for i in range(self.m):
            if request[i] > self.available[i]:
                print("请求超过可用资源！不允许分配！")
                return False

        # 更改数据，验证安全性
        for i in range(self.m):
            self.available[i] -= request[i]
            self.allocation[index][i] += request[i]
            self.need[index][i] -= request[i]

        self.safe()
        if not self.flag:
            print("进程 " + str(index) + " 请求 " + str(request) + " 不安全！不允许分配！")
            # roll back
            for i in range(self.m):
                self.available[i] += request[i]
                self.allocation[index][i] -= request[i]
                self.need[index][i] += request[i]
            return False
        else:
            print("请求安全，可用的安全序列为：")
            for seq in self.safe_list:
                print("\t" + seq)
            return True

    def safe(self):
        """
        验证当前状态是否安全
        :return: bool
        """
        self.flag = False
        self.safe_list = []
        visited = [False for i in range(self.n)]
        s = []
        self.dfs(visited, s)

    def dfs(self, visited, s):
        """
        回溯法
        :return:
        """

        if len(s) == self.n:
            self.flag = True
            seq = ""
            for i in range(len(s) - 1):
                seq += "P" + str(s[i]) + "->"
            seq += "P" + str(s[-1])
            self.safe_list.append(seq)
            return

        for i in range(len(visited)):
            if not visited[i]:
                # 检查是否系统持有足够的资源来分配给进程Pi
                flag = True
                for j in range(self.m):
                    if self.need[i][j] > self.available[j]:
                        flag = False
                        break

                # 一次分配，并返回所有资源
                if flag:
                    for j in range(self.m):
                        self.available[j] += self.allocation[i][j]
                    visited[i] = True
                    s.append(i)
                    # 递归
                    self.dfs(visited, s)
                    # 回溯
                    for j in range(self.m):
                        self.available[j] -= self.allocation[i][j]
                    visited[i] = False
                    s.pop()


if __name__ == '__main__':
    n = int(input("请输入进程数："))
    m = int(input("请输入资源数："))
    resource = Resource(n, m)
    # resource.init()
    resource.available = [3, 3, 2]
    resource.max = [[7, 7, 3], [3, 3, 4], [9, 1, 2], [2, 3, 3], [4, 3, 4]]
    resource.allocation = [[0, 2, 0], [2, 1, 0], [3, 0, 2], [2, 1, 2], [0, 1, 2]]
    resource.need = [[7, 5, 3], [1, 2, 4], [6, 1, 0], [0, 2, 1], [4, 2, 2]]
    resource.isFinish = [False, False, False, False, False]

    print(resource.available)
    print(resource.max)
    print(resource.allocation)
    print(resource.need)
    print(resource.isFinish)

    resource.show()
    resource.verify(1, [0, 0, 0])
    """
	P3->P1->P0->P2->P4
	P3->P1->P0->P4->P2
	P3->P1->P2->P0->P4
	P3->P1->P2->P4->P0
	P3->P1->P4->P0->P2
	P3->P1->P4->P2->P0
	P3->P4->P1->P0->P2
	P3->P4->P1->P2->P0
    """
    resource.show()

    resource.safe()
    print(resource.flag)
