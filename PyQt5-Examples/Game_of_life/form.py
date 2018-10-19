
import sys
from random import randint
import numpy

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QBrush

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter

from maingui import Ui_MainWindow
import model


# The main form class - application entry point
# form.ui imported from maingui.py
class Form(QMainWindow):
    
    
    def __init__(self, parent=None):
        
        super(Form, self).__init__(parent)
        
        self.scale = 6
        self.new_life = True
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # The default shape is glider gun
        self.ui.radio_glider_gun.setChecked(True)
        
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.ui.surface.setScene(self.scene)
        
        self.ui.surface.setCacheMode(QGraphicsView.CacheBackground)
        
        self.color = QColor(0, 0, 0)
        self.brush = QBrush(self.color)
        self.pen = QPen()
        
        # Initialize the scene timer
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        
        # Connect button event handlers
        
        self.ui.button_start.clicked.connect(
                self.button_start_clicked)
        
        self.ui.button_pause.clicked.connect(
                self.button_pause_clicked)
        
        self.ui.button_stop.clicked.connect(
                self.button_stop_clicked)
        
    
    # The start button event handler
    def button_start_clicked(self):
        
        if self.new_life:
            self.new_life = False
            self.life_shape = self.select_life()
            self.matrix = model.first_generation(
                    100, 100, self.life_shape)
        self.timer.start(10)
        
    
    # The pause button event handler
    def button_pause_clicked(self):        
        self.timer.stop()
        
    
    # The stop button event handler
    def button_stop_clicked(self):
        
        self.timer.stop()
        self.scene.clear()
        self.new_life = True
    
    
    # Which game of life shape the user selected?
    def select_life(self):
        
        if self.ui.radio_toad.isChecked():
            life = model.TOAD
        elif self.ui.radio_beacon.isChecked():
            life = model.BEACON
        elif  self.ui.radio_glider.isChecked():
            life = model.GLIDER
        elif self.ui.radio_glider_gun.isChecked():
            life = model.GLIDER_GUN
        elif self.ui.radio_life_spaceship.isChecked():
            life = model.LIFE_SPACESHIP
        elif self.ui.radio_pentomino.isChecked():
            life = model.PENTOMINO
            
        return life
        
    
    # Draw the game of life generation
    def draw(self):
        
        self.scene.clear()
        
        for (x, y), value in numpy.ndenumerate(self.matrix):

            if value == 1:
                
                x_sc = x * self.scale
                y_sc = y * self.scale
                rect = QRectF(x_sc, y_sc, self.scale, self.scale)
                self.scene.addRect(rect, self.pen, self.brush)
                
        self.matrix = model.next_generation(self.matrix)
        
        

def main():
    
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
