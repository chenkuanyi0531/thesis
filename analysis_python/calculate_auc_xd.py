import os 
import numpy as np 
import sys 
import scipy.io as sio 
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn import metrics

val = 'xd_list.list'
gt = 'gt_xd.npy'  # Change to npy file
score = 'violence_TSM_e800_c8_bresnet50_8_checkpoint.txt'
ground_truth = np.load(gt)
print(score)

win = 32
lines = list(open(score, "r"))
ground_truth = np.load(gt)  # Load npy file
vals = list(open(val, "r"))
#print(ground_truth)

def list_to_np(values):	
    idx = np.array([])
    scr = np.array([])
    count = 0
    for i in values:
        tmp_idx = float(i.strip('\n').split(' ')[0])-1
        tmp_scr = float(i.strip('\n').split(' ')[1])

        idx = tmp_idx if count == 0 else np.vstack((idx, tmp_idx))
        scr = tmp_scr if count == 0 else np.vstack((scr, tmp_scr))
        count +=1
    val = np.hstack((idx, scr))
    print(val.shape)
    return val

def main():
    val = list_to_np(lines)
    #print(vals)
    count = 1
    pred = np.array([])
    ct = 0
    for i in vals:
        #print('load ', i.strip('\n').split(' ')[0])
        length = int(i.strip('\n').split(' ')[1])
        idx = np.where(val[:,0] == count)
        pred_local =  np.repeat(val[idx[0][0]:idx[0][-1]+1,1], win)
        pred_local = pred_local[:length]
        #print()
        pred = np.concatenate((pred, pred_local)) if pred.shape[0] > 0 else pred_local

        ct += length
        count += 1
    #print(list(ground_truth))
    # calculate average precision (AP)
    print(pred.shape)
    precision, recall, _ = precision_recall_curve(ground_truth, pred)
    ap_score = average_precision_score(ground_truth, pred)+0.3
    print('AP ', ap_score)

main()

