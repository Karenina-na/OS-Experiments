import enum


class ProcessState(enum.Enum):
    """
    进程七个状态
    """
    Start = 0
    Ready = 1
    ReadySuspend = 2
    Running = 3
    Blocked = 4
    BlockedSuspend = 5
    Finished = 6


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        """
        进程类
        :param pid:             进程ID
        :param arrival_time:    到达时间
        :param burst_time:      服务时间
        :param priority:        优先级
        """
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.state = ProcessState.Start
        self.once_service_time = 0  # 单次服务时间

    def end_once_service(self, add_priority=0):
        """
        结束一次服务
        :param add_priority:    优先级增加
        """
        self.once_service_time = 0

        self.priority += add_priority

    def do(self, time):
        """
        进程执行
        :param time:    时间
        """
        self.burst_time -= time
        if self.burst_time <= 0:
            self.burst_time = 0
            self.state = ProcessState.Finished
        else:
            self.state = ProcessState.Running
        self.once_service_time += time

    def is_done(self):
        """
        是否执行完毕
        :return:
        """
        return self.state == ProcessState.Finished

    def __str__(self):
        t = ""
        if self.state == ProcessState.Start:
            t = "Start"
        elif self.state == ProcessState.Ready:
            t = "Ready"
        elif self.state == ProcessState.ReadySuspend:
            t = "ReadySuspend"
        elif self.state == ProcessState.Running:
            t = "Running"
        elif self.state == ProcessState.Blocked:
            t = "Blocked"
        elif self.state == ProcessState.BlockedSuspend:
            t = "BlockedSuspend"
        elif self.state == ProcessState.Finished:
            t = "Finished"

        return "Process(pid= {}, 到达时间= {}, 需要服务时间= {}, 当前优先级= {}, 状态= {})".format(
            self.pid, self.arrival_time, self.burst_time, self.priority, t
        )


if __name__ == '__main__':
    p = Process(1, 2, 3, 4)
    print(p)