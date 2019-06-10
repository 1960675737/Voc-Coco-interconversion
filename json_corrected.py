import json
from pycocotools.coco import COCO
result={}                              # 保存修改后的dict
# test json

submit="./test.json"
my_json=COCO("C:/Users/19606/Datasets/CleanedData/code/pre_test.json")

# trainval json

# submit="./trainval.json"
# my_json=COCO("C:/Users/19606/Datasets/CleanedData/code/pre_trainval.json")

my_data=my_json.dataset

result["images"]=my_data["images"]
result["categories"]=[{'supercategory': 'Person', 'id': 1, 'name': 'Person'},
					 {'supercategory': 'Vehicle', 'id': 2, 'name': 'Vehicle'}, 
 					{'supercategory': 'Prop', 'id': 3, 'name': 'Prop'}, 
 					{'supercategory': 'Bike', 'id': 4, 'name': 'Bike'}]
result["annotations"]=[]
my_annotations=my_data["annotations"]

# test_json_corrected

for i in range(len(my_annotations)):
	if my_annotations[i]["category_id"]==1:                # 1->Person
		result["annotations"].append(my_annotations[i])
	elif my_annotations[i]["category_id"]==3:              # 2->Vehicle
		my_annotations[i]["category_id"]=2
		result["annotations"].append(my_annotations[i])
	elif my_annotations[i]["category_id"]==2:
		my_annotations[i]["category_id"]=3                 # 3->Prop
		result["annotations"].append(my_annotations[i])
	elif my_annotations[i]["category_id"]==7:
		my_annotations[i]["category_id"]=4                  # 4->Bike
		result["annotations"].append(my_annotations[i])
	else:
		continue

# trainval_json_corrected

# for i in range(len(my_annotations)):
# 	if my_annotations[i]["category_id"]==1:                # 1->Person
# 		result["annotations"].append(my_annotations[i])
# 	elif my_annotations[i]["category_id"]==2:              # 2->Vehicle
# 		result["annotations"].append(my_annotations[i])
# 	elif my_annotations[i]["category_id"]==5:
# 		my_annotations[i]["category_id"]=3                  # 3->Prop
# 		result["annotations"].append(my_annotations[i])
# 	elif my_annotations[i]["category_id"]==8:
# 		my_annotations[i]["category_id"]=4                  # 4->Bike
# 		result["annotations"].append(my_annotations[i])
# 	elif my_annotations[i]["category_id"]==9:
# 		my_annotations[i]["category_id"]=2
# 		result["annotations"].append(my_annotations[i])
# 	else:
# 		continue

with open(submit,"w") as f:
	json.dump(result,f)



