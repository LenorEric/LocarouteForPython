import GiveQuery

queryBot = GiveQuery.GiveQuery()

if __name__ == '__main__':
    pos = [[40 for i in range(2)] for j in range(16)]
    queryList = queryBot.queryMat(pos, 1)
    for i in range(16):
        print(queryList[i])
