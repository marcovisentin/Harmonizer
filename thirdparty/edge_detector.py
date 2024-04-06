import kornia as kn
import argparse
from pidinet import models
import torch
from dataclasses import dataclass

def get_edge(img):
    #img [1,3,512,512]
    filter = kn.filters.Sobel()
    img_edge = filter(img)

    return img_edge #[1,1,512,512]


@dataclass
class PidinetConfig:
    pidinet_model: str = 'pidinet_tiny'
    sa: bool = True  # Note: store_false means the default is True, but for clarity in dataclasses, we'll invert it and handle the logic in code.
    dil: bool = True  # Similar to 'sa', handle the inversion in your application logic.
    config: str = 'carv4'
    evaluate: str = "thirdparty/pidinet/trained_models/table5_pidinet-tiny.pth"
    gpu: int = 0
pidnet_args = PidinetConfig() # NOTE: I changed it to a dataclass because the parser was creating conflicts

# '''PidiNet egge detector'''
# parser = argparse.ArgumentParser(description='PyTorch Pixel Difference Convolutional Networks')
# parser.add_argument('--pidinet_model', type=str, default='pidinet_tiny',
#         help='model to train the dataset')
# parser.add_argument('--sa', action='store_false',
#         help='use CSAM in pidinet')
# parser.add_argument('--dil', action='store_false',
#         help='use CDCM in pidinet')
# parser.add_argument('--config', type=str, default='carv4',
#         help='model configurations, please refer to models/config.py for possible configurations')
# parser.add_argument('--evaluate', type=str, default="thirdparty/pidinet/trained_models/table5_pidinet-tiny.pth",
#         help='full path to checkpoint to be evaluated')
# parser.add_argument('--gpu', type=str, default='0', help='gpus available')

# pidnet_args_2 = parser.parse_args()

def Initialize_PidNet(args):
    ### Create model
    model = getattr(models, args.pidinet_model)(args)

    ###Transfor to cuda devices
    model = torch.nn.DataParallel(model).cuda()

    ###load model
    state = torch.load(args.evaluate, map_location='cpu')
    model.load_state_dict(state['state_dict'])
    return model

def PidNet(model,img):
    _,_,H,W = img.shape
    with torch.no_grad():
        results = model(img)
        result = results[-1]
    return result

# Calculate the original's edge map.
pidnet = Initialize_PidNet(pidnet_args)