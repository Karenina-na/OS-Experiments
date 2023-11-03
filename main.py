from PageTable import PageTable
import pandas as pd

if __name__ == "__main__":
    physical_memory_size = input("请输入物理内存大小（单位MB）：")
    page_size = input("请输入页大小（单位KB）：")
    process_number = input("请输入进程数量：")

    # 物理内存列表
    physical_memory = [-1 for _ in range(int(physical_memory_size) * 1024 // int(page_size))]

    # 页表初始化
    print("----------------------------------------")
    page_table_list = []
    for i in range(int(process_number)):
        page_table: PageTable
        while True:
            process_size = input("请输入进程 {} 内存大小（单位bit）：".format(i))
            page_length = int(process_size) // (int(page_size) * 1024)
            if int(process_size) % (int(page_size) * 1024) != 0:
                page_length += 1
            page_table = PageTable(i, page_length, int(page_size) * 1024)
            flag = page_table.allocate_memory(physical_memory)
            if not flag:
                # 计算空余内存大小
                free_memory = 0
                for i in range(len(physical_memory)):
                    if physical_memory[i] == -1:
                        free_memory += 1
                print("内存不足，添加失败，剩余内存大小为 {} bit".format(free_memory))
                page_table.free_memory(physical_memory)
            else:
                break
        page_table_list.append(page_table)
        print("内存分配成功，进程 {} 的页表如下：".format(i))
        print(pd.DataFrame(page_table.page_table, columns=["物理块号"]))
        print("----------------------------------------")

    while True:
        print("========================================")
        print("请输入操作")
        print("1. 查看物理内存块分配情况\t 2.查看进程页表\t 3.进程逻辑地址转换\t 4.添加进程\t 5.释放进程内存\t 0.退出")
        op: int
        while True:
            op = int(input("请输入操作："))
            if 0 <= op <= 5:
                break
            else:
                print("输入错误，请重新输入")

        if op == 0:
            # 退出
            print("-" * 50)
            break

        elif op == 1:
            # 查看物理内存块分配情况
            print("-" * 50)
            print("物理内存块分配情况如下：")
            # 统计物理内存块分配情况 进程id: 物理内存块号
            physical_memory_table = []
            for i in range(len(physical_memory)):
                if physical_memory[i] != -1:
                    if physical_memory[i] >= len(physical_memory_table):
                        for _ in range(physical_memory[i] - len(physical_memory_table) + 1):
                            physical_memory_table.append([])
                        physical_memory_table[physical_memory[i]].append(i)
                    else:
                        physical_memory_table[physical_memory[i]].append(i)
            for key in range(len(physical_memory_table)):
                print("进程 {} 占用的物理内存块号为：".format(key), end="")
                print(physical_memory_table[key])

        elif op == 2:
            # 查看进程页表
            print("-" * 50)
            pid = int(input("请输入进程号："))
            if pid >= len(page_table_list):
                print("进程不存在")
                continue
            print("进程页表如下：")
            print(pd.DataFrame(page_table_list[pid].page_table, columns=["物理块号"]))

        elif op == 3:
            # 进程逻辑地址转换
            print("-" * 50)
            pid: int
            while True:
                pid = int(input("请输入进程号（页表地址）："))
                if pid >= len(page_table_list):
                    print("进程不存在，请重新输入")
                else:
                    break

            convert: int
            while True:
                logical_address = int(input("请输入逻辑地址："))
                convert = page_table_list[pid].address_convert(logical_address)
                if convert == -1:
                    print("地址越界，请重新输入")
                else:
                    break
            print("物理地址为：" + str(convert))

        elif op == 4:
            # 添加进程
            print("-" * 50)
            page_table: PageTable
            while True:
                process_size = input("请输入进程 {} 内存大小（单位bit）：".format(len(page_table_list)))
                page_length = int(process_size) // (int(page_size) * 1024)
                if int(process_size) % (int(page_size) * 1024) != 0:
                    page_length += 1
                page_table = PageTable(len(page_table_list), page_length, int(page_size) * 1024)
                flag = page_table.allocate_memory(physical_memory)
                if not flag:
                    # 计算空余内存大小
                    free_memory = 0
                    for i in range(len(physical_memory)):
                        if physical_memory[i] == -1:
                            free_memory += 1
                    print("内存不足，添加失败，剩余内存大小为 {} bit".format(free_memory))
                    page_table.free_memory(physical_memory)
                else:
                    break
            page_table_list.append(page_table)
            print("内存分配成功，进程 {} 的页表如下：".format(page_table.pid))
            print(pd.DataFrame(page_table.page_table, columns=["物理块号"]))
            print("添加成功")

        elif op == 5:
            # 释放进程内存
            print("-" * 50)
            pid = int(input("请输入进程号："))
            page_table_list[pid].free_memory(physical_memory)
            print("释放成功")

    print("进程已退出")
