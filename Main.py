import Locate
import ImageOutput
import Route
from copy import deepcopy as dcp
import numpy as np

if __name__ == '__main__':
    print("Locating Core")
    locater = Locate.Locate()
    locater.roughScan()

    # 测试locate
    # print(locater.queryBot.queryCount)
    # print(locater.maxPoint)
    # print(list(map(lambda lst: lst[0], locater.coreList)))
    # locSum = dcp(locater.inCore)
    # for p in locater.maxPoint:
    #     locSum[p[0]][p[1]] = 2
    # ImageOutput.IMGOutput(locSum)

    print("Calcing Route")
    router = Route.Route(dcp(locater.inCore), locater.maxPoint)
    router.calcRoute()
    # 测试route

    # print(router.routeList)
    # routeSum = [[(locater.inCore[i][j]*2) for j in range(len(locater.inCore[i]))] for i in range(len(locater.inCore))]
    # for route in router.routeList:
    #     for point in route:
    #         routeSum[point[0]][point[1]] = 1
    # ImageOutput.IMGOutput(routeSum)
