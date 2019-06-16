# 将Voc格式的xml标注的文件转换为Coco格式的json标注文件

## getData.py

将txt文件里面指定的训练和测试文件从初始数据集文件夹中提取出来，训练数据放一个文件夹，测试数据放一个文件夹。

## voc2coco.py

将voc数据的标注文件.xml文件转化为coco数据集的标注文件.json文件。

## json_corrected.py
 
调整json文件，删除无用类别。

## trim.py

调整COCO预训练模型用于其他数据集微调训练。将.pkl格式的预训练权重文件删除最后的分类全连接层权重，保存为.pth格式权重文件，然后用自己的数据集微调模型。预训练模型只能为.pkl文件

## trim_detection_model.py

删除.pth格式权重文件的部分层权重。
