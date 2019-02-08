ccc;
%%%here we will try and further minimise the difference between AMP and
%%%Camera timings%%%

%%%let's loop through our EEG data first and gather the timings for each
%%%participant%%%

parts = {'003';'004';'005';'007';'008';'009';'010';'011'};
% % parts = {'010'};

amp_latencies = [];
camera_latencies = [];
latency_diff = [];

[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;

for i_part = 1:length(parts)
    EEG = pop_loadbv(['M:\Experiments\Visual P3\EEG_Data'], [parts{i_part} '_camera_p3.vhdr']);
    load(['M:\Experiments\Visual P3\Times\' parts{i_part} '_GoPro_Times.mat'])
    
    camera_latencies(i_part,:) = flash_latencies_gp_adjusted_shifted;
    for i_tone = 3:152
        amp_latencies(i_part,i_tone-2) = EEG.event(i_tone).latency;
    end
    amp_latencies(i_part,:) = amp_latencies(i_part,:)/EEG.srate;
    
    latency_diff(i_part,:) = (amp_latencies(i_part,:) - camera_latencies(i_part,:));
end

avg_latency_diff = mean(mean(latency_diff,2))