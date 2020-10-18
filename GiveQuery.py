class GiveQuery:
    matrix = [[0 for i in range(640)] for j in range(640)]
    queryCount = 0

    def __init__(self):
        self.generateMat()

    def generateMat(self):
        pass

    def queryMat(self, pos, quad):
        self.queryCount += 1
        retMat = []
        for i in range(16):
            retMat.append(self.matrix[(quad % 2 * 4 + i % 4)*80+pos[i][0]][(quad // 2 * 4 + i // 4)*80+pos[i][0]])
        return retMat
