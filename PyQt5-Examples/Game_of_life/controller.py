

import threading

from queue import Queue
import time

import model
import view


def worker(q, gen):
    print(gen)
    gen = model.next_generation(gen)
    view.loop(q, 10, 10, 40)
    print(gen)
    q.put(gen)
    q.task_done()


def main():

    height = 10
    width = 10
    scale = 40

    first_gen = model.first_generation(height, width, [[4, 4], [4, 5], [4, 6]])
    
    q = Queue()
    q.put(first_gen)
    
    t = threading.Thread(target=worker, args=(q, first_gen))
    t.start()
    
    
if __name__ == '__main__':
    main()
