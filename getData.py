import os, random, shutil

path="C:\\Users\\19606\\Datasets\\CleanedData\\PascalVoc\\ImageSets\\trainval.txt"
# path="C:\\Users\\19606\\Datasets\\CleanedData\\PascalVoc\\ImageSets\\test.txt"

file = open(path,"r",encoding="utf-8",errors="ignore")
# Img_path=[]
# Img_id=[]
n=0
while True:
        mystr = file.readline()
        if not mystr:
                break
        n+=1
        mystr=mystr[:-1]

        # 标注文件提取
        
        # test 标注
        # mystr+='.xml' 
        # final_Img_path='C:/Users/19606/Datasets/CleanedData/PascalVoc/Annotations/'+ mystr  # 原始文件路径
        # index=mystr.index('/')
        # Img_name=mystr.replace('/','_')              # image 新的命名
        # target_path='../XmlFile/test/'+ Img_name                                       # mystr[index+1:]
        # shutil.move(final_Img_path, target_path)
        
        # trainval 标注
        # mystr+='.xml' 
        # final_Img_path='../PascalVoc/Annotations/'+ mystr  # 原始文件路径
        # index=mystr.index('/')
        # Img_name=mystr.replace('/','_')              # image 新的命名
        # target_path='../XmlFile/trainval/'+ Img_name                                       # mystr[index+1:]
        # shutil.move(final_Img_path, target_path)

        # image提取
        
        # test image 提取
        # mystr+='.jpg' 
        # final_Img_path='../PascalVoc/JPEGImages/'+ mystr  # 原始文件路径
        # Img_name=mystr.replace('/','_')
        # target_path='../ImageFile/test/'+Img_name
        # shutil.move(final_Img_path, target_path)

        # trainval image 提取
        mystr+='.jpg' 
        final_Img_path='../PascalVoc/JPEGImages/'+ mystr  # 原始文件路径
        Img_name=mystr.replace('/','_')
        target_path='../ImageFile/trainval/'+Img_name
        shutil.move(final_Img_path, target_path)


DIR='../XmlFile/trainval'
print (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
print(n)
