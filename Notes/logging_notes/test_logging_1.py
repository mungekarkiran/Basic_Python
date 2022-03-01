import logging
logging.basicConfig(filename='my_divlog.log', level = logging.DEBUG, format='%(levelname)s %(asctime)s %(message)s')

def divbyzero(a,b):
    logging.info(f'Start of the code and a: {a}, b: {b}.')
    try:
        div = a/b
        logging.info(f'Executed successfully and ans. is : {div}.')
    except Exception as e:
        logging.error('Error occured.')
        logging.exception(f'Exception is : {e}.')


divbyzero(3,2)
divbyzero(4,1)
divbyzero(6,0)
divbyzero(0,2)
divbyzero(3,6)
divbyzero(0,'2')
divbyzero(3,0.9)

