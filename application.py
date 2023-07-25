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

def ocr_program(target_folder,pattern):
    reader = easyocr.Reader(['en', 'hi'], gpu=False, quantize=False)

    

    #pattern  = 'namrata'
    print("Entered the ocr function")
    for dirpath, dirnames, filenames in os.walk(target_folder): #for Recursive Searching of Images

        if (dirnames == "manual") or (dirnames == pattern) :
            continue
        counter = 1
        dump =[]
        for image in filenames:
            
            word_list =[]
            if (image.endswith('.jpg') or image.endswith('.png') or image.endswith('.jpeg')) and 'tmb' not in image:
                start_time = time.time()
                result = reader.readtext(dirpath.replace(".\\", '')+"\\"+image, detail=0, paragraph=False)
                word_list.extend(result)
                
                flag = False

                for i in result:


                    if re.search(pattern, i.upper(), flags=re.I|re.M|re.X):
                        flag = True
                        break

                    else:
                        flag = False

                if flag == True:
                    #os.chdir("/home/varun/temp")
                    #SpecificDir = dirpath.replace(".\\", '')+"\\"+pattern+"\\"
                    if not os.path.exists(dirpath.replace(".\\", '')+"\\"+pattern+"\\"):
                        #os.chdir("..")
                        os.makedirs(dirpath.replace(".\\", '')+"\\"+pattern+"\\")
                        print("New folder created successfully!")

                    shutil.copy(dirpath.replace(".\\", '')+"\\"+image, dirpath.replace(".\\", '')+"\\"+pattern+"\\")


                else:
                    if not os.path.exists(dirpath.replace(".\\", '')+"\\Manual\\"):
                        os.makedirs(dirpath.replace(".\\", '')+"\\Manual\\")
                        print("New folder created successfully!")

                    shutil.copy(dirpath.replace(".\\", '')+"\\"+image, dirpath.replace(".\\", '')+"\\Manual\\")

                end_time = time.time()
                difference = end_time-start_time

                print(f"Time Taken for Image {counter} is {math.ceil(difference)} secs")
                counter+=1
            dump.extend(word_list)
            index1=len(dump)
            dump.insert(index1, image)
            #dump_deduplicated = np.unique(dump) -- to be checked if deduplication is required
            #np.savetxt(dirpath+"dump.csv", dump_deduplicated, delimiter="|", fmt='% s')
        if len(dump) > 0:
            with open(target_folder.replace(".\\", '').replace(".", '')+ time.strftime("%d-%m-%Y") + ".txt", "a", encoding='utf-8') as f:
                #Header1 = "Time Taken for Image Number-" + str(counter) + " Name-" + image + "-is " + str(difference) + " secs"
                #f.write("%s\n" % Header1)
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
