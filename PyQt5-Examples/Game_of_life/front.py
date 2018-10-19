
import pygame
from pygame.locals import *
import tkinter
import random
import sys
import model
import numpy


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BLINKER = [[50, 49], [50, 50], [50, 51]]

TOAD = [[50, 49], [50, 50], [50, 51],
        [51, 48], [51, 49], [51, 50]]
        
BEACON = [[50, 50], [50, 51],
          [51, 50], [51, 51],
          [52, 52], [52,  53],
          [53, 52], [53, 53]]
          
GLIDER = [[50, 50], [51, 51], 
          [52, 49], [52, 50], [52, 51]]
          
GLIDER_GUN = [[5, 1], [5, 2], [6, 1], 
              [6, 2], [5, 11], [6, 11],
              [7, 11], [4, 12], [3, 13],
              [3, 14], [8, 12], [9, 13],
              [9, 14], [6, 15], [4, 16],
              [5, 17], [6, 17], [7, 17],
              [6, 18], [8, 16], [3, 21],
              [4, 21], [5, 21], [3, 22],
              [4, 22], [5, 22], [2, 23],
              [6, 23], [1, 25], [2, 25],
              [6, 25], [7, 25], [3, 35],
              [4, 35], [3, 36], [4, 36],[40, 50]]
              
LIFE_SPACESHIP = [[52, 50], [54, 50], [51, 51],
                  [51, 52], [51, 53], [54, 53], 
                  [51, 54], [52, 54], [53, 54]]
                  
PENTOMINO = [[50, 50], [50, 51], [49, 51], 
             [50, 52], [51, 52]]


