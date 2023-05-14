"""
Author: Andres Pinilla Palacios
Institution: Quality and Usability Lab, TU Berlin & UTS Games Studio, University of Technology Sydney
"""

participants = ["3I6EY","6HARB","AY9SI","DODE8","GLJO8","GNIE1","KNY2Z","MJC27","MRB58","NJL7V","PJGHY","QPLQF","RSC25","SDE14","SWLFB","SXZNO","TXNOY","UVBY3","VHY9N","YOO7M"];

for p = participants
    % Define file name
    file = sprintf("%s_eeg", p);
    
    % Define file path with raw data
    raw_file_path = sprintf(strcat(pwd, '/affect_detection/data/objective/csv/eeg/%s.csv'), file);
    
    % Read data
    data = csvread(raw_file_path, 1 ,1);
    
    % Transpose data
    transposed = data.';
    
    % Import data to EEGLAB
    EEG = pop_importdata('dataformat','array','nbchan',0,'data','transposed','srate',256,'pnts',0,'xmin',0);
    EEG.setname='raw';
    
    % Set marker channel
    EEG = pop_chanevent(EEG, 9,'edge','leading','edgelen',3);
    EEG = eeg_checkset( EEG );
    
    % Set channel locations
    % Load channel locations standard
    elec_standard_path = strcat(pwd, '/eeglab2021.1/plugins/dipfit4.3/standard_BEM/elec/standard_1020.elc')
    EEG=pop_chanedit(EEG, 'lookup', elec_standard_path,'changefield',{1,'labels','Ref'},'append',1,'changefield',{2,'labels','F3'},'setref',{'1',''},'append',2,'changefield',{3,'labels','F4'},'setref',{'1',''},'append',3,'changefield',{4,'labels','P3'},'setref',{'1',''},'append',4,'changefield',{5,'labels','P4'},'setref',{'1',''},'append',5,'changefield',{6,'labels','T7'},'setref',{'1',''},'append',6,'changefield',{7,'labels','T8'},'setref',{'1',''},'append',7,'changefield',{8,'labels','Cz'},'setref',{'1',''},'changefield',{8,'datachan',1},'changefield',{7,'datachan',1},'changefield',{6,'datachan',1},'changefield',{5,'datachan',1},'changefield',{4,'datachan',1},'changefield',{3,'datachan',1},'changefield',{2,'datachan',1});
    EEG = eeg_checkset( EEG );
    
    % Select channels
    EEG = pop_select( EEG, 'channel',{'F3','F4','P3','P4','T7','T8','Cz'});
    EEG = eeg_checkset( EEG );
    
    % Remove powerline noise
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
    
    % Extract epochs
    EEG = pop_epoch( EEG, {  '7'  }, [-3  60], 'newname', 'filtered epochs', 'epochinfo', 'yes');
    EEG.setname='epochs';
    EEG = eeg_checkset( EEG );
    
    % Remove baseline
    EEG = pop_rmbase( EEG, [-3000 0] ,[]);
    EEG.setname='baseline';
    EEG = eeg_checkset( EEG );
    
    % Resample
    EEG = pop_resample( EEG, 128);
    EEG = eeg_checkset( EEG );
    
    % Define export file path
    export_file_path = sprintf(strcat(pwd, '/affect_detection/data/objective/preprocessed/eeg/%s.csv'), file);
    
    % Export preprocessed data
    pop_export(EEG,export_file_path,'transpose','on','separator',',','precision',16);

end