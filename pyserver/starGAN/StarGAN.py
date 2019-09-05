from util import pil_to_tensor, tensor_to_cv2
import torch
import torch.nn
from starGAN.network import Generator

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
c_dim = 8 # ラベル数
G = Generator(c_dim=c_dim)
G = G.to(device)
G = torch.nn.DataParallel(G)
G.load_state_dict(torch.load("./models/110000-G-sky256.ckpt", map_location=lambda storage, loc: storage))

def translate_interior(input_img, c):
    c_trg = torch.Tensor([c]).to(device)
    input_img = pil_to_tensor(input_img)

    with torch.no_grad():
        x_real = G(input_img, c_trg)
        return tensor_to_cv2(x_real.data.cpu())

