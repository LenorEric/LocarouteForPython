from numpy import *
from scipy import optimize


def circle(coordinates):
    # 因为namespace缘故写到函数内部
    # 计算误差
    def f_2(c):
        Ri = sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2)
        return Ri - Ri.mean()

    x = []
    y = []
    # 分别计算
    for coordinate in coordinates:
        x.append(coordinate[0])
        y.append(coordinate[1])
    x = array(x)
    y = array(y)
    x_m = mean(x)
    y_m = mean(y)
    center_estimate = x_m, y_m
    # 最小二乘法
    center_2, _ = optimize.leastsq(f_2, center_estimate)
    xc_2, yc_2 = center_2
    # 拟合半径（给定的coord中的点到圆心的距离的算数平均值），本质上也算一次最小二乘法吧
    Ri_2 = sqrt((x - xc_2) ** 2 + (y - yc_2) ** 2)
    R_2 = int(Ri_2.mean())
    return [list(map(int, [xc_2, yc_2])), R_2]


if __name__ == '__main__':
    coord = [[36, 14], [36, 10], [19, 28], [18, 31], [33, 18], [26, 26]]
    for i in range(64):
        print(circle(coord))
