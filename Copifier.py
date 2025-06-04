import os
import shutil

char_map = {
    '0': 'Ա',  '1': 'Բ',  '2': 'Գ',   '3': 'Դ',   '4': 'Ե',   '5': 'Զ',   '6': 'Է',   '7': 'Ը',
    '8': 'Թ',  '9': 'Ժ',  '10': 'Ի',  '11': 'Լ',  '12': 'Խ',  '13': 'Ծ',  '14': 'Կ',  '15': 'Հ',
    '16': 'Ձ', '17': 'Ղ', '18': 'Ճ',  '19': 'Մ',  '20': 'Յ',  '21': 'Ն',  '22': 'Շ',  '23': 'Ո',
    '24': 'Ու','25': 'Չ', '26': 'Պ',  '27': 'Ջ',  '28': 'Ռ',  '29': 'Ս',  '30': 'Վ',  '31': 'Տ',
    '32': 'Ր', '33': 'Ց', '34': 'Փ',  '35': 'Ք',  '36': 'Եվ', '37': 'Օ',  '38': 'Ֆ',  '39': 'ա',
    '40': 'բ', '41': 'գ', '42': 'դ',  '43': 'ե',  '44': 'զ',  '45': 'է',  '46': 'ը',  '47': 'թ',
    '48': 'ժ', '49': 'ի', '50': 'լ',  '51': 'խ',  '52': 'ծ',  '53': 'կ',  '54': 'հ',  '55': 'ձ',
    '56': 'ղ','57': 'ճ',  '58': 'մ',  '59': 'յ',  '60': 'ն',  '61': 'շ',  '62': 'ո',  '63': 'ու',
    '64': 'չ', '65': 'պ', '66': 'ջ',  '67': 'ռ',  '68': 'ս',  '69': 'վ',  '70': 'տ',  '71': 'ր',
    '72': 'ց', '73': 'փ', '74': 'ք',  '75': 'և',  '76': 'օ',  '77': 'ֆ'
}

source_root = r"C:\Project1\Folder\Train"
output_root = r"C:\Project1\tesstrain\data\arm-ground-truth"
photo_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")

if not os.path.exists(output_root):
    os.makedirs(output_root)

for foldername in os.listdir(source_root):
    folder_path = os.path.join(source_root, foldername)
    if not os.path.isdir(folder_path):
        continue

    if foldername not in char_map:
        print(f"Folder '{foldername}' not in mapping, skipping.")
        continue

    character = char_map[foldername]
    local_counter = 0

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if not (os.path.isfile(full_path) and filename.lower().endswith(photo_extensions)):
            continue

        ext = os.path.splitext(filename)[1].lower()
        new_name = f"{foldername}_{local_counter}{ext}"
        new_photo_path = os.path.join(output_root, new_name)

        shutil.copy2(full_path, new_photo_path)

        gt_filename = f"{foldername}_{local_counter}.gt.txt"
        gt_full_path = os.path.join(output_root, gt_filename)

        with open(gt_full_path, 'w', encoding='utf-8') as f:
            f.write(character)

        print(f"Copied: {new_photo_path}, Created: {gt_full_path}")

        local_counter += 1

print("Done.")