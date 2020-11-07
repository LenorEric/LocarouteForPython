import csv
import json


class GiveQuery:
    csvName = ""
    matrix = []
    queryCount = 0

    def __init__(self):
        js = open("config.json", 'r')
        jsData = js.read()
        dictData = json.loads(jsData)
        self.csvName = dictData["csvName"]
        self.generateMat()

    def generateMat(self):
        f = open(self.csvName, 'r')
        csvreader = csv.reader(f)
        final_list = list(csvreader)
        for i in range(len(final_list)):
            for j in range(len(final_list[i])):
                final_list[i][j] = float(final_list[i][j])
        self.matrix = final_list

    # 这个报废，别用
    # def queryMat(self, pos, quad):
    #     self.queryCount += 1
    #     retMat = list(self.matrix[pos[0]][pos[1]][quad])
    #     return retMat

    def queryMaxMat(self, pos):
        self.queryCount += 1
        ret = self.matrix[pos[0]][pos[1]]
        return ret


if __name__ == '__main__':
    queryBot = GiveQuery()
    pass
