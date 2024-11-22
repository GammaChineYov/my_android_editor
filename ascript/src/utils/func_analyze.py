
import time


def test_call_performance(func, *args, exec_time=3, **kwargs) -> float:
    """
    测试函数调用性能的函数

    :param func: 要测试的函数
    :param args: 要测试函数的位置参数
    :param kwargs: 要测试函数的关键字参数
    :return: 最大调用频率（次/秒）
    """
    # 定义循环执行的时间（秒）
    EXECUTION_TIME = exec_time

    # 用于记录操作开始时间
    start_time = 0
    # 用于记录操作调用次数
    call_count = 0

    def wrapper():
        nonlocal call_count, start_time
        if start_time == 0:
            start_time = time.time()
        call_count += 1
        func(*args, **kwargs)
        

    # 循环执行测试函数指定时间
    start_time = time.time()
    while time.time() - start_time < EXECUTION_TIME:
        wrapper()

    # 计算最大调用频率
    max_call_frequency = calculate_max_call_frequency(call_count, EXECUTION_TIME)
    return max_call_frequency


def calculate_max_call_frequency(call_count, execution_time):
    """
    计算最大调用频率
    :param call_count: 操作调用次数
    :param execution_time: 执行时间（秒）
    :return: 最大调用频率（次/秒）
    """
    if execution_time == 0:
        return 0
    return call_count / execution_time