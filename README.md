# PeopleCounter
count people with raspberry!

# Dataset note:
from: https://drive.google.com/drive/folders/1EK_Nfsjudn-Ku0-Q81c454fLBAQnRp-R
###### Train set: 25_20160407_back, 106_20150511_front
    removed: 
     - all ...Depth.avi files
     - all label.txt of end-folders (ex: .../noisy/crowd/label.txt)
     - Corrupted file: 25_20160407_back/noisy/uncrowd/2016_04_07_09_11_02BackColor.avi
don't do my mistake: use 7zip to unzip and keep the structure

###### Test set: to decide



# Folder structure

    |- label harmoniser
        |- metadata_reconcile.py
    |- input
        |-25_20160407_back
            |-label.txt
            |-noisy
                |-crowd
                    |-2016_04_07_14_20_59BackColor.avi
                    ...
    |-output
        |-x
    |-mobilenet_ssd
        |- /models
    |-pyimagesearch
        |-
