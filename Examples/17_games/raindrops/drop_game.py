

import sys, random

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QObject, QTimer, QEvent
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QColor, QPixmap


class Window(QWidget):
       
    WIDTH = 860
    HEIGHT = 540
    SPEED = 300

    def __init__(self):
        
        super().__init__()
               
        self.is_started = False
        self.is_paused = False

        timer = QTimer()
        timer.setInterval(Window.SPEED)

        self.initUi(timer)
    
        self.show()
          
        
    def initUi(self, timer):

        self.resize(Window.WIDTH, Window.HEIGHT)        
        
        layout = QGridLayout()
        
        button_start = QPushButton('Start')
        button_pause = QPushButton('Pause / Resume')
        
        button_start.clicked.connect(
                lambda: self.start(timer))
        button_pause.clicked.connect(
                lambda: self.pause(timer))
                
        self.label_cought = QLabel('Raindrops cought: 0')
        self.label_cought.setAlignment(Qt.AlignCenter)
        self.label_missed = QLabel('Raindrops missed: 0')
        self.label_missed.setAlignment(Qt.AlignCenter)
        
        scene = GraphicsScene()
        view = GraphicsView()
        view.setScene(scene)

        scene.add_bucket()
              
        timer.timeout.connect(
                lambda: view.paint_scene(scene))
                
        timer.timeout.connect(
                lambda: self.update_score(view))

        scene_brush = QBrush(Qt.darkBlue)
        scene.setBackgroundBrush(scene_brush)    
        
        layout.addWidget(button_start, 0, 0)
        layout.addWidget(button_pause, 0, 1)
        layout.addWidget(self.label_cought, 0, 2)
        layout.addWidget(self.label_missed, 0, 3)
        layout.addWidget(view, 1, 0, 4, 4)
        
        self.setLayout(layout)
        

    def start(self, timer):
        
        if not self.is_paused:
            self.is_started = True
            timer.start(Window.SPEED)


    def pause(self, timer):
        
        if not self.is_started:
            return

        self.is_paused = not self.is_paused
        
        if self.is_paused:
            timer.stop()            
        else:
            timer.start(Window.SPEED)


    def update_score(self, view):
        
        self.label_cought.setText(
                'Raindrops cought: {}'.format(str(view.cought)))
                
        self.label_missed.setText(
                'Raindrops missed: {}'.format(str(view.missed)))


class GraphicsView(QGraphicsView):

    WIDTH = 840
    HEIGHT = 500
    
    def __init__(self):
        
        super(GraphicsView, self).__init__()
                
        self.setFixedSize(
                GraphicsView.WIDTH, GraphicsView.HEIGHT)
                
        self.cought = 0
        self.missed = 0
                
            
    def paint_scene(self, scene):
        
        scene.add_droplet()

        for item in scene.items():
            if item.data(0) == 'droplet':
                item.setY(item.y() + 20)
                
        bucket = scene.bucket_item

        for droplet in scene.droplets:
            
            if droplet:
                if bucket.collidesWithItem(droplet):
                    scene.droplets.remove(droplet)
                    scene.removeItem(droplet)
                    self.cought += 1
                
            if droplet:
                if droplet.y() > scene.HEIGHT:
                    scene.droplets.remove(droplet)
                    scene.removeItem(droplet)
                    self.missed += 1
 


class GraphicsScene(QGraphicsScene):

    WIDTH = 800
    HEIGHT = 480
    
    def __init__(self):
        
        super(GraphicsScene, self).__init__()
        
        self.installEventFilter(self)
        self.setSceneRect(
                0, 0, GraphicsScene.WIDTH,
                GraphicsScene.HEIGHT)
                
        self.bucket_created = False                     
        self.add_bucket()
        self.bucket_created = True
        
        self.droplets = list()  

        

    def add_bucket(self):

        if not self.bucket_created:
            
            bucket_pixmap = QPixmap('images/bucket.png')
            
            self.bucket_item = QGraphicsPixmapItem(bucket_pixmap)
            self.bucket_item.setPos(368, 416)
            self.bucket_item.setData(0, 'bucket')
            
            self.addItem(self.bucket_item)


    def add_droplet(self):

        to_add = random.randint(0, 1)

        if to_add == 1:
            
            x = random.randint(0, GraphicsScene.WIDTH - 64)
            y = 0

            drop_pixmap = QPixmap('images/droplet.png')
            self.drop_item = QGraphicsPixmapItem(drop_pixmap)
            self.drop_item.setPos(x, y)
            self.drop_item.setData(0, 'droplet')
            self.addItem(self.drop_item)
            
            self.droplets.append(self.drop_item)



    def eventFilter(self, source, event):

        if event.type() == QEvent.KeyPress:

            key = event.key()
            x = self.bucket_item.x()
            y = self.bucket_item.y()
            
            if key == Qt.Key_Right:
                if x <= GraphicsScene.WIDTH - 64:
                    self.bucket_item.setPos(x + 20, y)
            elif key == Qt.Key_Left:
                if x >= 0:
                    self.bucket_item.setPos(x - 20, y)
            return True

        else:
            return QObject.eventFilter(self, source, event)
       


if __name__ == '__main__':
    
    app = QApplication([])
    window = Window()    
    sys.exit(app.exec_())
