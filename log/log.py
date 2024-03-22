import logging
import datetime
import os


def log_record():
    # 创建日志记录器
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    # 创建文件处理程序
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = 'logs/file_{}.txt'.format(current_time)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')

    # 创建控制台处理程序
    console_handler = logging.StreamHandler()

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 将格式化器分别应用于文件处理程序和控制台处理程序
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理程序添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 示例用法
    logger.info('这是一条日志信息')
    logger.warning('这是一条警告信息')
    return logger
