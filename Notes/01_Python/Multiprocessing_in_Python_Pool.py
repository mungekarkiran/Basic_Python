'''
Multiprocessing in Python: Pool
https://www.youtube.com/watch?v=u2jTn-Gj2Xw
'''
import time
from multiprocessing import Pool

def sum_of_square(number):
    '''
    This function is used to return sum of square.
    '''
    sos = 0
    for num in range(number):
        sos += num * num
    return sos

def sum_of_square_with_MP(numbers):
    # start time 
    start_time = time.time()

    p = Pool()
    result = p.map(sum_of_square, numbers)
    # print(f"Result : {result}")
    p.close()
    p.join()
    
    # end time
    end_time = time.time() - start_time
    print(f"Processing {len(numbers)} numbers took {end_time} sec. time using multiprocessing.")

def sum_of_square_without_MP(numbers):
    # start time 
    start_time = time.time()

    result = []
    for num in numbers:
        result.append(sum_of_square(num))

    # end time
    end_time = time.time() - start_time
    print(f"Processing {len(numbers)} numbers took {end_time} sec. time using serial processing.")


if __name__ == "__main__":
    numbers = range(100)
    
    # # test with MP
    # p = Pool()
    # result = p.map(sum_of_square, numbers)
    # print(f"Result : {result}")
    # p.close()
    # p.join()

    # run function with multiprocessing
    sum_of_square_with_MP(numbers)
    # run function without multiprocessing
    sum_of_square_without_MP(numbers)

    # test 2
    numbers = range(10000)
    # run function with multiprocessing
    sum_of_square_with_MP(numbers)
    # run function without multiprocessing
    sum_of_square_without_MP(numbers)
