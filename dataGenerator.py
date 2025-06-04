import random
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
lang = "arm"
output_dir = f"data/{lang}-ground-truth"
font_dir = "fonts"
os.makedirs(output_dir, exist_ok=True)

# Armenian alphabet and punctuation
armenian_chars = list("աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքևօֆԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ")
punctuation_between_words = [" ", " ", " ", " ", "՝ "]  # Single spaces, rarely Armenian comma+space
sentence_endings = [":", ":", "."]  # typical Armenian sentence-end symbols
internal_punctuations = ["՞", "՛"]

# Load fonts
font_files = [os.path.join(font_dir, f) for f in os.listdir(font_dir) if f.lower().endswith((".ttf", ".otf"))]
if not font_files:
    raise Exception("No .ttf or .otf fonts found in ./fonts")

def generate_arm_word(min_len=3, max_len=10):
    length = random.randint(min_len, max_len)
    word_chars = random.choices(armenian_chars, k=length)
    if random.random() < 0.3:
        vowels = ['ա', 'ե', 'է', 'ը', 'ի', 'ո', 'օ', 'ու']
        vowel_indices = [i for i, c in enumerate(word_chars) if c.lower() in vowels]
        if vowel_indices:
            chosen_index = random.choice(vowel_indices)
            punctuation_mark = random.choice(internal_punctuations)
            word_chars.insert(chosen_index + 1, punctuation_mark)
    return ''.join(word_chars)

def generate_arm_sentence(min_words=3, max_words=10):
    word_count = random.randint(min_words, max_words)
    words = [generate_arm_word() for _ in range(word_count)]
    sentence = words[0]
    for word in words[1:]:
        punct = random.choice(punctuation_between_words)
        sentence += punct + word
    sentence += random.choice(sentence_endings)
    return sentence

img_w, img_h = 800, 100
max_attempts = 10
min_font_size = 20  # Don't shrink below this for readability
max_font_size = 32  # Start from here

for i in range(2000):
    # Try several times for a suitable sentence/font combo
    for attempt in range(max_attempts):
        gt_sentence = generate_arm_sentence()
        visual_sentence = gt_sentence.replace(' ', '  ')
        font_path = random.choice(font_files)
        font_size = max_font_size
        fits = False
        while font_size >= min_font_size:
            font = ImageFont.truetype(font_path, font_size)
            text_bbox = font.getbbox(visual_sentence)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            if text_width < img_w - 20 and text_height < img_h - 20:
                fits = True
                break
            font_size -= 2
        if fits:
            break  # Success, proceed with this sentence/font
    else:
        # If nothing fit in N attempts, skip this sample
        print(f"[{i}] Skipped: could not fit any suitable sentence at readable font size.")
        continue

    # Create image and center text
    img = Image.new('L', (img_w, img_h), color=255)
    draw = ImageDraw.Draw(img)
    x = (img_w - text_width) // 2
    y = (img_h - text_height) // 2
    draw.text((x, y), visual_sentence, font=font, fill=0)

    # === optional augmentations ===
    if random.random() < 0.4:
        img = img.rotate(random.uniform(-3, 3), expand=1, fillcolor=255)
        img = img.resize((img_w, img_h), Image.BICUBIC)
    if random.random() < 0.2:
        shear_value = random.uniform(-0.15, 0.15)
        img = img.transform(img.size, Image.AFFINE, (1, shear_value, 0, 0, 1, 0), resample=Image.BICUBIC, fillcolor=255)
    if random.random() < 0.2:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.1, 0.5)))
    if random.random() < 0.1:
        np_img = np.array(img)
        noise_mask = np.random.choice([0,255,-1], size=np_img.shape, p=[0.005,0.005,0.99])
        np_img[noise_mask==0] = 0
        np_img[noise_mask==255] = 255
        img = Image.fromarray(np_img)

    # Store sentence image and ground truth text
    filename_base = f"{lang}.{i:07d}"
    img.save(os.path.join(output_dir, f"{filename_base}.tif"), format='TIFF')
    with open(os.path.join(output_dir, f"{filename_base}.gt.txt"), "w", encoding="utf-8") as f:
        f.write(gt_sentence)
    if i % 1000 == 0:
        print(f"[{i}] Generated: {filename_base}.tif")
        print(f"     Text for image: {visual_sentence}")
        print(f"     GT:             {gt_sentence}")