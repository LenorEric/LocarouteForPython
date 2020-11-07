import Locate
import numpy as np
import cv2
import Route

if __name__ == '__main__':
    locater = Locate.Locate()
    locater.roughScan()

    # 测试locate
    # print(locater.queryBot.queryCount)
    # print(locater.counts)
    # print(len(locater.maxPoint))
    # img = np.array(locater.inCore, dtype=np.uint8)
    # img = cv2.merge([img*200, img*200, img*200])
    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    # 测试route
    router = Route.Route(locater.inCore, locater.maxPoint)
    router.calcRoute()
    print(router.routeList)