class Window(tkinter.Frame):
    
    
    def __init__(self, root=None):
        
        self.done = False
        self.running = False
        
        self.clock = pygame.time.Clock()        
        
        tkinter.Frame.__init__(self, root)
        self.root = root
        self.init_window()
        self.pack()
        self.init_pygame()  
       
        
    def init_window(self):
        
        self.root.title('Game of life')
        self.root.protocol(
                "WM_DELETE_WINDOW", 
                self.quit_callback)
                
        self.options = tkinter.LabelFrame(
                self.root,
                text = 'Select a shape')
        self.options.pack(fill='both', expand='yes', side='left')
        
        self.choice = tkinter.IntVar()
        self.choice.set(5)
        self.grid_width = tkinter.IntVar()
        self.grid_width.set(100)
        self.grid_height = tkinter.IntVar()
        self.grid_height.set(100)
        self.cell_size = tkinter.IntVar()
        self.cell_size.set(4)
        
        self.option_blinker = tkinter.Radiobutton(
                self.options,
                text='Blinker',
                padx=20,
                variable=self.choice,
                value=1)
        self.option_blinker.pack(anchor='w')
        
        self.option_toad = tkinter.Radiobutton(
                self.options,
                text='Toad',
                padx=20,
                variable=self.choice,
                value=2)
        self.option_toad.pack(anchor='w')
        
        self.option_beacon = tkinter.Radiobutton(
                self.options,
                text='Beacon',
                padx=20,
                variable=self.choice,
                value=3)
        self.option_beacon.pack(anchor='w') 
        
        self.option_glider = tkinter.Radiobutton(
                self.options,
                text='Glider',
                padx=20,
                variable=self.choice,
                value=4)
        self.option_glider.pack(anchor='w')
        
        self.option_glider_gun = tkinter.Radiobutton(
                self.options,
                text='Glider gun',
                padx=20,
                variable=self.choice,
                value=5)
        self.option_glider_gun.pack(anchor='w')
        
        self.option_life_spaceship = tkinter.Radiobutton(
                self.options,
                text='Life spaceship',
                padx=20,
                variable=self.choice,
                value=6)
        self.option_life_spaceship.pack(anchor='w')
        
        self.option_pentomino = tkinter.Radiobutton(
                self.options,
                text='Pentomino',
                padx=20,
                variable=self.choice,
                value=7)
        self.option_pentomino.pack(anchor='w')
        
        self.grid_options = tkinter.LabelFrame(
                self.root,
                text = 'Grid options')
        self.grid_options.pack(fill='both', expand='yes', side='left')
        
        self.label_width = tkinter.Label(self.grid_options, text='Width')
        self.label_width.pack(anchor='n')
        
        self.entry_width = tkinter.Entry(self.grid_options, width=10, textvariable=self.grid_width)
        self.entry_width.pack(anchor='n')
        
        self.label_height = tkinter.Label(self.grid_options, text='Height')
        self.label_height.pack(anchor='n')
        
        self.entry_height = tkinter.Entry(self.grid_options, width=10, textvariable=self.grid_height)
        self.entry_height.pack(anchor='n')        
               
        self.label_cell = tkinter.Label(self.grid_options, text='Cell size')
        self.label_cell.pack(anchor='n')
        
        self.entry_cell = tkinter.Entry(self.grid_options, width=10, textvariable=self.cell_size)
        self.entry_cell.pack(anchor='n')               
        
        self.start_stop_options = tkinter.LabelFrame(
                self.root,
                text = 'Start game')
        self.start_stop_options.pack(fill='both', expand='yes', side='left')
        
        self.button_start = tkinter.Button(self.start_stop_options, text='Start', command=self.start, width=10)
        self.button_start.pack(anchor='n')
        
        self.button_pause = tkinter.Button(self.start_stop_options, text='Pause', command=self.pause, width=10)
        self.button_pause.pack(anchor='n')
        
        self.button_stop = tkinter.Button(self.start_stop_options, text='Stop', command=self.resume, width=10)
        self.button_stop.pack(anchor='n')        
        
        
    def init_pygame(self):
        
        self.screen_size = (
                self.grid_width.get() * self.cell_size.get(),
                self.grid_height.get() * self.cell_size.get())
        self.surface = pygame.display.set_mode(self.screen_size)
        pygame.init()
   

    def draw(self, surface, matrix, scale):
        
        surface.fill(WHITE)
        for (x, y), value in numpy.ndenumerate(matrix):
            if value == 1:
                pygame.draw.rect(
                        surface, 
                        BLACK, 
                        ((x * scale, y * scale), 
                         (scale, scale)))
                     
        pygame.display.flip()


    def get_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN:
                print(event)
            if event.type == MOUSEBUTTONDOWN:
                print(event)
                sys.stdout.flush()
        return False


    def get_matrix(self):
        
        index = self.choice.get()
        
        if index == 1:
            matrix = BLINKER
        elif index == 2:
            matrix = TOAD
        elif index == 3:
            matrix = BEACON
        elif index == 4:
            matrix = GLIDER
        elif index == 5:
            matrix = GLIDER_GUN
        elif index == 6:
            matrix = LIFE_SPACESHIP
        else:
            matrix = PENTOMINO
            
        return matrix


    def quit_callback(self):
        self.done = True
        

    def start(self):
        self.running = True
        self.loop()
       
        
    def pause(self):
        print(self.running)
        self.running = False
        
        
    def resume(self):
        print('in resume')
        print(self.running)
        self.running = True
        

    def loop(self):
        
        print('loop')
        width = self.grid_width.get()
        height = self.grid_height.get()
        scale = self.cell_size.get()
        
        matrix = model.first_generation(
                width, height, 
                self.get_matrix())

        while not self.done:
            if self.running:
                try:
                    self.root.update()
                except:
                    print("dialog error")

                if self.get_input(): 
                    break
                self.draw(self.surface, matrix, scale)
                matrix = model.next_generation(matrix)
            self.clock.tick(20)

        self.root.destroy()


if __name__ == '__main__': 
    
    root = tkinter.Tk()
    window = Window(root)
    root.mainloop()

    


