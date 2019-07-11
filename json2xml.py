import xml.dom
import xml.dom.minidom
import os
# from PIL import Image
import cv2
import json
_IMAGE_PATH = './imagesDatasets'
 
_INDENT = '' * 4
_NEW_LINE = '\n'
_FOLDER_NODE = 'VideoFrame'                       # 文件节点
_ROOT_NODE = 'annotation'
_DATABASE_NAME = ''
_ANNOTATION = 'COCO'
_AUTHOR = 'X'
_SEGMENTED = '0'
_DIFFICULT = '0'
_TRUNCATED = '0'
_POSE = 'Unspecified'
 
# _IMAGE_COPY_PATH= 'JPEGImages'
_ANNOTATION_SAVE_PATH = './xmlDataset'
# 封装创建节点的过程
def createElementNode(doc, tag, attr):  # 创建一个元素节点
    element_node = doc.createElement(tag)
 
    # 创建一个文本节点
    text_node = doc.createTextNode(attr)
 
    # 将文本节点作为元素节点的子节点
    element_node.appendChild(text_node)
 
    return element_node
def createChildNode(doc, tag, attr, parent_node):
    child_node = createElementNode(doc, tag, attr)
 
    parent_node.appendChild(child_node)
# object节点比较特殊
def createObjectNode(doc, attrs):
    object_node = doc.createElement('object')
    print("创建object中")
    midname = className[attrs["LabelId"]]
 
    createChildNode(doc, 'name', midname,
                    object_node)
    createChildNode(doc, 'pose',
                    _POSE, object_node)
    createChildNode(doc, 'truncated',
                    _TRUNCATED, object_node)
    createChildNode(doc, 'difficult',
                    _DIFFICULT, object_node)
    bndbox_node = doc.createElement('bndbox')
    # print("midname1[points]:",midname1["points"])
    createChildNode(doc, 'xmin', str(int(attrs['box'][0])),
                    bndbox_node)
    createChildNode(doc, 'ymin', str(int(attrs['box'][1])),
                    bndbox_node)
    createChildNode(doc, 'xmax', str(int(attrs['box'][2])),
                    bndbox_node)
    createChildNode(doc, 'ymax', str(int(attrs['box'][3])),
                    bndbox_node)
    object_node.appendChild(bndbox_node)
 
 
    return object_node
# 将documentElement写入XML文件
def writeXMLFile(doc, filename):
    tmpfile = open('tmp.xml', 'w')
    doc.writexml(tmpfile, addindent='' * 4, newl='\n', encoding='utf-8')
    tmpfile.close()
    # # 删除第一行默认添加的标记
    fin = open('tmp.xml')
    fout = open(filename, 'w')
    lines = fin.readlines()
    for line in lines[1:]:
        if line.split():
            fout.writelines(line)
    fin.close()
    fout.close()

className={
    1:"Person",
    2:"Vehicle",
    3:"Prop",
    4:"Bike"
}
 
if __name__ == "__main__":
    ##json文件路径和图片路径,
    json_path = "./jsonDatasets"
    img_path = "./imagesDatasets"
    json_list = os.listdir(json_path)
    # print("json_list:",json_list)
    fileList = os.listdir(img_path)
    # print(".....::")
    # print("fileList:", fileList)
    if fileList == 0:
        os._exit(-1)
        #对于每一张图都生成对应的json文件
    for i in range(len(fileList)):
        imageName = str(i+1)+'.jpg'
        saveName = imageName.strip(".jpg")
        # print("图片名称:", saveName)
        # 得到xml文件的名字
        xml_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (saveName + '.xml'))
        # print('...')
        # print("xml_file_name:", xml_file_name)
        img = cv2.imread(os.path.join(img_path, imageName))
        print(os.path.join(img_path, imageName))
        # cv2.imshow(img)
        height, width, channel = img.shape
        # print(height, width, channel)
        my_dom = xml.dom.getDOMImplementation()
        doc = my_dom.createDocument(None, _ROOT_NODE, None)
        # 获得根节点
        root_node = doc.documentElement
        # folder节点
        createChildNode(doc, 'folder', _FOLDER_NODE, root_node)
        # filename节点
        createChildNode(doc, 'filename', saveName + '.jpg', root_node)
        # print("正在创建各个结点中")
        # source节点
        source_node = doc.createElement('source')
        # source的子节点
        createChildNode(doc, 'database', _DATABASE_NAME, source_node)
        # createChildNode(doc, 'annotation', _ANNOTATION, source_node)
        # createChildNode(doc, 'image', 'flickr', source_node)
        root_node.appendChild(source_node)
        size_node = doc.createElement('size')
        createChildNode(doc, 'width', str(width), size_node)
        createChildNode(doc, 'height', str(height), size_node)
        createChildNode(doc, 'depth', str(channel), size_node)
        root_node.appendChild(size_node)
        # 创建segmented节点
        createChildNode(doc, 'segmented', _SEGMENTED, root_node)
        print("创建object节点")
        ann_data = []

        json_path1=os.path.join(json_path,str(i+1)+'.json')
        with open(json_path1, "r") as f:
            ann = json.load(f)
        for j in range(len(ann['predictions'])):
            object_node = createObjectNode(doc, ann["predictions"][j])
            root_node.appendChild(object_node)

        # 构建XML文件名称
        print(xml_file_name)  # 写入文件
        writeXMLFile(doc, xml_file_name)