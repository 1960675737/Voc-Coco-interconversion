# import sys
# sys.path.append('../')
# from maskrcnn_benchmark.config import cfg
# from predictor import COCODemo
# from PIL import Image
# import numpy as np
# config_file = "../configs/e2e_faster_rcnn_R_101_FPN_1x_my_1.yaml"
# cfg.merge_from_file(config_file)
# cfg.merge_from_list(["MODEL.DEVICE", "cpu"])
# cfg.MODEL.WEIGHT="../model_final_24000_finetune_Cleaned_5.pth"
# coco_demo = COCODemo(
#     cfg,
#     min_image_size=800,
#     confidence_threshold=0.7,
# )
# image="./2.jpg"
# pil_image=Image.open(image).convert("RGB")
# image=np.array(pil_image)[:,:,[2,1,0]]
# predictions = coco_demo.run_on_opencv_image(image)
# print(predictions[1])

# inference simple video bbox prediction
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
video_path="./VIRAT_S_000201_03_000640_000672.mp4"
json_dir = 'Video_json.json'

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


video_json = {}.fromkeys(('predictions', 'image_num'))
predictions_dic = {}.fromkeys(('ImageId', 'BoxId', 'LabelId', 'box'))
video_json['predictions'] = []
video_json['image_num'] = []
start_time=time.time()
camera=cv2.VideoCapture(video_path)
frameN=0
while True:
    res,image=camera.read()
    if not res:
        break
    frameN+=1
    # pil_image = Image.open(image).convert("RGB")
    # image=np.array(pil_image)[:,:,[2,1,0]]
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
with open(json_dir, 'w', encoding='utf8') as f:
    f.write(json.dumps(video_json, cls = MyEncoder, ))


json_end = time.time()
end_time = time.time()

print('processing time: '+ str(end_time-start_time))
print('json time: ' + str(json_end - json_start))


