import os
import re
import shutil
import sys
from send2trash import send2trash
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
        ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
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


def normalize(path):
    """normalize's files names in path folder

    Args:
        path (path): path to folder
    """

    for each_file in os.listdir(path):
        path_for_each_file = os.path.join(path, f'{each_file}')
        if os.path.isdir(path_for_each_file):
            continue
        else:
            splited = each_file.split('.')
            translated = splited[0].translate(TRANS)
            if not bool(re.match(r'\W', translated)):
                clear = re.sub(r'\W', '_', translated)
                complete = f'{clear}.{splited[1].lower()}'
                os.rename(path_for_each_file, os.path.join(path, complete))
            else:
                continue


def sort(path):
    """sort's files names in folder

    Args:
        path (path): folder path

    Returns:
        dict : dict of files lists
    """
    dir_i = os.path.join(path, 'images')
    dir_d = os.path.join(path, 'documents')
    dir_v = os.path.join(path, 'video')
    dir_a = os.path.join(path, 'audio')
    dir_ar = os.path.join(path, 'archives')
    dir_u = os.path.join(path, 'unknown')

    image_list = []
    video_list = []
    documents_list = []
    music_list = []
    archives_list = []
    unknown_list = []
    folder_list = []

    for each_file in os.listdir(path):
        path_for_each_file = os.path.join(path, f'{each_file}')
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


def files_for_direction(path: str) -> None:

    sorted_files = sort(path)
    print(sorted_files)

    dir_i = os.path.join(path, 'images')
    dir_d = os.path.join(path, 'documents')
    dir_v = os.path.join(path, 'video')
    dir_a = os.path.join(path, 'audio')
    dir_ar = os.path.join(path, 'archives')
    dir_u = os.path.join(path, 'unknown')

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

    def check_for_empty(folder_name: str):
        """
        Checking if the directory is empty

        Args:
            direction : Direction for the folder
            folder_name : Folder name
        Returns:
            bool : True if the folder got something inside
        """

        if os.path.isdir(os.path.join(path, folder_name)):
            if path not in [dir_i, dir_d, dir_v, dir_a, dir_ar, dir_u]:
                if len(os.listdir(os.path.join(path, folder_name))) == 0:
                    send2trash(os.path.join(path, folder_name))
                    sorted_files['folder_list'].remove(folder_name)
                    return False
        return True

    def folder_solver():

        for each_folder in sorted_files['folder_list']:
            check_for_empty(each_folder)
        direcotorys_for_folders = [os.path.join(
            path, folder_name) for folder_name in sorted_files['folder_list']]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            result = executor.map(files_for_direction, direcotorys_for_folders)

    create_folders()
    folder_solver()

    for files in sorted_files['image_list']:
        shutil.move(os.path.join(path, files), dir_i)
    for files in sorted_files['video_list']:
        shutil.move(os.path.join(path, files), dir_v)
    for files in sorted_files['documents_list']:
        shutil.move(os.path.join(path, files), dir_d)
    for files in sorted_files['audio_list']:
        shutil.move(os.path.join(path, files), dir_a)
    for files in sorted_files['archives_list']:
        shutil.unpack_archive(os.path.join(path, files),
                              os.path.join(dir_ar, files))


def main():
    logging.basicConfig(level=logging.DEBUG)
    path = input("Input directory: ")
    normalize(path)
    files_for_direction(path)

#To tests


def for_test(path: str = None):  # Fully changable

    for i in range(5):
        os.mkdir(os.path.join("C:\\Users\\Deic\\Desktop\\ForHW", str(i)))

    for i in range(5):
        for e_type in TYPES:
            for ee in e_type:
                with open(f"C:\\Users\\Deic\\Desktop\\ForHW\\{i}\\New_file.{ee}", 'w') as ph:
                    pass


if __name__ == '__main__':
    main()
