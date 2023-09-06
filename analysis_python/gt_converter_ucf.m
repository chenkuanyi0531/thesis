clc
clear
close all

% gt converter of ucf to 1D dimension
load('ucf.mat')
data = length(tempo.textdata);

list = importdata('ucf_list.list');

gt_segment2 = [];
count2 = 0;
for i = 1:length(list.textdata)
    tmp = zeros(1,list.data(i));
    disp(length(tmp));
    count2 = count2+ list.data(i);
    if contains(list.textdata(i),'Normal') == 1
        gt_segment2 = [gt_segment2 tmp]; % only normal videos
    else 
        for j = 1 : length(tempo.data)
            disp(j)
            if contains(tempo.textdata(j), list.textdata(i)) == 1
                tmp(tempo.data(j,2):tempo.data(j,3)) = 1; % contains anomaly
                if tempo.data(j,4) ~= -1
                    tmp(tempo.data(j,4):tempo.data(j,5)) = 1; % contains anomaly
                end
            end
        end
        tmp = tmp(1:list.data(i)) % make sure the length is the same
        gt_segment2 = [gt_segment2 tmp]; 
    end
    disp(length(tmp));
    if length(gt_segment2) ~= count2
        disp('beda ');
    end
        
end

save('gt_ucf.mat','gt_segment2', '-v7');   % 1x1111808 -- 1x1111808
clear; load('gt_ucf.mat')