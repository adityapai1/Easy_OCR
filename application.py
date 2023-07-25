from flask import Flask, render_template, request
import easyocr
import os
import shutil
import time
import datetime
import math
import re
import csv

app = Flask(__name__)

def check_words_in_reader_list(text_words, reader_list):
    return [word for word in text_words if word in reader_list]

def ocr_program(target_folder, keyword_file):
    reader = easyocr.Reader(['en', 'hi'], gpu=False, quantize=False)

    # Read the keyword file and create a list of keywords
    with open(keyword_file, "r", encoding='utf-8') as f:
        reader_list = f.read().split(",")

    for dirpath, _, filenames in os.walk(target_folder):
        counter = 1
        for image in filenames:
            if (image.endswith('.jpg') or image.endswith('.png') or image.endswith('.jpeg')) and 'tmb' not in image:
                start_time = time.time()
                result = reader.readtext(os.path.join(dirpath, image), detail=0, paragraph=False)

                # Match OCR output with keyword list
                matching_words = check_words_in_reader_list(result, reader_list)

                if matching_words:
                    for keyword in matching_words:
                        if not os.path.exists(os.path.join(dirpath, keyword)):
                            os.makedirs(os.path.join(dirpath, keyword))
                        shutil.copy(os.path.join(dirpath, image), os.path.join(dirpath, keyword))
                else:
                    if not os.path.exists(os.path.join(dirpath, "Manual")):
                        os.makedirs(os.path.join(dirpath, "Manual"))
                    shutil.copy(os.path.join(dirpath, image), os.path.join(dirpath, "Manual"))

                end_time = time.time()
                difference = end_time - start_time
                print(f"Time Taken for Image {counter} is {math.ceil(difference)} secs")
                counter += 1

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("form.html")

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        target_folder = request.form['target_folder']
        keyword_file = request.files['keyword_file']
        keyword_file.save(os.path.join("temp", keyword_file.filename))
        ocr_program(target_folder, os.path.join("temp", keyword_file.filename))
        os.remove(os.path.join("temp", keyword_file.filename))
        return "Image OCR processing completed. Check the output folders."

if __name__ == '__main__':
    app.run(debug=True)
