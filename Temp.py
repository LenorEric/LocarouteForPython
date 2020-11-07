import queue

if __name__ == '__main__':
    openX = queue.PriorityQueue()
    for i in range(5, 0, -1):
        openX.put(i)
    for i in range(5):
        print(openX.get())
