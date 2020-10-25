import AStar


class Route:
    start = []
    destination = []
    routeList = []
    invalid = []

    def __init__(self, start, dest, invalid):
        self.destination = dest
        self.start = start
        self.invalid = invalid

    def calcRoute(self):
        for i in range(self.destination):
            calcor = AStar.AStar(self.invalid, self.start, self.destination[i])
            calcor.bfs()
            calcor.generoute()
            self.routeList.append(calcor.route)
