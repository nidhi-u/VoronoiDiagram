import tkinter as tk
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np


class MainWindow:
    RADIUS = 3                              # radius of drawn points on canvas
    LOCK_FLAG = False                       # flag to lock the canvas when drawn

    def __init__(self, master):
        '''
        Initialises and creates a frame with a canvas and three buttons
        '''
        self.master = master
        self.master.title("Voronoi")

        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.width = 500
        self.height = 500
        self.w = tk.Canvas(self.frmMain, width=self.width, height=self.height)
        self.w.configure(background='white')

        # plotting points by double clicking
        self.w.bind('<Double-1>', self.onDoubleClick)
        self.w.pack()

        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack()

        self.btnCalculate = tk.Button(self.frmButton, text='Calculate', width=20, command=self.onClickCalculate)
        self.btnCalculate.pack(side=tk.LEFT)

        self.btnClear = tk.Button(self.frmButton, text='Clear', width=20, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)

        self.btnContinue = tk.Button(self.frmButton, text='Continue', width=20, command=self.onClickContinue)
        self.btnContinue.pack(side=tk.LEFT)

        self.btnToxicDump = tk.Button(self.frmButton, text='Toxic Dump', width=20, command=self.onClickDump)
        self.btnToxicDump.pack(side=tk.LEFT)


    def onClickCalculate(self):
        '''
        Locates the points drawn and generates Voronoi diagram for those points
        '''
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True           # disables point plotting

            pObj = self.w.find_all()        # locates points drawn
            points = []
            for p in pObj:
                coord = self.w.coords(p)
                points.append((coord[0] + self.RADIUS,500 - (coord[1] + self.RADIUS)))  # adding radius value to get the exact value

            vor = Voronoi(points)
            voronoi_plot_2d(vor)
            plt.show()

    def onClickClear(self):
        '''
        Unlocking the canvas and clearing all the previouly drawn points
        '''
        self.LOCK_FLAG = False
        self.w.delete(tk.ALL)

    def onDoubleClick(self, event):
        '''
        Plots point on event of double click
        '''
        if not self.LOCK_FLAG:
            # generating oval
            self.w.create_oval(event.x - self.RADIUS, event.y - self.RADIUS, event.x + self.RADIUS,
                               event.y + self.RADIUS, fill="blue")

    def onClickContinue(self):
        '''
        Unlocks the flag without deleting previously plotted points
        '''
        self.LOCK_FLAG = False

    def onClickDump(self):
        '''
        Finds ideal location for toxic dump
        (Largest Empty Circle Problem)
        '''
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True           # disables point plotting

            pObj = self.w.find_all()        # locates points drawn
            points = []
            for p in pObj:
                coord = self.w.coords(p)
                points.append((coord[0] + self.RADIUS,500 - (coord[1] + self.RADIUS)))  # adding radius value to get the exact value

            findingMax = {}
            vor = Voronoi(points)
            vertices = vor.vertices
            for vertex in vertices:
                findingMin = []
                for point in points:
                    dist = np.sqrt(np.square(vertex[0] - point[0]) + np.square(vertex[1] - point[1]))
                    findingMin.append(dist)

                findingMax.__setitem__(min(findingMin), vertex)

            radius = max(findingMax.keys())
            center = findingMax[radius]

            x = []
            y = []
            for point in points:
                x.append(point[0])
                y.append(point[1])
            fig, ax = plt.subplots(1, 1)
            voronoi_plot_2d(vor, ax)
            draw_circle = plt.Circle((center[0], center[1]), radius, fill=False)
            ax.add_artist(draw_circle)
            plt.show()


def drawOnCanvas():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

def genRandom():
    '''
    Generates n random data points where n is taken from user as input
    It then plots a Voronoi diagram for those points
    '''
    num_v = int(input("Enter number of vertices:\n"))
    coords = np.random.rand(num_v, 2).tolist()             # generating random 2D points
    rand_vor = Voronoi(coords)                             # generating Voronoi diagram
    voronoi_plot_2d(rand_vor)                              # plotting the diagram
    plt.show()

def main():
    while True:
        choice = input("Choose one of the following: 1. Plot on Canvas 2. Generate random\n")
        if choice == "1":
            drawOnCanvas()
            break

        elif choice == "2":
            genRandom()
            break

        else:
            print("Please enter a valid choice")



if __name__ == '__main__':
    main()