import os
from ProcessQueue import ProcessQueue
from Process import Process

if __name__ == '__main__':
    # 初始化队列
    print("多级反馈队列")
    print("========================================")
    q_number = int(input("请输入队列数："))
    q_size = int(input("请输入队列大小："))
    time_slice = int(input("请输入第0级队列时间片："))
    time_scale = int(input("请输入时间增长比例："))
    is_preemptive = input("是否抢占式（y/n）：") == "y"
    queue = ProcessQueue(q_number, q_size, time_slice, time_scale, is_preemptive)
    print("========================================")

    # 批量输入进程信息
    print("批量输入进程信息")
    init_process_num = int(input("请输入进程数量："))
    print("请依次输入进程信息：pid, service_time, priority")
    for i in range(init_process_num):
        pid, service_time, priority = map(int, input().split())
        arrive_time = 0
        # pid不能相同
        flag = True
        for p in queue.processes:
            if p.pid == pid:
                print("pid = {}的进程已存在，请重新输入".format(pid))
                flag = False
                break
        if flag:
            assert len(queue.processes) < queue.size, "队列已满，无法添加新进程"
            queue.put(Process(pid, arrive_time, service_time, priority))
    print("========================================")

    print("开始执行")
    # 执行
    while True:
        print("当前时间片：{} | 当前执行进程 pid = {}".format(queue.time,
                                                           queue.doing.pid if queue.doing is not None else None))
        print("等待队列：{} | 完成队列：{}".format(len(queue.processes), len(queue.processes_done)))
        print("========================================")
        print("请选择操作：")
        print("1. 执行一次")
        print("2. 查看就绪进程信息")
        print("3. 查看进程队列信息信息")
        print("4. 添加进程")
        print("0. 退出")
        print("========================================")
        while True:
            op = int(input("请输入操作："))
            if op == 1 or op == 0:
                break
            elif op == 2:  # 查看就绪进程信息
                queue.showReadyProcess()
                print("--------------------")
            elif op == 3:  # 查看进程队列信息信息
                queue.show()
                print("--------------------")
            elif op == 4:  # 添加进程
                arrive_time = queue.time
                pid, service_time, priority = map(int, input(
                    "请输入进程信息：pid, service_time, priority -- 注意, priority 需要小于 {}\n".format(q_number)).split())
                queue.put(Process(pid, arrive_time, service_time, priority))
                print("--------------------")

        if op == 1:  # 执行一次
            queue.step()
        elif op == 0:   # 退出
            break

    print("========================================")
    print("退出")
