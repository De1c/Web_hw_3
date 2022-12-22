import os
import re
import shutil
from send2trash import send2trash
from time import time
import logging
import concurrent.futures

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k",
    "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
)
TYPES = [
        ['jpeg', 'png', 'jpg', 'svg'],
        ['avi', 'mp4', 'mov', 'mkv'],
        ['doc', 'docx','txt', 'pdf', 'xlsx', 'pptx'],
        ['mp3', 'ogg', 'wav', 'amr'],
        ['zip', 'gz', 'tar']
        ]
images = TYPES[0]
videos = TYPES[1]
documents = TYPES[2]
music = TYPES[3]
archives = TYPES[4]


TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

dir = "C:\\Users\\Deic\\Desktop\\ForHW"
dir_i = os.path.join(dir, 'images')
dir_d = os.path.join(dir, 'documents')
dir_v = os.path.join(dir, 'video')
dir_a = os.path.join(dir, 'audio')
dir_ar = os.path.join(dir, 'archives')
dir_u = os.path.join(dir, 'unknown')

def normalize(path):
    """normalize's files names in path folder

    Args:
        path (path): path to folder
    """


    for each_file in os.listdir(path):
        path_for_each_file = os.path.join(dir, f'{each_file}')
        if os.path.isdir(path_for_each_file):
            continue
        else:
            splited = each_file.split('.')
            translated = splited[0].translate(TRANS)
            if not bool(re.match(r'\W', translated)):
                clear = re.sub(r'\W', '_', translated)
                complete = f'{clear}.{splited[1].lower()}'
                os.rename(path_for_each_file, os.path.join(dir, complete))
            else:
                continue

def sort(path):
    """sort's files names in folder

    Args:
        path (path): folder path

    Returns:
        dict : dict of files lists
    """

    image_list = []
    video_list = []
    documents_list = []
    music_list = []
    archives_list = []
    unknown_list = []
    folder_list = []
    for each_file in os.listdir(path):
        path_for_each_file = os.path.join(dir, f'{each_file}')
        if os.path.isdir(path_for_each_file):
            if path_for_each_file not in [dir_i, dir_d, dir_v, dir_a, dir_ar, dir_u]:
                folder_list.append(each_file)
        else:
            spl = each_file.split('.')
            if spl[1] in images:
                image_list.append(each_file)
            elif spl[1] in videos:
                video_list.append(each_file)
            elif spl[1] in documents:
                documents_list.append(each_file)
            elif spl[1] in music:
                music_list.append(each_file)
            elif spl[1] in archives:
                archives_list.append(each_file)
            else:
                unknown_list.append(each_file)


    return {'image_list': image_list, "video_list": video_list,
            'documents_list': documents_list, 'audio_list': music_list,
            'archives_list': archives_list, 'unknown_list': unknown_list,
            'folder_list': folder_list
            }


def files_for_direction(path):
    
    sorted_files = sort(path)
    print(sorted_files)
    
    def create_folders():
        if not os.path.exists(dir_i):
            os.mkdir(dir_i)
        if not os.path.exists(dir_d):
            os.mkdir(dir_d)
        if not os.path.exists(dir_v):
            os.mkdir(dir_v)
        if not os.path.exists(dir_a):
            os.mkdir(dir_a)
        if not os.path.exists(dir_ar):
            os.mkdir(dir_ar)
        if not os.path.exists(dir_u):
            os.mkdir(dir_u)
            
            
    def check_for_empty (direction, folder_name):
        """Checking if the directory is empty

        Args:
            direction : Direction for the folder
            folder_name : Folder name
        Returns:
            bool : True if the folder is not empty
        """
        

        if os.path.isdir(os.path.join(dir, direction)):
            if path not in [dir_i, dir_d, dir_v, dir_a, dir_ar, dir_u]:
                if len(os.listdir(os.path.join(dir, direction))) == 0:
                    send2trash(os.path.join(dir, direction))
                    return False
        else:
            return True
        
    

    create_folders()


    for files in sorted_files['image_list']:
        shutil.move(os.path.join(dir, files), dir_i)
    for files in sorted_files['video_list']:
        shutil.move(os.path.join(dir, files), dir_v)
    for files in sorted_files['documents_list']:
        shutil.move(os.path.join(dir, files), dir_d)
    for files in sorted_files['audio_list']:
        shutil.move(os.path.join(dir, files), dir_a)
    for files in sorted_files['archives_list']:
        shutil.unpack_archive(os.path.join(dir, files), os.path.join(dir_ar, files))


def main_sync():
    start = time()
    normalize(dir)
    files_for_direction(dir)
    end = time()
    logging.debug(f"{end-start} seconds")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    main_sync()     