import datetime
import sys
sys.path.append('../')
from maskrcnn_benchmark.config import cfg
from predictor_bbox import COCODemo
from maskrcnn_benchmark.utils.logger import setup_logger
from maskrcnn_benchmark.utils.comm import get_rank
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
# video_dir="./Video"
# json_dir = './Video_json'
video_dir="/raid/data/backup/challenge/stabilizationVideo/All_Data"
json_dir_ed= "/raid/data/backup/challenge/stabilizationVideo/Video_json"
json_dir= "/raid/data/backup/challenge/stabilizationVideo/Video_json_1"
if not os.path.exists(json_dir):
    os.mkdir(json_dir)

videos=os.listdir(video_dir)
jsons_ed=os.listdir(json_dir_ed)
for json_ed in jsons_ed:
    videos.remove(json_ed[:-5]+'.mp4')
video_id = 0

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

logger = setup_logger("bbox_prediction", '.', get_rank())     # 创建日志文件 log.txt

for video in videos:
    video_id+=1
    # print('Dealing with '+ str(video_id)+ 'th video')
    
    logger.info('Dealing with '+ str(video_id) + 'th video:{}'. format(video))

    video_path=os.path.join(video_dir,video)

    start_time=time.time()

    camera = cv2.VideoCapture(video_path)

    video_json = {}.fromkeys(('predictions', 'image_num'))
    predictions_dic = {}.fromkeys(('ImageId', 'BoxId', 'LabelId', 'box'))
    video_json['predictions'] = []
    video_json['image_num'] = []

    frameN=0
    while True:
        res,image=camera.read()
        if not res:
            break
        frameN+=1
    
        scores, labels, boxes= coco_demo.run_on_opencv_image(image)
        BboxNum = len(scores)
        for i in range(BboxNum):
            predictions_dic['ImageId'] = frameN
            predictions_dic['BoxId'] = i + 1
            predictions_dic['LabelId'] = labels[i]
            predictions_dic['box'] = [boxes.numpy()[i, 0], boxes.numpy()[i, 1], boxes.numpy()[i, 2], boxes.numpy()[i, 3],
                                  scores[i]]
            video_json['predictions'].append(copy.deepcopy(predictions_dic))

    video_json['image_num']=frameN

    json_start = time.time()
    with open(os.path.join(json_dir,video[:-4]+'.json'), 'w', encoding='utf8') as f:
        f.write(json.dumps(video_json, cls = MyEncoder, ))


    json_end = time.time()
    end_time = time.time()

    logger.info('processing time: {}'. format(datetime.timedelta(seconds=end_time-start_time)))
    logger.info('json time: {}' . format(datetime.timedelta(seconds =json_end - json_start)))
    # print('processing time: ', datetime.timedelta(seconds=end_time-start_time))
    # print('json time: ' , datetime.timedelta(seconds =json_end - json_start))


