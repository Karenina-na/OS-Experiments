from Resource import Resource

if __name__ == '__main__':
    n = int(input("请输入进程数："))
    m = int(input("请输入资源数："))

    resource = Resource(n, m)
    resource.init()

    while True:
        print("========================================")
        print("请输入操作")
        print("1. 查看当前资源分配情况\t 2.请求分配资源\t 3.当前可用安全序列\t 0.退出")
        op: int
        while True:
            op = int(input("请输入操作："))
            if 0 <= op <= 3:
                break
            else:
                print("输入错误，请重新输入")

        if op == 0:
            # 退出
            print("-" * 50)
            break

        elif op == 1:
            # 查看当前资源分配情况
            print("-" * 50)
            resource.show()

        elif op == 2:
            print("-" * 50)
            # 请求分配资源
            process = int(input("请输入请求资源的进程号："))
            request = input("请输入请求的资源：").split()
            request = [int(i) for i in request]
            resource.verify(process, request)

        elif op == 3:
            print("-" * 50)
            # 当前可用安全序列
            resource.safe()
            print("可用的安全序列为：")
            for seq in resource.safe_list:
                print("\t" + seq)

    print("进程已退出")
