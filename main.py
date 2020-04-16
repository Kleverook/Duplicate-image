import cv2
import difflib
import os
from operator import itemgetter


def get_tree(path):
    file_list = []

    for i in os.listdir(path):
        temp_path = os.path.join(path, i)
        if os.path.isdir(temp_path):
            get_tree(temp_path)
        else:
            tmp_top.append(temp_path)

    for file in tmp_top:
        if file.endswith(".jpg") or file.endswith(".png"):
            file_list.append((os.path.join(file), CalcImageHash(os.path.join(file))))

    return file_list


def CalcImageHash(FileName):
    image = cv2.imread(FileName)  # Прочитаем картинку
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу
    # Рассчитаем хэш
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def similarity(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()


def comparison_list(input_data):
    return_data = []
    for i in range(0, len(input_data)):
        for j in range(i, len(input_data)):
            if j != i:
                sim = similarity(input_data[i][1], input_data[j][1])
                if sim >= similarity_degree:
                    return_data.append((input_data[i][0], input_data[j][0], sim))
    return_data.sort(key=itemgetter(2), reverse=True)
    return return_data


if __name__ == "__main__":
    tmp_top = []

    path_input = input("Enter directory path\n")
    similarity_degree = float(input("Enter the degree of similarity from 0 to 1\n"))
    path_start = os.path.join(path_input)
    data = get_tree(path_start)
    result = comparison_list(data)
    for i in result:
        print(i)

    print("Results are placed.")
