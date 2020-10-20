import json
# 千万别忘记实例化啊啊啊呜qwq
import GiveQuery
import Query
import json

queryBot = GiveQuery.GiveQuery()


class Locate(Query.Query):
    # Const is here
    totalLen = 0
    groupLen = 0
    coreLen = 0
    coreThre = 0   #0 of 100 percent(0~1)

    # Save Calc Result here
    framePos = [0, 0, 0, 0]  # top left right bottom

    def __init__(self):
        js = open("config.json", 'r')
        jsData = js.read()
        dictData = json.loads(jsData)
        self.totalLen = dictData["totaoLen"]
        self.framePos[3] = self.framePos[4] = self.totalLen
        self.groupLen = dictData["groupLen"]
        self.coreLen = self.groupLen/5
        self.coreThre = dictData["coreThre"]


    def roughScan(self):
        seStep = 3
        for i in range(self.framePos[3], self.groupLen/seStep):
            for j in range(self.framePos[2], self.groupLen/seStep):
                if self.queryData((i, j), )


if __name__ == '__main__':
    loca = Locate()
    print(loca.queryData((12, 2), 4))
