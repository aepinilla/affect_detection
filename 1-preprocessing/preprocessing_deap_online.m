for s = 1:32
    % Define file name
    file = sprintf("s%d", s); 
    
    % Define file path with raw data
    raw_file_path = sprintf(strcat(pwd, '/affect_detection/data/deap_online/objective/raw/%s.bdf'), file);
    
    % Read data
    EEG = pop_biosig(raw_file_path, 'channels',[1:32 48] ,'ref',32);
    
    % Load channel locations standard
    elec_standard_path = strcat(pwd, '/eeglab2021.1/plugins/dipfit4.3/standard_BEM/elec/standard_1020.elc')
    EEG=pop_chanedit(EEG, 'lookup', elec_standard_path);
    EEG = eeg_checkset( EEG );
    
    % Remove powerline noise
    EEG = eeg_checkset( EEG );
    EEG = pop_eegfiltnew(EEG, 'locutoff',45,'hicutoff',55,'revfilt',1,'plotfreqz',0);
    EEG = eeg_checkset( EEG );
     
    % ASR 
    EEG = pop_clean_rawdata(EEG, 'FlatlineCriterion',5,'ChannelCriterion',0.8,'LineNoiseCriterion',4,'Highpass',[0.25 0.75] ,'BurstCriterion',20,'WindowCriterion','off','BurstRejection','off','Distance','Euclidian');
    EEG.setname='data_asr';
    EEG = eeg_checkset( EEG );
    
    % Common average reference
    EEG = pop_reref( EEG, []);
    EEG.setname='data_referenced';
    EEG = eeg_checkset( EEG );
    
    % Apply filter
    EEG = pop_eegfiltnew(EEG, 'locutoff',4,'hicutoff',45);
    EEG.setname='data_filtered';
    EEG = eeg_checkset( EEG );
    
    % Extract epochs.
    % According to DEAP dataset documentation, the marker channel is different in files 23 onwards.
    if s <= 23
        EEG = pop_epoch( EEG, {  'condition 4'  }, [-3  60], 'newname', 'epochs', 'epochinfo', 'yes');
        EEG = eeg_checkset( EEG );
    else
        EEG = pop_epoch( EEG, {  '65284'  }, [-3  60], 'newname', 'epochs', 'epochinfo', 'yes');
        EEG = eeg_checkset( EEG );
    end
    
    % Remove baseline
    EEG = pop_rmbase( EEG, [-3000 0] ,[]);
    EEG.setname='data_filtered baseline';
    EEG = eeg_checkset( EEG );
    
    % Resample
    EEG = pop_resample( EEG, 128);
    EEG = eeg_checkset( EEG );
    
    % Remove unwanted channels to reduce size of exported files
    EEG = pop_select( EEG, 'channel',{'F3' 'F4', 'P3', 'P4'});
    EEG.setname= 'eeg';
    EEG = eeg_checkset( EEG );
    
    % Define export file path
    export_file_path = sprintf(strcat(pwd, '/affect_detection/data/deap_online/objective/preprocessed/%s.csv'), file);
    
    % Export preprocessed data
    pop_export(EEG,export_file_path,'transpose','on','separator',',','precision',16);
end