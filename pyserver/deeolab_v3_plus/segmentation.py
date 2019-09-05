from deeolab_v3_plus.modeling.sync_batchnorm.replicate import patch_replication_callback
from deeolab_v3_plus.modeling.deeplab import *
import torch
import torch.nn
from torchvision import transforms as T
import numpy as np


def transform_val(sample):
    composed_transforms = T.Compose([
        T.Resize(256),
        T.ToTensor(),
        T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
    ])
    return composed_transforms(sample)


class Segmentation(object):
    def __init__(self):
        # whether to use class balanced weights
        self.model = DeepLab(num_classes=8,
                             backbone="xception",
                             output_stride=16,
                             sync_bn=True,
                             freeze_bn=False)

        # Using cuda
        self.model = torch.nn.DataParallel(self.model, device_ids=[0])
        patch_replication_callback(self.model)
        self.model = self.model.cuda()

        self.model.load_state_dict(
            torch.load("models/89_ade20k_xception_512.ckpt", map_location=lambda storage, loc: storage))

    def validation(self, img):
        self.model.eval()
        image = transform_val(img).unsqueeze(0).cuda()
        with torch.no_grad():
            output = self.model(image)
            """return tensor_to_pil(decode_seg_map_sequence(torch.max(output[:3], 1)[1].detach().cpu().numpy()), nrow=1,
                          normalize=False, range=(0, 255))"""
            result = output.data.cpu().numpy()
            prediction = np.argmax(result, axis=1)
            result = prediction[0]
            h, w = result.shape
            rgb = np.empty((h, w, 3), dtype=np.uint8)
            rgb[:, :, 0] = result
            rgb[:, :, 1] = result
            rgb[:, :, 2] = result
            # rgb[rgb != 0] = 255
            return rgb
