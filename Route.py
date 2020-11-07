import AStar
import json
import queue
import cv2
from copy import deepcopy as dcp
import ImageOutput


class Route:
    start = []
    destination = []
    routeList = []
    invalid = []
    maxPoint = []

    def __init__(self, invalid, maxPoint):
        js = open("config.json", 'r')
        jsData = js.read()
        dictData = json.loads(jsData)
        self.maxPoint = maxPoint
        self.start = maxPoint[int(dictData["start"])]
        for i in range(len(maxPoint)):
            if i != dictData["start"]:
                self.destination.append(maxPoint[i])
        self.invalid = dcp(invalid)


    def minusInvalid(self, start, dest):
        # 纤芯不能在边界，否则会越界
        def deColor(invalid, point):
            processList = queue.Queue()
            processList.put(point)
            bearing = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
            while not (processList.empty()):
                present = processList.get()
                invalid[present[0]][present[1]] = 0
                for i in range(8):
                    if invalid[present[0] + bearing[i][0]][present[1] + bearing[i][1]]:
                        processList.put([present[0] + bearing[i][0], present[1] + bearing[i][1]])
                        invalid[present[0] + bearing[i][0]][present[1] + bearing[i][1]] = 0

        retInvalid = dcp(self.invalid)
        deColor(retInvalid, start)
        deColor(retInvalid, dest)
        # ImageOutput.IMGOutput(retInvalid)
        return retInvalid

    def calcRoute(self):
        count = 0
        for dest in self.destination:
            count += 1
            print("Route", count)
            calcor = AStar.AStar(self.minusInvalid(self.start, dest), self.start, dest)
            calcor.bfs()
            calcor.generoute()
            self.routeList.append(calcor.route)
            del calcor
