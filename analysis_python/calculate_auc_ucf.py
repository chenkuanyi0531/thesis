import os 
import numpy as np 
import sys 
import scipy.io as sio 
from sklearn.metrics import auc, roc_curve, precision_recall_curve
from sklearn import metrics

val = 'ucf_list.list'
gt = 'gt_ucf.mat'
score = 'ucf_TSM_e30_c6_bresnet50_8_checkpoint.txt'

win = 32
lines = list(open(score, "r"))
ground_truth = sio.loadmat(gt)
vals = list(open(val, "r"))
ground_truth = ground_truth['gt_segment2'][0] 
print(ground_truth)

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
	return  val


def main():
	val = list_to_np(lines)
	count = 1
	pred = np.array([])
        #print(val)
	ct = 0
	for i in vals:
		#print('load ', i.strip('\n').split(' ')[0])
		length = int(i.strip('\n').split(' ')[1])
		idx = np.where(val[:,0] == count) 
		pred_local =  np.repeat(val[idx[0][0]:idx[0][-1]+1,1], win) 
		pred_local = pred_local[:length]
		pred = np.concatenate((pred, pred_local)) if pred.shape[0] > 0 else pred_local

		ct += length
		count += 1
        print(len(ground_truth))
        print(len(pred))
	# calcultae auc
	fpr, tpr, threshold = roc_curve(list(ground_truth), list(pred)) 
	auc_score = auc(fpr, tpr)
	print('auc ', auc_score)

		
main()


	
