import socket
import threading
import time


class SimplePortScanner:
    def __init__(self, target, timeout=1.0, max_threads=100):
        self.target = target
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
        self.lock = threading.Lock()  # 用于线程安全地修改共享数据

    def scan_port(self, port):
        """扫描单个端口"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    with self.lock:  # 确保线程安全
                        self.open_ports.append(port)
                        print(f"端口 {port} 开放")
        except Exception:
            pass  # 静默处理异常

    def scan_range(self, start_port=1, end_port=1024):
        """扫描端口范围"""
        print(f"开始扫描 {self.target} 的端口 {start_port}-{end_port}...")
        start_time = time.time()

        threads = []
        # 创建并启动所有线程
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()

            # 控制同时运行的线程数量
            while threading.active_count() > self.max_threads:
                time.sleep(0.1)

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        end_time = time.time()
        print(f"\n扫描完成! 耗时: {end_time - start_time:.2f} 秒")
        print(f"发现 {len(self.open_ports)} 个开放端口: {sorted(self.open_ports)}")


def main():
    target = input("请输入目标主机名或IP地址: ")
    start_port = int(input("请输入起始端口 (默认1): ") or 1)
    end_port = int(input("请输入结束端口 (默认1024): ") or 1024)

    scanner = SimplePortScanner(target)
    scanner.scan_range(start_port, end_port)


if __name__ == "__main__":
    main()