# =======================================================================================
# root_dir: analysis_python
# main functions:
# 1. calculate AUC
# 2. error analysis (visualization)
# =======================================================================================

# -------------------------------
# 1. calculate auc
# -------------------------------
# note to get auc score, first, we need to generate with python3.6 src/get_score.py
# 
# usage: python3.6 calculate_auc_dataset.py

python3.6 calculate_auc_ucf.py 
# input: score.txt
# output: auc score

python3.6 calculate_auc_shanghai.py 
# input: score.txt
# output: auc score


# -------------------------------
# 2. error analysis 
# -------------------------------
# usage: python3.6 visualize_dataset.py \
# --scores score.txt --rgb path/to/dataset/ --output path/to/output/folder/ --type one/or/all
# 
# --type one: create only single frame for each video
# --type all: create all frames based on FPS for each video, here, it will be used to produce the GIF file

python3.6 visualize_ucf.py \
--scores score.txt \
--rgb /media/ee401_2/Dataset2/dg_datasets/UCF_crimes/untrimmed_ucf_crimes_det_flow \
--output ../visualization/ucf/server/ \
--type one # {one, all}
# input: scores
# output: visualization

python3.6 visualize_shanghai.py \
--scores score.txt \
--rgb /media/ee401_2/Datasets1/dg/sh/rgb_frames/ \
--output ../visualization/shanghai/server/ \
--type one # {one, all}
# input: scores
# output: visualization

# to create the gif file as visualization
python3.6 convert_jpg2gif.py \
--folder folder/visualization/jpgs \
--results folder/visualization/gif
# input: jpg images, which is the output of visulize.py
# output: .gif images

# ----------------------------------------------------------------------------------------
