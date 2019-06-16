import torch
path=""
_d=torch.load(path)
newdict=_d
def removekey(d, listofkeys):
    r=d
    for key in listofkeys:
        del r[key]
    return r

newdict['model'] = removekey(_d['model'], ['module.roi_heads.box.predictor.cls_score.bias','module.roi_heads.box.predictor.cls_score.weight','module.roi_heads.box.predictor.bbox_pred.bias','module.roi_heads.box.predictor.bbox_pred.weight','module.roi_heads.mask.predictor.mask_fcn_logits.weight','module.roi_heads.mask.predictor.mask_fcn_logits.bias'])
torch.save(newdict, 'mymodel.pth')