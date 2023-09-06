import os 
import numpy as np 
import sys 
import scipy.io as sio 
from sklearn.metrics import auc, roc_curve, precision_recall_curve
from sklearn import metrics

val = 'shanghai_list.list'
gt = 'gt_shanghai.mat'
score = 'shanghai_TSM_e1300_c8_bresnet50_8_checkpoint_bestauc.txt'

win = 64
lines = list(open(score, "r"))
ground_truth = sio.loadmat(gt)
vals = list(open(val, "r"))
ground_truth = ground_truth['gt_segment2']

def list_to_np(values):	
	idx = np.array([])
	scr = np.array([])
	count = 0
	for i in values:
		tmp_idx = int(i.strip('\n').split(' ')[0])
		idx = tmp_idx if count == 0 else np.vstack((idx, tmp_idx))
		tmp_scr = float(i.strip('\n').split(' ')[1])	
		scr = tmp_scr if count == 0 else np.vstack((scr, tmp_scr))
		count +=1
	val = np.hstack((idx, scr))
	return  val


def main():
	val = list_to_np(lines)
        #print(len(val)
	count = 1
	pred = np.array([])	
	ct = 0
	for i in vals:
		#print(i.strip('\n').split(' ')[0])
		length = int(i.strip('\n').split(' ')[1])
		idx = np.where(val[:,0] == count)
		pred_local =  np.repeat(val[idx[0][0]:idx[0][-1]+1,1], win) 
                #pred_local1=pred_local/64
                #print(pred_local.shape)
		pred_local = pred_local[:length]
		pred = pred_local if pred.shape[0] == 0 else np.hstack((pred, pred_local))

		ct += length
		count += 1

	# print(len(pred), ground_truth[0][:].shape)
	# calcultae auc
        print(len(pred))
        print(len(ground_truth[0][:]))
	fpr, tpr, threshold = roc_curve(list(ground_truth[0][:]), list(pred)) 
	auc_score = auc(fpr, tpr)
	print('auc ', auc_score*100)
		
main()


	
