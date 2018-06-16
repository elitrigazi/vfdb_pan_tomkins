x=load('ecg.mat');
[qrs_amp_raw,qrs_i_raw,delay]=pan_tompkin(x.val(1,:),250,1);
dlmwrite('ecg_1s_i.txt',qrs_i_raw);
dlmwrite('ecg_1s_amp.txt',qrs_amp_raw);
