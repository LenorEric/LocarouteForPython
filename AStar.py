import queue
import json


# if you want to change Heuristic calcation
# you may change it, and make it more sophisticated
def calcHeur(prePos, dest):
    h_diagonal = min(abs(prePos[0] - dest[0]), abs(prePos[0] - dest[0]))
    h_straight = abs(prePos[0] - dest[0]) + abs(prePos[0] - dest[0])
    heur = h_diagonal * (2 ** 0.5) + h_straight - 2 * h_diagonal
    return heur


class AStar:
    invalid = []
    startPoint = [0, 0]
    destination = [0, 0]
    route = []
    open = queue.PriorityQueue
    map = {}
    closed = []
    totalLen = 0

    def __init__(self, invalid, startPoint, destination):
        self.invalid = invalid
        self.totalLen = len(invalid[0])
        self.startPoint = startPoint
        self.destination = destination
        self.open.put([calcHeur(startPoint, destination), 0, startPoint, [-1, -1]])

    def generoute(self):
        pre = self.closed[len(self.closed) - 1]
        if pre[2] != self.destination:
            print("Desti ERROR")
        while pre[3] != [-1, -1]:
            self.route.append(pre[2])
            pre = self.closed[self.map[pre[3]]]
        self.route.reverse()

    def bfs(self):
        # bearing list
        bearing = [[i, j] for j in range(-1, 1) for i in range(-1, 1)]
        while True:
            pre = self.open.get()
            for i in range(8):
                if pre[2][0] + bearing[i][0] < 0 or pre[2][0] + bearing[i][0] >= self.totalLen or pre[2][1] + \
                        bearing[i][1] < 0 or pre[2][1] + bearing[i][1] >= self.totalLen:
                    break
                if self.invalid[pre[2][0] + bearing[i][0]][pre[2][1] + bearing[i][1]]:
                    nextStep = [0, pre[1] + 1 + (1 - i % 2) * (2 ** 0.5 - 1),
                                [pre[2][0] + bearing[i][0], pre[2][1] + bearing[i][1]], pre[2]]
                    if nextStep[2] == self.destination:
                        self.closed.append(nextStep)
                        self.map[nextStep[2]] = len(self.closed) - 1
                        self.generoute()
                        break
                    nextStep[0] = nextStep[1] + calcHeur(nextStep[2], self.destination)
                    self.map[pre[2]] = len(self.closed) - 1
                    self.open.put(nextStep)
                self.closed.append(pre)
