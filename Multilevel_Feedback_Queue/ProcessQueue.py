import queue
from Process import Process


class ProcessQueue:
    def __init__(self, q_number=4, q_size=10, time_slice=1, time_scale=2, is_preemptive=True):
        """
        多级反馈队列
        :param q_number:        队列数量
        :param q_size:          队列大小
        :param time_slice:      时间片
        :param time_scale:      时间片倍率
        :param is_preemptive:   是否抢占式
        """
        self.q_size = q_size
        self.is_preemptive = is_preemptive
        self.queues = []
        self.time_slice = []
        for i in range(q_number):
            self.queues.append(queue.Queue(maxsize=q_size))
            self.time_slice.append(time_slice * time_scale ** i)

        self.time = 0  # 当前时间
        self.processes = []  # 等待队列
        self.processes_done = []  # 完成队列
        self.doing = None  # 正在执行的进程

    def put(self, process: Process):
        """
        将进程放入队列
        :param process: 进程
        """
        assert process.priority < len(self.queues)
        process.state = process.state.Ready
        self.processes.append(process)
        self.queues[process.priority].put(process)

    def step(self):
        """
        执行一步
        """
        if len(self.processes) == 0 and self.doing is None:
            return

        # 找到优先级最高的进程
        if self.doing is None:
            for i in range(len(self.queues)):
                if not self.queues[i].empty():
                    self.doing = self.queues[i].get()
                    break
        else:
            # 如果是抢占式，且有更高优先级的进程，抢占
            flag = False
            if self.is_preemptive:
                for i in range(len(self.queues)):
                    if not self.queues[i].empty() and i < self.doing.priority:
                        self.doing.end_once_service(0)  # 结束一次服务
                        self.queues[self.doing.priority].put(self.doing)
                        self.doing = self.queues[i].get()
                        flag = True
                        break

            # 如果没有抢占，且只有最后一级队列，采用时间片轮转
            if not flag and self.doing.priority == len(self.queues) - 1:
                self.doing.end_once_service(0)
                self.queues[self.doing.priority].put(self.doing)
                self.doing = self.queues[self.doing.priority].get()

        # 执行
        self.doing.do(1)

        # 如果执行完毕，放入完成队列
        if self.doing.is_done():
            print("<========= 进程 pid = {} 执行完毕，当前时间：{} =========>".format(self.doing.pid, self.time))
            self.processes.remove(self.doing)
            self.processes_done.append(self.doing)
            self.doing = None

        # 如果时间片用完，放入下一级队列
        elif self.doing.once_service_time >= self.time_slice[self.doing.priority]:
            # 如果是最后一级队列，不放入下一级队列
            if self.doing.priority == len(self.queues) - 1:
                self.doing.end_once_service(0)
            else:
                self.doing.end_once_service(1)
            self.queues[self.doing.priority].put(self.doing)
            self.doing = None

        self.time += 1

    def get(self, pid):
        """
        获取指定pid的进程
        :param pid:     进程pid
        :return:        进程
        """
        for p in self.processes:
            if p.pid == pid:
                return p
        for p in self.processes_done:
            if p.pid == pid:
                return p
        return None

    def show(self):
        """
        查看当前进程执行情况
        """
        print(
            "当前时间：{} | 当前执行进程 pid = {}".format(self.time, self.doing.pid if self.doing is not None else None))
        print("等待队列：{} | 完成队列：{}".format(len(self.processes), len(self.processes_done)))
        print("=" * 50)
        for i in range(len(self.queues)):
            print("第 {} 级队列 | 队列进程数：{} | 时间片：{}".format(i, self.queues[i].qsize(), self.time_slice[i]))
            print("-" * 50)
            print("头  |", end=" ")
            for content in self.queues[i].queue:
                print("{} |".format(content.pid), end=" ")
            print(" 尾")
            print("-" * 50)
            print()

    def showReadyProcess(self):
        """
        查看就绪进程
        """
        print("就绪进程：")
        for task in self.processes:
            print(task)

    def showFinishProcess(self):
        """
        查看完成队列
        """
        print("完成进程：")
        for task in self.processes_done:
            print(task)


if __name__ == '__main__':
    q = ProcessQueue(q_number=4, q_size=10, time_slice=1, time_scale=2, is_preemptive=True)
    p1 = Process(1, 2, 10, 0)
    p2 = Process(2, 2, 10, 0)
    q.put(p1)
    q.put(p2)
    q.put(p1)
    q.put(p1)
    q.put(p1)
    q.show()
