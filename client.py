import multiprocessing
import time

def process1():
    while True:
        print("Process 1")
        time.sleep(3)

def process2():
    while True:
        print("Process 2")
        time.sleep(3)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=process1)
    p2 = multiprocessing.Process(target=process2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()