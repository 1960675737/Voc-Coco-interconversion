# 将Voc格式的xml标注的文件转换为Coco格式的json标注文件

## getData.py

将txt文件里面指定的训练和测试文件从初始数据集文件夹中提取出来，训练数据放一个文件夹，测试数据放一个文件夹。

## voc2coco.py

将voc数据的标注文件.xml文件转化为coco数据集的标注文件.json文件。

## json_corrected.py
 
调整json文件，删除无用类别。
