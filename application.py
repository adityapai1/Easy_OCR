def ocr_program(target_folder, patterns):
    reader = easyocr.Reader(['en', 'hi'], gpu=False, quantize=False)

    print("Entered the OCR function")
    for dirpath, dirnames, filenames in os.walk(target_folder):
        if "Manual" in dirnames:
            dirnames.remove("Manual")

        counter = 1
        dump = []
        pattern_folders = {}  # To store the dynamically created pattern folders

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
                    if matched_pattern not in pattern_folders:
                        pattern_folder = os.path.join(dirpath, matched_pattern)
                        os.makedirs(pattern_folder)
                        pattern_folders[matched_pattern] = pattern_folder

                    shutil.copy(os.path.join(dirpath, image), pattern_folders[matched_pattern])
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
