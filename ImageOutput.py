import numpy as np
import cv2


def IMGOutput(ary):
    img = np.array(ary, dtype=np.uint8)
    img = cv2.merge([img * 120, img * 120, img * 120])
    cv2.imshow("img", img)
    cv2.waitKey(0)


def IMGSave(ary):
    img = np.array(ary, dtype=np.uint8)
    img = cv2.merge([img * 120, img * 120, img * 120])
    name = "img.jpg"
    cv2.imwrite(name, img)


class IMGDebugger():
    count = 0

    def IMGSave(self, ary):
        if not (self.count % 1):
            img = np.array(ary, dtype=np.uint8)
            img = cv2.merge([img * 120, img * 120, img * 120])
            name = ".\\imgDebug\\" + str(self.count) + ".jpg"
            cv2.imwrite(name, img)
        self.count += 1


if __name__ == '__main__':
    pass
