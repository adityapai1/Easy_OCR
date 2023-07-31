from flask import Flask, render_template, request, Response
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
        if "Manual" in dirnames:
            dirnames.remove("Manual")

        counter = 1
        dump = []

        for image in filenames:
            word_list = []
            if (image.endswith('.jpg') or image.endswith('.png') or image.endswith('.jpeg')) and 'tmb' not in image:
                start_time = time.time()
                result = reader.readtext(os.path.join(dirpath, image), detail=0, paragraph=False)
                word_list.extend(result)

                matched_patterns = [pattern for pattern in patterns if any(re.search(pattern, word.upper(), flags=re.I | re.M | re.X) for word in word_list)]

                if matched_patterns:
                    for pattern in matched_patterns:
                        pattern_folder = os.path.join(dirpath, pattern)
                        if not os.path.exists(pattern_folder):
                            os.makedirs(pattern_folder)
                            print(
                                f"New folder '{pattern}' created successfully!")
                        shutil.copy(os.path.join(
                            dirpath, image), pattern_folder)
                else:
                    manual_folder = os.path.join(dirpath, "Manual")
                    if not os.path.exists(manual_folder):
                        os.makedirs(manual_folder)
                        print("New folder 'Manual' created successfully!")
                    shutil.copy(os.path.join(dirpath, image), manual_folder)

                end_time = time.time()
                difference = end_time - start_time

                print(f"Time Taken for Image {counter} is {math.ceil(difference)} secs")
                yield f"data: Iteration: {counter}, Elapsed Time: {math.ceil(difference)} seconds\n"

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


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        target_folder = request.form['target_folder']
        # folder_code_word = request.form['folder_code_word']
        global uploaded_file
        global text_words
        # Convert the comma-separated string into a list
        uploaded_file = request.files["folder_code_word"]
        text = uploaded_file.read().decode("utf-8")
        patterns_list = [pattern.strip() for pattern in text.split(",")]

        return Response(ocr_program(target_folder, patterns_list), content_type='text/event-stream')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)