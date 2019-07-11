
import sys
sys.path.append('../')
from maskrcnn_benchmark.config import cfg
from predictor_bbox import COCODemo
import cv2
import os
import time
import torch
import numpy as np
import json
import copy
# from PIL import Image
torch.cuda.set_device(1)
config_file = "../configs/e2e_faster_rcnn_R_101_FPN_1x_my_1.yaml"
cfg.merge_from_file(config_file)
cfg.merge_from_list(["MODEL.DEVICE", "cuda"])
cfg.MODEL.WEIGHT="../model_final_24000_finetune_Cleaned_5.pth"
coco_demo = COCODemo(
    cfg,
    min_image_size=800,
    confidence_threshold=0.3,
)
video_path="./Video/VIRAT_S_000200_02_000479_000635.mp4"
json_dir= './jsonDatasets'
if not os.path.exists(json_dir):
    os.mkdir(json_dir)

image_dir='./imagesDatasets'
if not os.path.exists(image_dir):
    os.mkdir(image_dir)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


camera=cv2.VideoCapture(video_path)
frameN=0
while True:
    res,image=camera.read()
    if not res:
        break
    frameN+=1

    image_path=os.path.join(image_dir,str(frameN)+'.jpg')
    cv2.imwrite(image_path,image)

    frame_json = {}.fromkeys(('predictions', 'ImageId'))
    predictions_dic = {}.fromkeys(('BoxId', 'LabelId', 'box'))
    frame_json['predictions'] = []
    frame_json['ImageId'] = []

    scores, labels, boxes= coco_demo.run_on_opencv_image(image)
    BboxNum = len(scores)
    for i in range(BboxNum):
        predictions_dic['BoxId'] = i + 1
        predictions_dic['LabelId'] = labels[i]
        predictions_dic['box'] = [boxes.numpy()[i, 0], boxes.numpy()[i, 1], boxes.numpy()[i, 2],   boxes.numpy()[i, 3]]
        frame_json['predictions'].append(copy.deepcopy(predictions_dic))

    frame_json['ImageId']=frameN

    json_path=os.path.join(json_dir,str(frameN)+'.json')
    with open(json_path, 'w', encoding='utf8') as f:
        f.write(json.dumps(frame_json, cls = MyEncoder, ))





