# Дан путь до дирректории в которой находятся папки и файлы. Внутри папок
# лежат изображения с расширением jpg, jpeg, png и методанные к ним с таким
# же именем, но с расширением json. Расширения могут быть написаны как
# строчными, так и заглавными буквами. Помимо перечисленных расширений
# могут быть и другие.

# Должен получиться следующий ответ:
# [{"label1" : [
#   ['/tmp/labels/label1/2.jpeg', '/tmp/labels/label1/2.json'],
# ['/tmp/labels/label1/1image.JPG', '/tmp/labels/label1/1image.json']]},
# {"label2" : [['/tmp/labels/label2/1.jpg', '/tmp/labels/label2/1.json']]},
# {"label3" : [
#   ['/tmp/labels/label3/1.PNG', '/tmp/labels/label3/1.JSON'],
#   ['/tmp/labels/label3/16.jpg', '/tmp/labels/label3/16.json'],
#   ['/tmp/labels/label3/15.png', '/tmp/labels/label3/15.json']]}
# ]

import os
from pprint import pprint

labels_dir = "/tmp/labels"


def setup():
    from glob import glob
    os.makedirs(labels_dir, exist_ok=True)
    labels = {
        "label1": ["1image.JPG", "2.jpeg", "2.json", "1image.json", "3.jpg"],
        "label2": ["1.jpg", "1.json", "2.json", "3.json"],
        "label3": ["15.png", "15.json", "16.json", "16.jpg", "1.PNG", "1.JSON"],
        "label4": ["1.png", "1.txt", "2.txt", ],
    }
    for label in labels:
        label_path = os.path.join(labels_dir, label)
        os.makedirs(label_path, exist_ok=True)
        for item in labels[label]:
            open(os.path.join(label_path, item), 'a').close()
        print(f"{label_path} {os.listdir(label_path)}")
    open(os.path.join(labels_dir, "test.txt"), 'a').close()


def main():
    res = []
    # Проверяем адрес на наличие чего-либо
    with os.scandir(labels_dir) as directory:
        entry: os.DirEntry
        # Проверяем каждую папку
        for entry in directory:
            if entry.is_dir():
                path = f"%s/%s/" % (labels_dir, entry.name)

                files = os.listdir(entry.path)
                # Соритруем массив, так картинка и мета-данные окажутся рядом
                files.sort()
                found = []
                skip = False
                # Проверяем каждый файл
                for i in range(len(files) - 1):
                    # Если мы наткнулись на json при проверке прошлого файла, то пропускаем цикл
                    if skip:
                        skip = False
                        continue
                    file: str = files[i]
                    mask = file[:file.find(".")]
                    # Если мы попали на картинку, то мета-данные должны быть после них
                    if files[i + 1].lower() == mask + ".json":
                        skip = True
                        found.append([path + file, path + files[i + 1]])
                    # Для png наоборот, мета-данные должны были идти перед ним
                    elif files[i - 1].lower() == mask + ".json":
                        # skip = True
                        found.append([path + file, path + files[i - 1]])

                if len(found) > 0:
                    label = {}
                    label.setdefault(entry.name, found)
                    res.append(label)
    pprint(res)


if __name__ == '__main__':
    main()
