from tkinter import *
import io
from numpy import exp, array, random, dot, concatenate
import json
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
        self.brush_size = 5
        # Помещение в окно UI
        self.setUI()
        # Создание экземпляра класса перцептрон
        self.P1 = Perceptron()
        
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
        
        self.parent.title("Perceptron")  # Устанавливаем название окна
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне

        self.canv = Canvas(self, width=CanvasWidth, height=CanvasHeight, bg="white")  # Создаем поле для рисования, устанавливаем белый фон
        self.canv.grid(row=2, column=0, columnspan=1,rowspan=3,
                       padx=5, pady=5, sticky=NW) 
        self.canv.bind("<B1-Motion>", self.draw) # Привязываем обработчик к канвасу. <B1-Motion> означает "при движении зажатой левой кнопки мыши" вызывать функцию draw
        self.canv.bind("<Button-1>", self.draw) # Привязываем обработчик к канвасу. <Button-1> означает "при нажатии левой кнопки мыши" вызывать функцию draw
        # Размещаем надписи 
        Label(self, text="Result: ").grid(row=2, column=1, padx=10,sticky=S) 
        ResultLabel = Label(self, text="   Инструкция:\nНарисовать букву и нажать SCAN")
        ResultLabel2 = Label(self, text="Нажать: \nTrue, если нарисованная буква правильная,\n False если нет")
        ResultLabel.grid (row=3, column=1, padx=10, columnspan=4, sticky=NW) 
        ResultLabel2.grid(row=4, column=1, padx=10, columnspan=4, sticky=NW) 
        
        color_lab = Label(self, text="Обучаемая буква: ") 
        color_lab.grid(row=0, column=0, padx=18) 

        # Размещаем кнопки
        red_btn = Button(self, text="True", width=6,
                         command=lambda: self.P1.incWeights()) # Определяем параметры кнопки
        red_btn.grid(row=0, column=1) # Устанавливаем кнопку в окно


        clear_btn = Button(self, text="Clear all", width=10,
                           command=lambda: self.canv.delete("all"))
        clear_btn.grid(row=0, column=2)
        
        save_button = Button(self, text="Save", width=10,
                           command=lambda: self.P1.save())
        save_button.grid(row=0, column=3, sticky=W)
        
        # Количество отображаемых чисел в спинбоксе from_=0, to=25
        size_lab = Spinbox(self, width=7, from_=0, to=CntSymbols,
                           command=lambda: self.P1.SetCurrentR(size_lab.get()))
        size_lab.grid(row=1, column=0, padx=10)
        
        one_btn = Button(self, text="False", width=6,
                         command=lambda: self.P1.decWeights()) 
        one_btn.grid(row=1, column=1)

        twenty_btn = Button(self, text="Scan", width=10,
                            command=lambda: self.getpixels())
        twenty_btn.grid(row=1, column=2)
        
        load_btn = Button(self, text="Load", width=10,
                           command=lambda: self.P1.load())
        load_btn.grid(row=1, column=3, sticky=W)
        
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
        # Помещение входных данных в экземпляр класса перцептрон
        self.P1.inputValues(colors)
        # Вызов функции, подготавливающей экземпляр класса к началу обучения
        self.P1.startTraining()

# Класс перцептрона
class Perceptron:
    global output
    global CurrentR
    
    # Функция установки текущего значения выхода R
    def SetCurrentR(self,CurrentR):
        self.CurrentR = int(CurrentR)
    
    # Инициализация переменных и массивов 
    def __init__(self):
        self.inputSet         = []
        self.synaptic_weights = []
        self.R_weights        = []
        self.A_weights        = []
        self.CurrentR         = 0
        
    # Функция установки входного сета
    def inputValues(self, inputSet):
        self.inputSet = inputSet;
        # Количество выходных нейронов
        self.cntR     = CntSymbols
        
    # Функция установки начального значения весов 
    def startTraining(self):
        if(len(self.synaptic_weights) == 0):
            random.seed(10)
            # вес связи от i-го A-элемента к j-му R элементу; 
            self.synaptic_weights = 2 * random.random(len(self.inputSet)) - 1
            # Связи от A к R (1 есть, 0 нет)
            self.R_weights = random.choice(2,(self.cntR,len(self.inputSet)))
            # Связи от S к A (1 есть, 0 нет)
            #self.A_weights = random.choice(2,(self.cntR,len(self.inputSet)))
            self.A_weights = random.choice(2,(len(self.inputSet),len(self.inputSet)))
        self.printSum()
    
    # Запускается при нажатии True
    # Увеличение весов при обучении
    def incWeights(self):
        self.synaptic_weights += self.inputSet*self.R_weights[self.CurrentR]
        self.printSum()
        
    # Запускается при нажатии False    
    # Уменьшение весов при обучении
    def decWeights(self):
        self.synaptic_weights -= self.inputSet*self.R_weights[self.CurrentR]
        self.printSum()
    
    # Расчет весов и вывод результата
    def printSum(self):
        # Расчет весов элементов A
        self.output = [0 for i in range(len(self.inputSet))]
        self.output += sum(self.inputSet * self.synaptic_weights *self.A_weights)
        sum_ = 0
        tmp = 0
        # Расчет весов элемента R
        readySum = [0 for i in range(0,self.cntR)]
        sum1_ = 0 
        for x in range(0,(len(self.output))): 
            tmp = 0
            for i in range(0,self.cntR):
                readySum[i] += self.output[x]*self.R_weights[i][x]
            sum1_ +=  self.output[x]*self.R_weights[1][x]
        sum_  +=  self.output*self.R_weights[0]
        # Вывод номера буквы с наибольшей суммой на экран
        if(max(readySum)>1000):
            ResultLabel['text'] = " № Буквы: "+str(readySum.index(max(readySum)))+"\n Сумма: "+str(round(max(readySum),3))
        else:
            ResultLabel['text'] = "  Буква не определена "
        # ResultLabel2['text'] = str(round(sum_,3))+" "+str(round(sum1_,3))
        # print(self.synaptic_weights)
        
    # Запускается при нажатии Save
    # Функция сохранения весов и связей в файл (data_file.json)
    def save(self):
        data = [[] for i in range(0,4)]
        data[0]=self.synaptic_weights.tolist()
        data[1]=self.R_weights.tolist()
        data[2]=self.A_weights.tolist()
        
        with open("data_file.json", "w") as write_file:
            json.dump(data, write_file)
            
    # Запускается при нажатии Load
    # Функция загрузки весов и связей из файла (data_file.json)
    def load(self):
        with open("data_file.json", "r") as read_file:
            data = json.load(read_file)
        self.synaptic_weights = array(data[0])
        self.R_weights        = array(data[1])
        self.A_weights        = array(data[2])
        
# Главная функция 
def main():
    global CntSymbols #Количество символов в алфавите
    CntSymbols=25 
    root = Tk()   
    # Настройка размера окна
    root.geometry("400x220+300+300")
    app = UI(root)
    # Главный цикл
    root.mainloop()

if __name__ == '__main__':
    main()