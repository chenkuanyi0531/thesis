import os
import imageio
import natsort 
import argparse

parser = argparse.ArgumentParser(description="jpg2pdf visualization")
parser.add_argument('--folder', type=str)
parser.add_argument('--results', type=str)
args = parser.parse_args()

os.makedirs(args.results) if not os.path.exists(args.results) else print('folder existed: ', args.results)
vid = [d for d in os.listdir(args.folder) if os.path.isdir(os.path.join(args.folder, d))]

count = 0
for k in vid:
	frame_path = os.path.join(args.folder, k)
	count+= 1
	print(str(count), ' processing >>', frame_path)
	filenames = [fn for fn in os.listdir(frame_path) if fn.endswith('.jpg')]
	filenames = natsort.natsorted(filenames,reverse=False)

	file_output = os.path.join(args.results, k +'.gif')
	with imageio.get_writer(file_output, mode='I', duration=0.5) as writer:
	    for filename in filenames:
	        image = imageio.imread(os.path.join(frame_path,filename))
	        writer.append_data(image)

