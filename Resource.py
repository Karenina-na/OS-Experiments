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


if __name__ == '__main__':
    n = int(input("请输入进程数："))
    m = int(input("请输入资源数："))
    resource = Resource(n, m)
    resource.init()
    print(resource.available)
    print(resource.max)
    print(resource.allocation)
    print(resource.need)
    print(resource.isFinish)
