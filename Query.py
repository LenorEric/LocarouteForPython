import GiveQuery

# 以下是GiveQuery测试实现方法
# 届时请直接重写GiveQuery接口类的第一个return方法



class Query:
    queryBot = GiveQuery.GiveQuery()
    matrix = [[-1 for i in range(5000)] for j in range(5000)]
    # 这个用不到了，千万别调用
    # def queryData(self, pos, quad):
    #     if -1 in self.matrix[pos[0]][pos[1]]:
    #         self.matrix[pos[0]][pos[1]][quad] = queryBot.queryMat(pos, quad)
    #         return self.matrix[pos[0]][pos[1]][quad]
    #     else:
    #         return list(self.matrix[pos[0]][pos[1]][quad])

    # 唉。。懒得重写接口类了，你们到时候重写Query.QUery.queryMax和GiveQuery.GiveQuery.queryMaxMat吧
    # 或者直接重写Query.Query也行。随便啦
    # 重写的时候记得改写matrix的内容，直接改成640*640吧，反正也只用到queryMax了
    # 总之你们看着办( •̥́ ˍ •̀ू )

    # 不用看着办了，重写GiveQuery.queryMaxMat
    def queryMax(self, pos):
        if self.matrix[pos[0]][pos[1]] == -1:
            self.matrix[pos[0]][pos[1]] = self.queryBot.queryMaxMat(pos)
            return self.matrix[pos[0]][pos[1]]
        else:
            return self.matrix[pos[0]][pos[1]]


# 千万别忘记实例化啊qwq
if __name__ == '__main__':
    qur = Query()
    # print(qur.queryData((10, 10), 1))
