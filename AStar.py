import queue
import ImageOutput


# if you want to change Heuristic calcation
# you may change it, and make it more sophisticated
def calcHeur(prePos, dest):
    h_diagonal = min(abs(prePos[0] - dest[0]), abs(prePos[1] - dest[1]))
    h_straight = abs(prePos[0] - dest[0]) + abs(prePos[1] - dest[1])
    heur = h_diagonal * 1.41421 + h_straight - 2 * h_diagonal
    return heur


# noinspection PyArgumentList
class AStar:
    count = 0
    invalid = []
    startPoint = [0, 0]
    destination = [0, 0]
    colored = []
    route = []
    open = queue.PriorityQueue()
    map = {}
    closed = []
    totalLen = 0
    imgDB = ImageOutput.IMGDebugger()

    def __init__(self, invalid, startPoint, destination):
        self.invalid = []
        self.startPoint = [0, 0]
        self.destination = [0, 0]
        self.colored = []
        self.route = []
        self.open = queue.PriorityQueue()
        self.map = {}
        self.closed = []
        self.totalLen = 0
        self.imgDB = ImageOutput.IMGDebugger()
        self.invalid = invalid
        self.totalLen = len(invalid[0])
        self.colored = [[0 for i in range(self.totalLen)] for j in range(self.totalLen)]
        self.startPoint = startPoint
        self.destination = destination
        self.open.put([calcHeur(startPoint, destination), 0, startPoint, [-1, -1]])

    def generoute(self):
        def sameDirc(lst, pre, nxt):
            if pre[0] - lst[0] == nxt[0] - pre[0] and pre[1] - lst[1] == nxt[1] - pre[1]:
                return True
            else:
                return False

        allRoute = []
        pre = self.closed[len(self.closed) - 1]
        if pre[2] != self.destination:
            print("Desti ERROR")
        while pre[3] != [-1, -1]:
            allRoute.append(pre[2])
            pre = self.closed[self.map[tuple(pre[3])]]
        allRoute.reverse()
        prime = [0]
        for i in range(1, len(allRoute) - 1):
            if not (sameDirc(allRoute[i - 1], allRoute[i], allRoute[i + 1])):
                prime.append(i)
        for key in prime:
            self.route.append(allRoute[key])

    def bfs(self):
        # bearing list
        bearing = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
        used = [[0 for i in range(self.totalLen)] for j in range(self.totalLen)]
        while True:
            pre = self.open.get()
            used[pre[2][0]][pre[2][1]] = 1
            self.map[tuple(pre[2])] = len(self.closed)
            self.closed.append(pre)
            # self.imgDB.IMGSave(used)
            for i in range(8):
                # print([pre[2][0] + bearing[i][0], pre[2][1] + bearing[i][1]])
                if pre[2][0] + bearing[i][0] < 0 or pre[2][0] + bearing[i][0] >= self.totalLen or pre[2][1] + \
                        bearing[i][1] < 0 or pre[2][1] + bearing[i][1] >= self.totalLen:
                    continue
                    # 因为有松弛的问题存在，这里不能这么写
                    # invalid和used要分开，并加入松弛
                if used[pre[2][0] + bearing[i][0]][pre[2][1] + bearing[i][1]]:
                    continue
                if not (self.invalid[pre[2][0] + bearing[i][0]][pre[2][1] + bearing[i][1]]):
                    nextStep = [0, pre[1] + 1 + abs(bearing[i][0] * bearing[i][1]) * (2 ** 0.5 - 1),
                                [pre[2][0] + bearing[i][0], pre[2][1] + bearing[i][1]], pre[2]]
                    if nextStep[2] == self.destination:
                        self.closed.append(nextStep)
                        self.map[tuple(nextStep[2])] = len(self.closed)
                        return
                    nextStep[0] = nextStep[1] + calcHeur(nextStep[2], self.destination)
                    used[nextStep[2][0]][nextStep[2][1]] = 1
                    self.open.put(nextStep)
