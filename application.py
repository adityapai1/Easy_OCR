from flask import Flask, render_template, request
import easyocr
import os
import shutil
import time
import datetime
from PIL import Image

import math
import re


app = Flask(__name__)

def ocr_program(target_folder, patterns):
    reader = easyocr.Reader(['en', 'hi'], gpu=False, quantize=False)

    print("Entered the OCR function")
    for dirpath, dirnames, filenames in os.walk(target_folder):
        if (dirnames == "manual") or any(name in dirnames for name in patterns):
            continue

        counter = 1
        dump = []

        for image in filenames:
            word_list = []
            if (image.endswith('.jpg') or image.endswith('.png') or image.endswith('.jpeg')) and 'tmb' not in image:
                start_time = time.time()
                result = reader.readtext(os.path.join(dirpath, image), detail=0, paragraph=False)
                word_list.extend(result)

                matched_pattern = None

                for i in result:
                    for pattern in patterns:
                        if re.search(pattern, i.upper(), flags=re.I | re.M | re.X):
                            matched_pattern = pattern
                            break
                    if matched_pattern:
                        break

                if matched_pattern:
                    pattern_folder = os.path.join(dirpath, matched_pattern)
                    if not os.path.exists(pattern_folder):
                        os.makedirs(pattern_folder)
                    shutil.copy(os.path.join(dirpath, image), pattern_folder)
                else:
                    manual_folder = os.path.join(dirpath, "Manual")
                    if not os.path.exists(manual_folder):
                        os.makedirs(manual_folder)
                    shutil.copy(os.path.join(dirpath, image), manual_folder)

                end_time = time.time()
                difference = end_time - start_time

                print(f"Time Taken for Image {counter} is {math.ceil(difference)} secs")
                counter += 1

            dump.extend(word_list)
            index1 = len(dump)
            dump.insert(index1, image)

        if len(dump) > 0:
            with open(target_folder.replace(".\\", '').replace(".", '') + time.strftime("%d-%m-%Y") + ".txt", "a", encoding='utf-8') as f:
                for item in dump:
                    f.write("%s\n" % item)



@app.route('/', methods=['GET', 'POST'])

def index():
    return render_template("form.html")

@app.route('/result', methods=['GET', 'POST'])

def result():
    if request.method == 'POST':
        target_folder = request.form['target_folder']
        global FolderCodeWord
        FolderCodeWord = request.form['folder_code_word']
        ocr_program(target_folder , FolderCodeWord)
        return render_template("success.html", )




if __name__ == '__main__':
    app.run(debug=True)



