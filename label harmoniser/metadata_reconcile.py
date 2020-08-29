"""
1.extract labels from label.txt in root of each BUS folder 
and consolidates meta-data into df:labels

2.walk through all folders 
and consolidate file names into df:files

3.reconcile both df:rec
and output the breaks found

TODO:
update label_extractor() to avoid passing arguments
"""
import os
import re
import pandas as pd


def label_extractor(folder_bus=["25_20160407_back", "106_20150511_front"]):
    """ crawls into the input folder, finds 'label.txt',
        extract video data such as 
        ./normal/crowd/2016_04_07_19_45_52BackDepth.avi 0 6 1
        and return a consolidated dataframe to store as csv"""
    # Prepare variables from label.txt
    # ./normal/crowd/2016_04_07_19_46_47BackDepth.avi 0 9 1
    pattern = r'(\w*)/(\w*)/(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})(\w*\.avi)\s(\d*)\s(\d*)\s(\d*)'

    columns = ['file_id', 'quality', 'crowd',
               'year', 'month', 'day', 'hour', 'min', 'sec',
               'video_id', 'EnteringNumber', 'ExitingNumber', 'VideoType']

    labels = pd.DataFrame(columns=columns)

    # Open label file in each bus folder
    folder_input = "C:/Users/Etienne/1.PythonProjects/ComputerVision/OpenCVPeopleCounter/input"

    # Loop through folders
    for bus in folder_bus:
        with open(os.path.join(folder_input, bus, 'label.txt')) as f:
            # skip 4 lines of label.txt file
            raw = f.readlines()[4:]

        c = 4
        # Extract all videos meta data
        for line in raw:
            c += 1
            result = re.search(pattern, line)
            if result:
                temp = pd.DataFrame(columns=columns, data=[
                                    [bus]+list(result.groups())])

                labels = pd.concat([labels, temp], axis=0)
            else:
                print("error in line", c)

    # save dataframe
    # labels.to_csv('label harmoniser/labels.csv')
    return labels


def file_name_extractor():
    """walk through the folders and return a dataframe
    with video files information"""
    folder_input = "C:/Users/Etienne/1.PythonProjects/ComputerVision/OpenCVPeopleCounter/input"

    # \106_20150511_front\normal\crowd\2015_05_11_19_33_26FrontColor.avi

    pattern = r'\\([a-z0-9_]*)\\(\w*)\\(\w*)\\(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})(\w*\.avi)'

    columns = ['file_id', 'quality', 'crowd',
               'year', 'month', 'day', 'hour', 'min', 'sec',
               'video_id']

    file_list = []

    for root, dirs, files in os.walk(os.path.join(folder_input), topdown=True):
        # print(dirs)
        raw = root.lstrip(folder_input)
        if len(raw.split('\\')) > 3:
            # print(raw)
            for fname in files:
                text = os.path.join(raw, fname)
                file_list.append(re.search(pattern, text).groups())

    files = pd.DataFrame(columns=columns, data=file_list)

    # Save file
    # files.to_csv('label harmoniser/files.csv')
    return files


def reconcile(labels, files):
    # label = pd.read_csv('label harmoniser/label.csv')
    # files = pd.read_csv('label harmoniser/files.csv')

    labels = labels.astype('str')
    files = files.astype('str')

    labels['primary_key'] = labels['file_id']+labels['quality']+labels['crowd'] + \
        labels['year']+labels['month']+labels['day'] + \
        labels['hour']+labels['min']+labels['sec']

    files['primary_key'] = files['file_id']+files['quality']+files['crowd'] + \
        files['year']+files['month']+files['day'] + \
        files['hour']+files['min']+files['sec']

    rec = pd.merge(labels, files, on='primary_key',
                   how='outer', suffixes=['', '_f'])

    print('Reconciliation:')

    print(
        f"{rec['file_id'].isna().sum()} videos in folder are not in label.txt: ")
    if rec['file_id'].isna().sum() > 0:
        print(rec[rec['file_id'].isna() == True].values)

    print(
        f"{rec['file_id_f'].isna().sum()} lines in label.txt are not in folder: ")

    if rec['file_id_f'].isna().sum() > 0:
        print(rec[rec['file_id_f'].isna() == True].values)

    rec.to_csv('label harmoniser/reconcile.csv')


labels = label_extractor()
files = file_name_extractor()
reconcile(labels, files)
