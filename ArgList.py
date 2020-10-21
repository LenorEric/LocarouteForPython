import json


class ArgList:
    # Const is here
    args = {}
    # totalLen = 0
    # groupLen = 0
    # coreLen = 0
    # coreThre = 0  # 0 of 100 percent(0~1)

    def __init__(self):
        self.getArg()

    def getArg(self):
        js = open("config.json", 'r')
        jsData = js.read()
        self.args = json.loads(jsData)
        # self.totalLen = self.args["totaoLen"]
        # self.framePos[3] = self.framePos[4] = self.totalLen
        # self.groupLen = self.args["groupLen"]
        # self.coreLen = self.groupLen / 5
        # self.coreThre = self.args["coreThre"]
