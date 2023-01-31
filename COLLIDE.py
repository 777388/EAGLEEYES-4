import multiprocessing
import time

def worker(mem):
    while True:
        mem.put('string1')
        time.sleep(1)
        mem.put('string2')
        time.sleep(1)

if __name__ == '__main__':
    mem = multiprocessing.Manager().Queue()
    process1 = multiprocessing.Process(target=worker, args=(mem,))
    process2 = multiprocessing.Process(target=worker, args=(mem,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
