import math
import numpy as np
# from PIL import Image
from tkinter import *
import io
from numpy import exp, array, random, dot, concatenate
import json   
import numpy as np
import random
# from PIL import Image
import os
import re
import time
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
        self.brush_size = 7
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
        CanvasWidth = 280
        CanvasHeight= 280
        
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
        ResultLabel2 = Label(self, text="")
        ResultLabel.grid (row=3, column=1, padx=10, columnspan=4, sticky=NW) 
        ResultLabel2.grid(row=4, column=1, padx=10, columnspan=4, sticky=NW) 
        
        color_lab = Label(self, text="Обучаемая буква: ") 
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
        
        # one_btn = Button(self, text="Restore", width=6,
                         # command=lambda: testh(app,theta=0.5, time=30000, size=(100, 100), threshold=80)) 
        # one_btn.grid(row=1, column=1)

        twenty_btn = Button(self, text="Scan", width=10,
                            command=lambda: train1(app))
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
        bacj=10
        colors2=[]
        while(i<len(colors)):
            if i%(CanvasWidth)==1:
                colors2.append(colors[i])
                i=i+(bacj*CanvasHeight)
                i = i + bacj
                continue
            colors2.append(colors[i])
            i = i + bacj
        print(len(colors2))
        a = array(colors).reshape((280, 280))
        b=[]
        for i in range(0,len(a),10):
            for j in range(0,len(a),10):
                if a[i][j]:
                    b.append(a[i][j])
                    print(a[i][j],end='')
                else:
                    b.append(a[i][j])
                    print(a[i][j],end='')
                
            print("")
        #print("b")
        return array(b).reshape(784,)
        # return np.array(b)
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

def hebb(speed, train, y, weights):
    for i,f in enumerate(train):
        for j in range(len(weights) - 1):
            weights[j] += speed * f[j] * y[i]
        weights[784] += speed*y[i] #bias
    return(weights)

def predict(features, weights):
    pred = []
    for i, f in enumerate(features):
        tmp = 0
        for j in range(len(weights) - 1):
            tmp += weights[j] * f[j]
        tmp += weights[784]
        if tmp < 47000:
            pred.append("Class 0")
        else:
            pred.append("Class 1")
    return(pred)

def train(weights,lr):
    data_file = open('mnist_train.csv', 'r')
    trening_list = data_file.readlines()
    data_file.close()
    inputs = []
    outputs = []
    # bar = IncrementalBar('Обучение', max=len(trening_list), suffix='%(percent)d%%')
    for record in trening_list:
        # bar.next()
        all_values = record.split(',')
        if (all_values[0] == '1') or (all_values[0] == '0'):
            inputs.append(np.asfarray(all_values[1:]))
            outputs.append(int(all_values[0]))
    # bar.finish()
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if int(inputs[i][j]) > 125:
                inputs[i][j] = 1
            else:
                inputs[i][j] = 0
    weights = hebb(lr, inputs, outputs, weights)

def img_to_csv(file):
    img = Image.open(file)
    img = img.resize((28, 28), Image.NEAREST)
    img.load()
    imgdata = np.asarray(img, dtype="int32")
    data = []
    for y in range(28):
        for x in range(28):
            if imgdata[x][y] > 125:
                data.append(1)
            else:
                data.append(0)
    return data
def train1(app):
    lr = 0.5
    global weights
    try:
        weights # does a exist in the current namespace
    except NameError:
        ResultLabel2['text']="Подождите\nОбучение..."
        app.update()
        time.sleep(1)
        weights = np.zeros(784)
        weights = np.append(weights, -1)
        train(weights,lr)
    dataSet = []
    img = app.getpixels()
    dataSet.append(img)
    print(predict(dataSet, weights))
    ResultLabel2['text']=(predict(dataSet, weights))

if __name__ == "__main__":
    root = Tk()   
    # Настройка размера окна
    root.geometry("600x400+300+300")
    app = UI(root)
    # Главный цикл
    root.mainloop()

