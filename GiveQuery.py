class GiveQuery:
    matrix = [[[[0 for k in range(16)] for p in range(4)] for i in range(640)] for j in range(640)]
    queryCount = 0

    def __init__(self):
        self.generateMat()

    def generateMat(self):
        pass

    def queryMat(self, pos, quad):
        self.queryCount += 1
        retMat = list(self.matrix[pos[0]][pos[1]][quad])
        return retMat
