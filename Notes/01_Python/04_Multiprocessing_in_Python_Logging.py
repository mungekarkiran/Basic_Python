'''
Multiprocessing in Python: Logging
https://www.youtube.com/watch?v=KpDKpgzvmrY&list=PL5tcWHG-UPH3SX16DI6EP1FlEibgxkg_6&index=4
'''
import logging
import time
from multiprocessing import Process, Lock, Value
from multiprocessing import log_to_stderr, get_logger

def add_500_lock(total, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        total.value += 5
        lock.release()

def sub_500_lock(total, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        total.value -= 5
        lock.release()

if __name__ == '__main__':
    total = Value('i', 500)
    lock = Lock()

    log_to_stderr()
    logger = get_logger()
    logger.setLevel(logging.INFO)

    add_proc = Process(target=add_500_lock, args=(total, lock))
    sub_proc = Process(target=sub_500_lock, args=(total, lock))

    add_proc.start()
    sub_proc.start()

    add_proc.join()
    sub_proc.join()
    print(total.value)