import Locate

if __name__ == '__main__':
    locater = Locate.Locate()
    locater.roughScan()
    print(len(locater.coreList))
