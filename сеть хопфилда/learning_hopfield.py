from tkinter import *
import io
from numpy import exp, array, random, dot, concatenate
import json   
import numpy as np
import random
from PIL import Image
import os
import re
from PIL import Image, ImageTk
# Вспомогательный класс для получения цветов всех пикселей

class ImageUtils:

    @staticmethod
    def get_pixels_of(canvas):
        width = int(canvas["width"])
        height = int(canvas["height"])
        colors = []

        for x in range(width):
            column = []
            for y in range(height):
                colors.append(ImageUtils.get_pixel_color(canvas, y, x))

        return colors

    @staticmethod
    def get_pixel_color(canvas, x, y):
        ids = canvas.find_overlapping(x, y, x, y)

        if len(ids) > 0:
            index = ids[-1]
            color = canvas.itemcget(index, "fill")
            color = color.upper()
            if color != '':
                return 1

        return 0
# Класс User Interface
class UI(Frame):
    # Конструктор
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # цвет кисти 
        self.color = "black"
        # размер кисти
        self.brush_size = 1
        # Помещение в окно UI
        self.setUI()
        # Создание экземпляра класса перцептрон
        # self.P1 = Perceptron()
        
    # Запускается при нажатии мыши и при перемещении зажатой мыши
    # Рисование на холсте
    def draw(self, event):
        self.canv.create_oval(event.x-(self.brush_size),
                              event.y-(self.brush_size),
                              event.x+ self.brush_size,
                              event.y+ self.brush_size,
                              fill=self.color, outline=self.color)
    # Помещение в окно UI
    def setUI(self):
        global CanvasWidth
        global CanvasHeight
        global ResultLabel
        global ResultLabel2
        # Ширина и высота в пикселях
        CanvasWidth = 100
        CanvasHeight= 100
        
        self.parent.title("LR")  # Устанавливаем название окна
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        self.canv = Canvas(self, width=CanvasWidth, height=CanvasHeight, bg="white")  # Создаем поле для рисования, устанавливаем белый фон
        self.canv.grid(row=2, column=0, columnspan=1,rowspan=3,
                       padx=5, pady=5, sticky=NW) 
        self.canv.bind("<B1-Motion>", self.draw) # Привязываем обработчик к канвасу. <B1-Motion> означает "при движении зажатой левой кнопки мыши" вызывать функцию draw
        self.canv.bind("<Button-1>", self.draw) # Привязываем обработчик к канвасу. <Button-1> означает "при нажатии левой кнопки мыши" вызывать функцию draw
        # Размещаем надписи 
        Label(self, text="Result: ").grid(row=2, column=1, padx=10,sticky=S) 
        ResultLabel = Label(self, text="   Инструкция:\nНарисовать букву и нажать SCAN")
        ResultLabel2 = Label(self, text="После завершения процесса \nсоздания матрицы дорисовать\n и нажать Restore")
        ResultLabel.grid (row=3, column=1, padx=10, columnspan=4, sticky=NW) 
        ResultLabel2.grid(row=4, column=1, padx=10, columnspan=4, sticky=NW) 
        
        color_lab = Label(self, text="Рисунок: ") 
        color_lab.grid(row=0, column=0, padx=18) 

        # Размещаем кнопки
        # red_btn = Button(self, text="True", width=6,
                         # command=lambda: self.P1.incWeights()) # Определяем параметры кнопки
        # red_btn.grid(row=0, column=1) # Устанавливаем кнопку в окно


        clear_btn = Button(self, text="Clear all", width=10,
                           command=lambda: self.canv.delete("all"))
        clear_btn.grid(row=0, column=2)
        
        # save_button = Button(self, text="Save", width=10,
                           # command=lambda: self.P1.save())
        # save_button.grid(row=0, column=3, sticky=W)
        
        # # Количество отображаемых чисел в спинбоксе from_=0, to=25
        # size_lab = Spinbox(self, width=7, from_=0, to=CntSymbols,
                           # command=lambda: self.P1.SetCurrentR(size_lab.get()))
        # size_lab.grid(row=1, column=0, padx=10)
        
        one_btn = Button(self, text="Restore", width=6,
                         command=lambda: testh(app,theta=0.5, time=30000, size=(100, 100), threshold=80)) 
        one_btn.grid(row=1, column=1)

        twenty_btn = Button(self, text="Scan", width=10,
                            command=lambda: hopfield(app,theta=0.5, time=30000, size=(100, 100), threshold=80))
        twenty_btn.grid(row=1, column=2)
        
        # load_btn = Button(self, text="Load", width=10,
                           # command=lambda: self.P1.load())
        # load_btn.grid(row=1, column=3, sticky=W)
        
    # Запускается при нажатии Scan  
    # Функция получения пикселей в массив
    def getpixels(self):
        global ResultLabel
        ResultLabel['text'] = "Text updated"    
        # получение пикселей в пассив
        colors = ImageUtils.get_pixels_of(self.canv)
        # уменьшение размера массива (для больших размеров масива пикселей)
        i=1
        bacj=5
        colors2=[]
        while(i<len(colors)):
            if i%(CanvasWidth)==1:
                colors2.append(colors[i])
                i=i+(bacj*CanvasHeight)
                i = i + bacj
                continue
            colors2.append(colors[i])
            i = i + bacj
        return np.array(colors)
        # Помещение входных данных в экземпляр класса перцептрон
        # self.P1.inputValues(colors)
        # Вызов функции, подготавливающей экземпляр класса к началу обучения
        # self.P1.startTraining()

