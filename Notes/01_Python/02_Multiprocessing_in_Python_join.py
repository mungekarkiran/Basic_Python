'''
Multiprocessing in Python: Introduction (Part 2)
https://www.youtube.com/watch?v=itbx_hDX7z8&list=PL5tcWHG-UPH3SX16DI6EP1FlEibgxkg_6&index=2
'''
import os
import time
from multiprocessing import Process, current_process

def square(numbers:list):
    '''
    This function is used to print
    the square of a number.
    '''
    # We can also use the 'current_process' function to get the name
    # of the process object.
    process_name = current_process().name
    print(f"Process name : {process_name}.")

    for number in numbers:
        # time.sleep(0.5)
        # calculate square of a number
        result = number * number
        print(f"The number {number} square to {result}.")

if __name__ == "__main__":
    numbers = range(100)
    processes = []

    # start time
    start_time = time.time()

    for _ in range(10):
        # function call with multiprocessing
        process = Process(target=square, args=(numbers,))
        processes.append(process)

        # Processes are spawned (create / generate) by creating a process object and
        # then calling it stasrt() method.
        process.start()

    for process in processes:
        # The join method blocks the execution of the main process until 
        # the process whose join method is called terminates. Without the 
        # join method, the main process won't wait until the process gets terminated.
        process.join()

    # end time
    end_time = time.time() - start_time
    print(f"Processing took {end_time} sec. time.") 