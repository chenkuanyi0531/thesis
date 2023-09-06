import sys
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import shutil
import matplotlib.patches as mpatches
import math
import cv2
import matplotlib.image as image
from datetime import datetime
import argparse
from scipy.io import loadmat


parser = argparse.ArgumentParser(description="jpg2pdf visualization")
parser.add_argument('--scores', type=str)
parser.add_argument('--rgb', type=str)
parser.add_argument('--output', type=str)
parser.add_argument('--type', choices= ['one', 'all'], type=str)
args = parser.parse_args()

score = list(open(args.scores, "r"))

input_testing = '../src/list/shanghai_val.list'; 
test = list(open(input_testing, "r"))

len_window = 64
fps = 32

annots = loadmat('ground_truth_shanghai.mat')
val_annot = [item.flat[0] for item in annots['gt_segment2']]

count = 1
en = 0
st = 0
for i in test:
    tmp = i.strip('\n')
    vid = tmp.split(' ')[0]
    vidname_ = vid.split('/')
    vidname = vidname_[len(vidname_)-1]
    print(count, 'processing .. ', vidname)

    score_each = np.array([])
    for k in range(len(score)):
        ss = score[k].split(' ')
        if int(ss[0]) == count:
            score_each = np.array(
                [float(ss[1])]) if score_each.shape[0] == 0 else np.vstack(
                (score_each, np.array([float(ss[1])])))

    score_each_new = np.repeat(np.array(score_each), len_window)
    score_each_new = score_each_new[:int(tmp.split(' ')[1])]

    en = en + int(tmp.split(' ')[1])
    st = 0 if count == 1 else en - int(tmp.split(' ')[1])
    gtt = val_annot[st:en]

    score_final = np.zeros(int(tmp.split(' ')[1]))
    if not args.type == 'one':
        os.makedirs(os.path.join(args.output,args.type,vidname)) if not os.path.exists(
            os.path.join(args.output,args.type,vidname)) else print('folder existed')
    else:
        os.makedirs(os.path.join(args.output,args.type)) if not os.path.exists(
            os.path.join(args.output,args.type)) else print('folder existed')

    for k in range(int(tmp.split(' ')[1])):
        if not args.type == 'all':
            fps = int(tmp.split(' ')[1])

        if k % fps == 0:
            x_val = np.arange(int(tmp.split(' ')[1]))

            if not args.type == 'all':
                score_final = score_each_new  
            else:
                score_final[:k] = score_each_new[:k]

            plt.figure(figsize = (6,6))
            plt.subplot(2,1,1)
            img_file = os.path.join(args.rgb, vidname, 'i', str(k+1).zfill(6) + '.jpg')
            img = plt.imread(img_file)
            info = 'clip: ' + str(k) + '   detection: ' + 'normal' if score_final[k-1] < 0.5 else  'clip: ' + str(k) + '   detection: ' + 'anomaly'
            config = {'facecolor': 'green', 'alpha': 0.5, 'pad': 8}  if score_final[k-1] < 0.5 else  {'facecolor': 'red', 'alpha': 0.5, 'pad': 8}
            plt.text(75, 75, info,  bbox=config)
            plt.imshow(img)

            plt.subplot(2,1,2)
            plt.plot(x_val, score_final, color = 'b')
            plt.axis([0, int(tmp.split(' ')[1]), 0, 1])
            plt.fill_between(x_val, gtt, color="red", alpha=0.4)

            colors = ["b"]
            texts = ["video name: " + vidname]
            patches = [ plt.plot([],[], marker="o", ms=10, ls="", mec=None, color=colors[i], 
                        label="{:s}".format(texts[i]) )[0]  for i in range(len(texts)) ]
            plt.legend(handles=patches, bbox_to_anchor=(0.5, 0.1), 
                       loc='center', ncol=2, facecolor="plum", numpoints=1 )

            save_file = os.path.join(
                args.output, args.type, vidname + '.png') if not args.type == 'all' else os.path.join(
                args.output, args.type, vidname, str(k).zfill(6) + '.png')
            
            print('output: ', save_file)
            plt.savefig(save_file, dpi=300)
            plt.show(block=False)
            plt.close('all')

    count += 1








