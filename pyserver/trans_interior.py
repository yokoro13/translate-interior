from PIL import Image
from deeolab_v3_plus.segmentation import Segmentation
from starGAN.StarGAN import translate_interior
from util import cv2_to_pil, pil_to_cv2
import cv2
import numpy as np
import time


class TransInterior(object):
    def __init__(self):
        self.deeplab = Segmentation()
        self.target_labels = [0, 0, 0, 0, 0, 0, 0, 0]
        self.mask_target = []

    def set_target_labels(self, labels):
        self.target_labels = [0, 0, 0, 0, 0, 0, 0, 0]

        for label in labels:
            self.target_labels[int(label)] = 1
        self.set_mask_target()

    def set_mask_target(self):
        self.mask_target = []
        for i, label in enumerate(self.target_labels):
            if label == 1:
                # img_mask == 0:none 1:wall 2:floor 3:ceiling 4:table 5:certain 6:chair 7:shelf
                if i in [0, 2, 4, 6] and 2 not in self.mask_target:
                    self.mask_target.append(2)
                elif i in [1, 3, 5, 7] and 1 not in self.mask_target:
                    self.mask_target.append(1)
                if i in [7]:
                    self.mask_target.append(3)

    def segmentation(self, img):
        return self.deeplab.validation(img)

    def trans_interior(self, img_org):
        """
        :param img_org: PIL Image
        :return: PIL Image
        """
        w, h = img_org.size

        # translation
        start = time.time()
        img_trans = translate_interior(img_org, self.target_labels)
        img_trans = cv2.cvtColor(img_trans, cv2.COLOR_RGB2BGR)
        img_trans = cv2.resize(img_trans, (w, h))
        print("trans: {}".format(time.time() - start))

        # segmentation
        start = time.time()
        img_mask = self.segmentation(img_org)
        img_mask = cv2.resize(img_mask, (w, h), interpolation=cv2.INTER_NEAREST)
        print("seg: {}".format(time.time() - start))

        img_org = pil_to_cv2(img_org)

        # merge images
        start = time.time()
        result = np.zeros_like(img_mask)
        for target in self.mask_target:
            result += np.where(img_mask == target, img_trans, 0)
        result += np.where(result == 0, img_org, 0)
        print("mask: {}".format(time.time() - start))

        return cv2_to_pil(result)

    def test_segmentation(self, img):
        """
        :param img: PIL Image
        :return: PIL Image
        """
        return cv2_to_pil(self.segmentation(img))

    def test_translation(self, img):
        """
        :param img: PIL Image
        :return: PIL Image
        """
        return cv2_to_pil(cv2.cvtColor(translate_interior(img, self.target_labels), cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    img_path = "./images/03755.jpg"
    input_img = Image.open(img_path)
    c_trg = [6]
    trans = TransInterior()
    trans.set_target_labels(c_trg)

    # result = trans.trans_interior(input_img)
    result = trans.test_translation(input_img)
    result.save("aaa.png")
