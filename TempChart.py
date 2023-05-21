from PySide6.QtWidgets import QWidget, QHBoxLayout, QSlider, QMessageBox, QPushButton, QColorDialog
from PySide6.QtCharts import QChart, QLineSeries, QChartView, QSplineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor, QMouseEvent, QPen


#Foto von Programm hinzufügen

class TempChart(QWidget):
    def __init__(self, parent):
        super(TempChart, self).__init__(parent)

        self.axis_time = QDateTimeAxis()
        self.axis_time.setTitleText("Datumachse")
        self.axis_time.setFormat("dd.MM")
        #self.axis_time.setFormat("mm.ss")
        self.axis_time.setTickCount(6)
        self.color = QColor("red")
        self.axis_time.setGridLineColor(self.color) #QColorDialog
        self.axis_time.setRange(QDateTime.currentDateTime(), QDateTime.currentDateTime().addDays(5))
        #self.axis_time.setRange(QDateTime.currentDateTime(), QDateTime.currentDateTime().addSecs(5 * 60))

        self.axis_percent = QValueAxis()
        self.axis_percent.setLabelFormat("%.2f" + "EUR")
        self.axis_percent.setTitleText("Euro")
        self.axis_percent.setRange(0, 100)


        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("x-Achse")
        self.axis_x.setRange(0, 5)

        #self.min = 0
        #self.max = 5
        #self.mid = (self.min + self.max) / 2
        #self.axis_x.setRange(self.min, self.max)
        #self.pen = QPen(Qt.SolidLine)
        #self.pen.setColor(Qt.black)
        #self.pen.setWidth(2)
        #self.axis_x.setLinePen(self.pen)
        #self.axis_x.setLine(self.mid)


        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("y-Achse")
        self.axis_y.setRange(0, 20)

        self.chart = QChart()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_time, Qt.AlignTop)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.chart.addAxis(self.axis_percent, Qt.AlignRight)

        self.chart_view = QChartView()
        self.chart_view.setChart(self.chart)

        self.my_layout = QHBoxLayout()
        self.my_layout.addWidget(self.chart_view)
        self.setLayout(self.my_layout)

        self.slider = QSlider() #Wert von 0 bis 100
        self.slider.valueChanged.connect(self.addPoint)
        #self.slider.setRange(25,50) #=Werte zwischen 25 und 50
        self.slider.setValue(50) #=Startwert ist 50
        self.my_layout.addWidget(self.slider)

        self.btn_changecolor = QPushButton("Farbe wählen", self)
        self.btn_changecolor.clicked.connect(self.setColor)
        self.my_layout.addWidget(self.btn_changecolor)


        self.series = QSplineSeries()
        self.chart.addSeries(self.series)
        self.series.setName("Eurobetrag")
        #self.series.setName("f(x) = x^2")
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        #Punkte nach Ticks
        self.series.append(0, 0)
        self.series.append(1, 1)
        self.series.append(2, 4)
        self.series.append(3, 9)
        self.series.append(4, 16)
        self.series.append(5, 25)

        self.series_2 = QLineSeries()
        self.chart.addSeries(self.series_2)
        self.series_2.attachAxis(self.axis_time)
        self.series_2.attachAxis(self.axis_percent)
        self.series_2.setName("Prozent über Zeit")

    def setColor(self):
        selected_color = QColorDialog.getColor(self.color, self)

        if selected_color.isValid():
            self.color = selected_color
            self.axis_time.setGridLineColor(self.color)  # QColorDialog

    def addPoint(self, percent):
        self.series_2.append(QDateTime.currentDateTime().toMSecsSinceEpoch(), percent)
#(Tageszeit, aktuelle Zeit, inMSecs >>> seit jesus Christus, in prozent (ist sonst zulang)
    def mousePressEvent(self, event: QMouseEvent):
        if event.isBeginEvent():
            event.accept()
            self.series_2.setName("Du hälst die Maus gedrückt.")
        elif event.isEndEvent():
            event.accept()
            self.series_2.setName("Du hälst die Maus nicht mehr gedrückt.")

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.series_2.setName("Du hälst die Maus nicht mehr gedrückt.")

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        msgBox = QMessageBox()

        text = "Sie haben auf die Position\n"
        text += "x: " + str(event.x()) + "\n"
        text += "y: " + str(event.y()) + "\n"
        text += "global x: " + str(event.globalX()) + "\n"
        text += "global y: " + str(event.globalY()) + "\n"
        text += "doppelt geklickt."

        msgBox.setText(text)

        msgBox.exec()

        #Zeichnen mit Doppelklick
        maped_point = self.chart.mapToValue(event.pos(), self.series_2)
        self.series_2.append(maped_point)

