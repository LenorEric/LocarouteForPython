import AStar
import json


class Route:
    start = []
    destination = []
    routeList = []
    invalid = []

    def __init__(self, invalid, maxPoint):
        js = open("config.json", 'r')
        jsData = js.read()
        dictData = json.loads(jsData)
        self.start = maxPoint[int(dictData["start"])]
        for i in range(len(maxPoint)):
            if i != dictData["start"]:
                self.destination.append(maxPoint[i])
        self.invalid = invalid

    def calcRoute(self):
        for dest in self.destination:
            calcor = AStar.AStar(self.invalid, self.start, dest)
            calcor.bfs()
            calcor.generoute()
            self.routeList.append(calcor.route)
