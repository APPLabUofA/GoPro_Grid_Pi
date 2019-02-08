ccc

%%%for this we will loop through each part, and determine coefficients for
%%%each participant%%%

parts = {'003';'004';'005';'007';'008';'009';'010';'011'};

[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;

for i_part = 1:length(parts)
    
    EEG = pop_loadbv('M:\Experiments\Visual P3\EEG_Data', [parts{i_part} '_camera_p3.vhdr']);
    
    load(['M:\Experiments\Visual P3\Times\' parts{i_part} '_GoPro_Times.mat'])
    
    gopro_times = flash_latencies_gp_shifted;
    
    eeg_times = [];
    for i_event = 3:length(EEG.event)
        if strcmp(EEG.event(i_event).type, 'S  1') == 1
            eeg_times(i_event - 2) = EEG.event(i_event).latency/EEG.srate;
        elseif strcmp(EEG.event(i_event).type, 'S  2') == 1
            eeg_times(i_event - 2) = EEG.event(i_event).latency/EEG.srate;
        end
    end
    
    mdl = fitlm(gopro_times,eeg_times,'linear');
    adjustments(i_part,:) = mdl.Coefficients.Estimate';
    
    gopro_times = ((gopro_times*adjustments(i_part,2))+adjustments(i_part,1));
    
end

mean(adjustments(:,1))