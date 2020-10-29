import json
# 千万别忘记实例化啊啊啊呜qwq
import GiveQuery
import Query
import json
import math
import numpy as np
import Fit


# 此处可以优化
def circle(sqr, cent, radius):
    sq = list(sqr)
    for x in range(cent[0] - radius, cent[0] + radius):
        for y in range(cent[1] - radius, cent[1] + radius):
            # x是行，y是列
            if x < 0 or y < 0 or y > len(sqr[0]) or x > len(sqr):
                continue
            elif (cent[0] - x) ** 2 + (cent[1] - y) ** 2 <= radius ** 2:
                sq[x][y] = 1
    return sq


def calcG(subArea):
    g = [0, 0]
    dev = 0
    for i in range(len(subArea)):
        for j in range(len(subArea[i])):
            if subArea:
                g = [g[0] + i, g[1] + j]
                dev += 1
    return [[g[0] // dev, g[1] // dev], dev]


class Locate(Query.Query):
    # Const is here
    totalLen = 0
    groupLen = 0
    coreLen = 0
    coreThre = 0  # 0 of max percent(0~1)
    maxCore = 0
    coreRadius = 0
    disturange = 0

    # Save Calc Result here

    framePos = [0, 0, 0, 0]  # top left right bottom  # Perhaps unused, may be deleted later
    inCore = []
    # maxPoint和coreList的序列必须一一对应
    maxPoint = []
    # [[x, y], radius]
    coreList = []

    def __init__(self):
        js = open("config.json", 'r')
        jsData = js.read()
        dictData = json.loads(jsData)
        self.totalLen = dictData["totalLen"]
        self.framePos[3] = self.framePos[4] = self.totalLen
        self.groupLen = dictData["groupLen"]
        self.coreLen = self.groupLen / 5
        self.coreThre = dictData["coreThre"]
        self.maxCore = dictData["maxCore"]
        self.inCore = [[0 for i in range(self.totalLen)] for j in range(self.totalLen)]
        self.coreRadius = self.coreLen / 2
        self.disturange = dictData["disturange"]

    def scaCent(self, begin):
        def begin2TL(begin):
            tl = [begin[0] - self.coreRadius, begin[1] - self.coreRadius]
            return tl

        def mapGlobal2Sub(begin, glo):
            sub = [glo[0] - begin2TL(begin)[0], glo[1] - begin2TL(begin)[1]]
            return sub

        # 此处可以加入越界检查，或者别的地方加入
        def stepPresent(present, seStep, angle):
            step = [round(present[0] + self.coreLen / seStep * math.cos(angle)),
                    round(present[1] + self.coreLen / seStep * math.sin(angle))]
            return step

        def poli2Ord(point, angle):
            tang = math.tan(angle)
            return [tang, -1, point[1] - tang * point[0]]

        # 0 代表在直线下方， >0代表在直线上或者在直线上
        def dirPointLine(point, line):
            d = line[0] * point[0] + line[1] * point[1] + line[2]
            d = np.sign(d) + 1
            return d

        def carveSubArea(subArea, bearing, present):
            line = [poli2Ord(present, angle[i]) for i in range(3)]
            for i in range(subArea):
                for j in range(subArea[i]):
                    if not (subArea[i][j]):
                        continue
                    for line in range(2):
                        if bearing == 0:
                            if dirPointLine([i, j], line[1]) or not (dirPointLine([i, j], line[2])):
                                subArea[i][j] = 0
                        elif bearing == 1:
                            if dirPointLine([i, j], line[2]) or dirPointLine([i, j], line[0]):
                                subArea[i][j] = 0
                        elif bearing == 2:
                            if not(dirPointLine([i, j], line[0]) or dirPointLine([i ,j], line[1])):
                                subArea[i][j] = 0
            return subArea

        subArea = [[1 for i in range(self.coreLen)] for j in range(self.coreLen)]
        present = mapGlobal2Sub(begin, begin)
        # 0, 120, 240
        angle = [0, 2.0943951023931953, 4.1887902047863905]
        # 下面这两句写错了
        # angleStep = [angle[0] + angle[1], angle[1] + angle[2], angle[2] + math.pi * 2]
        # angleStep = list(map(lambda ang: ang / 2, angleStep))
        seStep = 5
        lastBearing = 0
        qPresent = [0, 0, 0]
        while True:
            g = calcG(subArea)
            if g[2] <= self.disturange:
                break
            else:
                for i in range(3):
                    qPresent[i] = self.queryMax(stepPresent(present, seStep, angle[i]))
                bearing = qPresent.index(min(qPresent))
                subArea = carveSubArea(subArea, bearing, present)
                if bearing == lastBearing:
                    # 这里收缩的方法可以更改
                    seStep *= 1.718
                    seStep = round(seStep)
                lastBearing = bearing
                present = g[0]
        maxD = 0
        centCir = [0, 0]
        # 这里貌似不是很精细，但是管不了那么多啦， disturange大一点就好qwq
        for i in range(len(subArea)):
            for j in range(len(subArea[i])):
                if maxD < self.queryMax([i + begin[0] - self.coreRadius, j + begin[1] - self.coreRadius]):
                    maxD = self.queryMax([i + begin[0] - self.coreRadius, j + begin[1] - self.coreRadius])
                    # 这边是映射到全局地址
                    centCir = [i + begin[0] - self.coreRadius, j + begin[1] - self.coreRadius]
        return centCir

    def roughScan(self):
        seStep = 3
        for i in range(self.framePos[3], self.groupLen / seStep):
            for j in range(self.framePos[2], self.groupLen / seStep):
                if self.inCore[i][j]:
                    continue
                # 必须保证给定的coreThre足够小，使得所有超过阈值的点都在以coreRadius为半径的圆中
                if self.queryMax([i, j]) > self.coreThre * self.maxCore:
                    cent = self.scaCent([i, j])
                    self.inCore = circle(self.inCore, cent, self.coreRadius)
                    self.coreList.append(cent)


if __name__ == '__main__':
    loca = Locate()
