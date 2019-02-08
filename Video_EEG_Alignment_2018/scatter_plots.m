ccc
%%%let's make scatter plots of all the possible EEG and camera times
parts= {'003';'004';'005';'007';'008';'009';'010';'011'};

%%%variables to store our latencies
eeg_latencies = zeros(length(parts),150);
camera_latencies_acs = zeros(length(parts),150);
camera_latencies_a = zeros(length(parts),150);
camera_latencies_as = zeros(length(parts),150);
camera_latencies_ac = zeros(length(parts),150);
camera_latencies = zeros(length(parts),150);
camera_latencies_acsp = zeros(length(parts),150);

%%%open eeglab and specify where our files are stored
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
filepath = ['M:\Experiments\Visual P3\EEG_Data'];

%%%loop through participants
for i_part = 1:length(parts)
    
    %%%load our EEG file for each participant
    filename = [parts{i_part} '_camera_p3.vhdr'];
    EEG = pop_loadbv(filepath, filename, [], []);
    
    %%%now load our camera latencies
    load(['M:\Experiments\Visual P3\Times\' parts{i_part} '_GoPro_Times.mat'])
    
    %%%aligned, corrected, shifted
    camera_latencies_acs(i_part,:) = (flash_latencies_gp_adjusted_shifted-0.0628);
    
    %%%aligned
    camera_latencies_a(i_part,:)  = flash_latencies_gp_shifted;
    
    %%%aligned, shifted
    camera_latencies_as(i_part,:)  = (flash_latencies_gp_shifted+0.12043)-0.0628;
    
    %%%aligned, corrected
    camera_latencies_ac(i_part,:)  = (flash_latencies_gp_shifted*1.001);
    
    %%%raw times
    camera_latencies(i_part,:)  = flash_latencies_gp_nonshifted;
    
    %%%now loop through and store each EEG event
    back = 0;
    for i_event = 1:length(EEG.event)
        if strcmp(EEG.event(i_event).type,'S255') == 1 | strcmp(EEG.event(i_event).type,'S  3') == 1 | strcmp(EEG.event(i_event).type,'boundary') == 1
            back = back + 1;
        else
            eeg_latencies(i_part,i_event-back) = (EEG.event(i_event).latency/EEG.srate);
        end
    end
    
    mdl = fitlm(flash_latencies_gp_shifted,eeg_latencies(i_part,:),'linear');
    adjustments = mdl.Coefficients.Estimate;
    
    camera_latencies_acsp(i_part,:) = ((flash_latencies_gp_shifted*adjustments(2,1))+adjustments(1,1));
end

%%%generate histograms of firt and last segments%%%
mean_cam_a = mean(camera_latencies_a,1);
mean_cam_acs = mean(camera_latencies_acs,1);
mean_cam_acsp = mean(camera_latencies_acsp,1);
mean_eeg = mean(eeg_latencies,1);

diff_cam_a = mean_eeg-mean_cam_a;
diff_cam_acs = mean_eeg-mean_cam_acs;
diff_cam_acsp = mean_eeg - mean_cam_acsp;

figure;
hist(diff_cam_a,15)
figure;
hist(diff_cam_acs,15)
figure;
hist(diff_cam_acsp,15)

figure;hold on;
hist(diff_cam_a,8);
hist(diff_cam_acs,8);
hist(diff_cam_acsp,8);
hold off;

mean(diff_cam_a)
mean(diff_cam_acs)
mean(diff_cam_acsp)

figure;hold on;
hist(camera_latencies_a,15);
hist(camera_latencies_acs,15);
hist(camera_latencies_acsp,15);
hold off;

%%%now make a scatter plot of our times
figure;hold on;
for i_part = 1:8
    plot(eeg_latencies(i_part,:),eeg_latencies(i_part,:),'r');
    plot(camera_latencies_a(i_part,:),eeg_latencies(i_part,:),'b');
    %     scatter(eeg_latencies(i_part,:),eeg_latencies(i_part,:),'r');
    %     scatter(camera_latencies_acs(i_part,:),eeg_latencies(i_part,:),'g');
    %     scatter(camera_latencies_a(i_part,:),eeg_latencies(i_part,:),'b');
    %     scatter(camera_latencies_as(i_part,:),eeg_latencies(i_part,:),'c');
    %     scatter(camera_latencies_ac(i_part,:),eeg_latencies(i_part,:),'m');
    %     scatter(camera_latencies(i_part,:),eeg_latencies(i_part,:),'y');
end
xlim([
    ax = gca;
    ax.Color = [0.75,0.75,0.75];
    line([0,300],[0,300],'color','k');
    hold off;
    ylabel(['EEG Times']); xlabel(['Camera Times']);
    % legend({'EEG','Camera (Aligned, Corrected, Shifted)',...
    %     'Camera (Aligned)','Camera (Aligned, Shifted)','Camera (Aligned, Corrected)',...
    %     'Camera (Raw)'},'location','southeast');
    
    figure;hold on;
    plot(mean(eeg_latencies,1),mean(eeg_latencies,1),'r');
    plot(mean(camera_latencies_a,1),mean(eeg_latencies,1),'b');
    hold off;
    % xlim([49,50]);
    xlim([234,235]);
    
    legend({'EEG','Camera (Aligned)'},'location','southeast');
