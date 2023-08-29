import logging

# 自定义日志处理程序
class LogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # 在这里进行自定义操作，例如记录到文件、数据库等
        with open('log.txt', 'a') as f:
            f.write(log_entry + '\n')

def log_init():
    # Set up logging with log handler
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s")

    handler = LogHandler()
    logging.getLogger().addHandler(handler)

