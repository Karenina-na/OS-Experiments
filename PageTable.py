import random


class PageTable:
    """
    页表  -  一个进程对应一个页表
    """

    def __init__(self, pid, page_length, page_size):
        """
        页表类
        :param page_length:     页表长度 - 页表项数
        :param page_size:   页大小
        """
        self.pid = pid
        self.page_length = page_length
        self.page_size = page_size
        self.page_table = []

    def address_convert(self, virtual_address):
        """
        虚拟地址转换为物理地址
        :param virtual_address: 虚拟地址
        :return: 物理地址
        """
        page_number = virtual_address // self.page_size
        page_offset = virtual_address % self.page_size
        if page_number >= self.page_length:
            print("地址越界")
            return -1
        physical_address = self.page_table[page_number] * self.page_size + page_offset
        return physical_address

    def allocate_memory(self, physical_memory_table):
        """
        分配内存
        :param physical_memory_table: 物理内存表
        :return: bool
        """
        # 随机分配
        counter = 0
        flag = 0
        while counter < self.page_length:
            page_number = random.randint(0, len(physical_memory_table) - 1)

            if flag > 10:
                # 如果随机分配10次都没有找到空闲的物理块，转顺序分配
                left = 0
                right = len(physical_memory_table) - 1
                while left <= right:
                    if physical_memory_table[left] == -1:
                        physical_memory_table[left] = self.pid
                        self.page_table.append(left)
                        counter += 1
                    left += 1

                    if counter >= self.page_length:
                        break

                    if physical_memory_table[right] == -1:
                        physical_memory_table[right] = self.pid
                        self.page_table.append(right)
                        counter += 1
                    right -= 1

                    if counter >= self.page_length:
                        break

                break

            else:
                if physical_memory_table[page_number] == -1:
                    physical_memory_table[page_number] = self.pid
                    self.page_table.append(page_number)
                    counter += 1
                    flag = 0
                else:
                    flag += 1

    def free_memory(self, physical_memory_table):
        """
        释放进程占用的内存
        :param physical_memory_table: 物理内存表
        :return: bool
        """
        # 二分搜索
        left = 0
        right = len(physical_memory_table) - 1
        while left <= right:

            if physical_memory_table[left] == self.pid:
                physical_memory_table[left] = -1
            left += 1

            if physical_memory_table[right] == self.pid:
                physical_memory_table[right] = -1
            right -= 1

        return True


if __name__ == "__main__":
    # 一页对应一个物理块
    pmt = [-1 for _ in range(32)]
    page_table = PageTable(10, 10, 16)
    page_table.allocate_memory(pmt)
    print(pmt)
    print(page_table.page_table)
    addr = page_table.address_convert(18)
    # 物理地址 = 页号 * 页大小 + 页内偏移    (一个页对应一个物理块)
    # 页号 = 逻辑地址 / 页大小
    # 页内偏移 = 逻辑地址 % 页大小
    print(page_table.page_table[18 // page_table.page_size] * page_table.page_size + 18 % page_table.page_size)
    print(addr)

    page_table.free_memory(pmt)
    print(pmt)
