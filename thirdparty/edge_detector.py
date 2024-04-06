import kornia as kn
import argparse
from thirdparty.pidinet import models
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
    sa: bool = False  # Note: store_false means the default is True, but for clarity in dataclasses, we'll invert it and handle the logic in code.
    dil: bool = False  # Similar to 'sa', handle the inversion in your application logic.
    config: str = 'carv4'
    evaluate: str = "thirdparty/pidinet/trained_models/table5_pidinet-tiny.pth"
    gpu: str = '0'

pidnet_args = PidinetConfig() # NOTE: I changed it to a dataclass because the parser was creating conflicts

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