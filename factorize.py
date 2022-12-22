from multiprocessing import Pool, cpu_count
import logging
from time import time

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def factorize(*number):
    
    final_list = []
    for num in number:
        final_list.append(list(filter(lambda x: num % x == 0, range(1, num+1))))

    logger.debug(f"Result - {final_list}")
    return final_list

if __name__ == '__main__':
    start = time()
    with Pool(cpu_count()) as pool:
        result = pool.apply_async(factorize, (128, 255, 99999, 10651060))
        a,b,c,d = result.get()
    # a,b,c,d = factorize(128, 255, 99999, 10651060)
    end = time()
    print(f"Result - {end-start} seconds")
    