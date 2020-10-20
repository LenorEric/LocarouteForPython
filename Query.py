import GiveQuery

# 以下是GiveQuery测试实现方法
# 届时请直接重写Query接口类的第一个return方法

queryBot = GiveQuery.GiveQuery()


class Query:
    matrix = [[[[-1 for k in range(16)] for p in range(4)] for i in range(640)] for j in range(640)]

    def queryData(self, pos, quad):
        if -1 in self.matrix[pos[0]][pos[1]]:
            self.matrix[pos[0]][pos[1]][quad] = queryBot.queryMat(pos, quad)
            return self.matrix[pos[0]][pos[1]][quad]
        else:
            return list(self.matrix[pos[0]][pos[1]][quad])


# 千万别忘记实例化啊qwq
if __name__ == '__main__':
    qur = Query()
    print(qur.queryData((10, 10), 1))
