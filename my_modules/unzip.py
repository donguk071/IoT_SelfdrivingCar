import glob
import zipfile

zip_folder_list = glob.glob('data/*.zip')
for zipfolder in zip_folder_list:
    with zipfile.ZipFile(zipfolder, 'r') as zf:
        zf.extractall('./data')