# Главная функция 

def showim1(root,pathToImage):
    im = Image.open(pathToImage)
    ph = ImageTk.PhotoImage(im)
    
    label = Label(root, image=ph)
    label.image=ph
    label.grid(column=4, row=2,columnspan=10,rowspan=3) 
    return label
# Конвертирование матрицы в массив
def mat2vec(x):
    m = x.shape[0] * x.shape[1]
    tmp1 = np.zeros(m)

    c = 0
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            tmp1[c] = x[i, j]
            c += 1
    return tmp1


# Создание матрицы весов для изображения
def create_W(x):
    if len(x.shape) != 1:
        print("На вход подан не вектор")
        return
    else:
        w = np.zeros([len(x), len(x)])
        for i in range(len(x)):
            for j in range(i, len(x)):
                if i == j:
                    w[i, j] = 0
                else:
                    w[i, j] = x[i] * x[j]
                    w[j, i] = w[i, j]
    return w


# Конвертирование изображения в массив
def readImg2array(file, size, threshold=145):
    pilIN = Image.open(file).convert(mode="L")
    pilIN = pilIN.resize(size)
    imgArray = np.asarray(pilIN, dtype=np.uint8)
    x = np.zeros(imgArray.shape, dtype=float)
    x[imgArray > threshold] = 1
    x[x == 0] = -1
    return x


# Конвертирование массива в изображение
def array2img(data, outFile=None):
    y = np.zeros(data.shape, dtype=np.uint8)
    y[data == 1] = 255
    y[data == -1] = 0
    img = Image.fromarray(y, mode="L")
    if outFile is not None:
        img.save(outFile)
    return img


def update(w, y_vec, theta=0.5, time=100):
    for s in range(time):
        m = len(y_vec)
        i = random.randint(0, m - 1)
        u = np.dot(w[i][:], y_vec) - theta

        if u > 0:
            y_vec[i] = 1
        elif u < 0:
            y_vec[i] = -1

    return y_vec


def hopfield(app,theta=0.5, time=1000, size=(100, 100), threshold=60):
    global w
    # Чтение изображения и перевод в numpy массив
    print("Чтение изображений и создание матрицы весов")
    ResultLabel2['text'] = "Чтение изображений и создание матрицы весов..."
    num_files = 0
    # for path in train_files:
    # print(path)
    # x = readImg2array(file=path, size=size, threshold=threshold)
    x_vec = app.getpixels()
    print(len(x_vec))
    if num_files == 0:
        w = create_W(x_vec)
        num_files = 1
    else:
        tmp_w = create_W(x_vec)
        w = w + tmp_w
        num_files += 1

    print("Матрица весов создана")
    ResultLabel2['text'] = "Матрица весов создана"
def testh(app,theta=0.5, time=1000, size=(100, 100), threshold=60):
    # Импорт test изображений
    counter = 0
 
 
    y_vec = app.getpixels()
    print("Восстановление изображений")
    y_vec_after = update(w=w, y_vec=y_vec, theta=theta, time=time)
    y_vec_after = y_vec_after.reshape(size)

    outfile = "after_" + str(counter) + ".jpeg"
    array2img(y_vec_after, outFile=outfile)
    after_img = array2img(y_vec_after, outFile=None)
    # after_img.show()
    showim1(app,outfile)
    # counter += 1


# Theta порог активации нейрона
# Time количество шагов запоминания train изображений
# size разрешение изображений на выходе
# threshold порог для отсечения бинаризации изображения (от 0 до 255)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()   
    # Настройка размера окна
    root.geometry("400x220+300+300")
    app = UI(root)
    # Главный цикл
    root.mainloop()

    # Запуск нейросети
    
