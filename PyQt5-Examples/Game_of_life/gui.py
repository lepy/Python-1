

import tkinter as tk
import view


class Application(tk.Frame):
    
    def __init__(self, root=None):
        
        super().__init__(root)
        self.root = root
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        self.selected = tk.IntVar()

        self.blinker = tk.Radiobutton(
                self, 
                text='blinker', 
                variable=self.selected,
                value=1)
                
        self.toad = tk.Radiobutton(
                self, 
                text='toad', 
                variable=self.selected,
                value=2)
                
        self.blinker.pack(side='top')
        self.toad.pack(side='top')

        self.start = tk.Button(
                self,
                text='Start',
                command=self.animate)


        self.quit = tk.Button(
                self, 
                text="Quit", 
                command=self.root.destroy)
                
        self.quit.pack(side='bottom')
        self.start.pack(side='bottom')

    def animate(self):
        print(self.selected.get())
        val = self.selected.get()
        view.loop(100, 100, 6, val)
        


def main():
    root = tk.Tk()
    app = Application(root=root)
    app.mainloop()

if __name__ == '__main__':
    main()
