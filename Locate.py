import json
# 千万别忘记实例化啊啊啊呜qwq
import GiveQuery
import Query
import json
import math
import numpy as np
import Fit


class Locate(Query.Query):
    # Const is here
    totalLen = 0
    groupLen = 0
    coreLen = 0
    coreThre = 0  # 0 of max percent(0~1)
    maxCore = 0
    coreRadius = 0
    disturange = 0
    coreThreDis = 0
    coreLenThre = 0

    # Save Calc Result here
    counts = [0 for i in range(6)]
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
        self.framePos[2] = self.framePos[3] = self.totalLen
        self.groupLen = dictData["groupLen"]
        self.coreLen = dictData["coreLen"]
        self.coreThre = dictData["coreThre"]
        self.maxCore = dictData["maxCore"]
        self.coreLenThre = dictData["coreLenThre"]
        self.inCore = [[0 for i in range(self.totalLen)] for j in range(self.totalLen)]
        self.coreRadius = self.coreLen / 2
        self.disturange = dictData["disturange"]
        self.coreThreDis = dictData["coreThreDis"]

    def scanMax(self, begin):
        def calcG(subArea):
            g = [0, 0]
            dev = 0
            for i in range(len(subArea)):
                for j in range(len(subArea[i])):
                    if subArea[i][j]:
                        g = [g[0] + i, g[1] + j]
                        dev += 1
            return [[g[0] // dev, g[1] // dev], dev]

        def begin2TL(begin):
            tl = [begin[0] - self.coreRadius, begin[1] - self.coreRadius]
            return tl

        def mapGlobal2Sub(begin, glo):
            sub = [glo[0] - begin2TL(begin)[0], glo[1] - begin2TL(begin)[1]]
            return sub

        def mapSub2Glb(begin, sub):
            cent = [(cL - 1) / 2, (cL - 1) / 2]
            glb = [begin[0] + sub[0] - cent[0], begin[1] + sub[1] - cent[1]]
            glb = list(map(int, glb))
            return glb

            # 此处可以加入越界检查，或者别的地方加入
            # 算了，不加了

        def stepPresent(present, seStep, angle):
            step = [round(present[0] + self.coreLen / seStep * math.cos(angle)),
                    round(present[1] + self.coreLen / seStep * math.sin(angle))]
            return step

        def poli2Lin(point, angle):
            tang = math.tan(angle)
            return [tang, point[1] - tang * point[0]]

        def poli2Ord(point, angle):
            tang = math.tan(angle)
            return [tang, -1, point[1] - tang * point[0]]

        # 0 代表在直线下方， >0代表在直线上或者在直线上
        def dirPointLine(point, line):
            # 一般式
            # d = line[0] * point[0] + line[1] * point[1] + line[2]
            # 点斜式
            d = point[1] - line[0] * point[0] - line[1]
            d = np.sign(d) + 1
            return d

        def carveSubArea(subArea, bearing, present):
            line = [poli2Lin(present, angle[i]) for i in range(3)]
            for i in range(len(subArea)):
                for j in range(len(subArea[i])):
                    if not (subArea[i][j]):
                        continue
                    if bearing == 0:
                        if dirPointLine([i, j], line[1]) or not (dirPointLine([i, j], line[2])):
                            subArea[i][j] = 0
                    elif bearing == 1:
                        if dirPointLine([i, j], line[2]) or dirPointLine([i, j], line[0]):
                            subArea[i][j] = 0
                    elif bearing == 2:
                        if not (dirPointLine([i, j], line[0]) and dirPointLine([i, j], line[1])):
                            subArea[i][j] = 0
            return subArea

        if self.coreLen % 2:
            cL = self.coreLen
        else:
            cL = self.coreLen + 1
        # 确保sebArea是奇数，这样有一个真中心点
        subArea = [[1 for i in range(cL)] for j in range(cL)]
        # present = mapGlobal2Sub(begin, begin)
        # 0, 120, 240
        angle = [0, 2.0943951023931953, 4.1887902047863905]
        # 下面这两句写错了
        seStep = 8
        lastBearing = -1
        qPresent = [0, 0, 0]
        while True:
            g = calcG(subArea)
            if g[1] <= self.disturange:
                break
            else:
                present = g[0]
                for i in range(3):
                    self.counts[0] += 1
                    qPresent[i] = self.queryMax(mapSub2Glb(begin, stepPresent(present, seStep, angle[i])))
                bearing = qPresent.index(min(qPresent))
                subArea = carveSubArea(subArea, bearing, present)
                if bearing == lastBearing:
                    # 这里收缩的方法可以更改
                    seStep *= 1.718
                else:
                    seStep *= 1.1
                lastBearing = bearing
        maxD = 0
        centCir = [0, 0]
        # 这里貌似不是很精细，但是管不了那么多啦， disturange大一点就好qwq
        for i in range(len(subArea)):
            for j in range(len(subArea[i])):
                if subArea[i][j]:
                    if maxD < self.queryMax(mapSub2Glb(begin, [i, j])):
                        maxD = self.queryMax(mapSub2Glb(begin, [i, j]))
                        # 这边是映射到全局地址
                        centCir = [i + begin[0] - self.coreRadius, j + begin[1] - self.coreRadius]
        return centCir

    def scanCircle(self, maxPoint):
        def ntIter(angle, initStep, initPoint):

            def asp2GP(angle, step, point):
                ret = [point[0] + step * math.cos(angle), point[1] + step * math.sin(angle)]
                ret = list(map(round, ret))
                return ret

            iterPoint = initPoint
            mnStep = initStep
            mxStep = self.coreLen
            while abs(
                    self.queryMax(asp2GP(angle, (mnStep + mxStep) / 2,
                                         iterPoint)) - self.coreLenThre * self.maxCore) > self.coreThreDis:
                if self.queryMax(asp2GP(angle, (mnStep + mxStep) / 2, iterPoint)) - self.coreLenThre * self.maxCore > 0:
                    mnStep = (mnStep + mxStep) / 2
                else:
                    mxStep = (mnStep + mxStep) / 2
            return asp2GP(angle, (mnStep + mxStep) / 2, iterPoint)

        precision = 6
        seStep = 3
        pointList = []
        # 如果maxPoint离圆心偏离较大，这里可以加入动态算法
        for i in range(precision):
            angle = math.pi / precision * i * 2
            pointList.append(ntIter(angle, self.coreLen / seStep, maxPoint))
        circle = Fit.circle(pointList)
        return circle

    def roughScan(self):
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

        seStep = 5
        for i in range(0, self.totalLen, round(self.groupLen / seStep)):
            for j in range(0, self.totalLen, round(self.groupLen / seStep)):
                if self.inCore[i][j]:
                    continue
                # 必须保证给定的coreThre足够小，使得所有超过阈值的点都在以coreRadius为半径的圆中
                self.counts[3] += 1
                if self.queryMax([i, j]) > self.coreThre * self.maxCore:
                    maxPoint = list(map(round, self.scanMax([i, j])))
                    self.maxPoint.append(maxPoint)
                    circ = self.scanCircle(maxPoint)
                    self.inCore = circle(self.inCore, *circ)
                    self.coreList.append(circ)


if __name__ == '__main__':
    loca = Locate()
