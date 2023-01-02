'''
Multiprocessing in Python: Introduction (Part 1)
https://www.youtube.com/watch?v=RR4SoktDQAw&list=PL5tcWHG-UPH3SX16DI6EP1FlEibgxkg_6&index=1
'''
import os
import time
from multiprocessing import Process, current_process

def square(number:float):
    '''
    This function is used to print
    the square of a number.
    '''
    # We can use 'os' modul in Python to print out the Process ID 
    # assigned to the call of this function assigned by the operating system.
    process_id = os.getpid()
    print(f"Process ID : {process_id}.")

    # We can also use the 'current_process' function to get the name
    # of the process object.
    process_name = current_process().name
    print(f"Process name : {process_name}.")

    # calculate square of a number
    result = number * number
    print(f"The number {number} square to {result}.")



if __name__ == "__main__":
    numbers = range(1000)
    processes = []

    # start time
    start_time = time.time()

    for number in numbers:
        # normal function call
        # square(number)

        # function call with multiprocessing
        process = Process(target=square, args=(number,))
        processes.append(process)

        # Processes are spawned (create / generate) by creating a process object and
        # then calling it stasrt() method.
        process.start()

    # end time
    end_time = time.time() - start_time
    print(f"Processing took {end_time} sec. time.") 
    # Processing took 0.451002836227417 sec. time. -> using normal function call with 100 numbers.
    # Processing took 5.0010833740234375 sec. time. -> using multiprocessing with 100 numbers.

    # Processing took 1.4930028915405273 sec. time. -> using normal function call with 1000 numbers.
    # Processing took 63.32500386238098 sec. time. -> using multiprocessing with 1000 numbers.