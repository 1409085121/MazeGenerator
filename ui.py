import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from Map import *
from PIL import Image, ImageDraw


class UI:
    def __init__(self, map: Map):
        self.map = map
        self.gridWidth = 20
        self.edgeWidth = 40
        self.mapWidth = map.width
        self.mapHeight = map.height
        self.root_width = (self.map.width-1) * self.gridWidth + self.edgeWidth*2
        self.root_height = (self.map.height-1) * self.gridWidth + self.edgeWidth*2 + 30

        self.root = Tk()
        self.root.title('Maze Generator')
        self.root.resizable(False, False)
        self.root.geometry(f"{self.root_width}x{self.root_height}")

        self.frame1 = Frame(self.root)
        self.frame1.pack(side=TOP, fill=X, expand=False)
        self.canvas = Canvas(self.root, bg='white')
        self.canvas.pack(fill=BOTH, expand=True)

        self.bt1 = Button(self.frame1, text="Fast generate", command=self.fast_generate)
        self.bt1.pack(side=LEFT)
        self.bt2 = Button(self.frame1, text="Save", command=self.save_as_file)
        self.bt2.pack(side=LEFT)
        self.bt3 = Button(self.frame1, text="Custom generate (drawing path)", command=self.start_draw_path)
        self.bt3.pack(side=LEFT)


        self.startPoint = Label(self.canvas, bg="green", text="S")
        self.endPoint = Label(self.canvas, bg="red", text="E")
        self.cursor = Label(self.canvas, bg="blue")

        self.cursorPosition = [0, 0]
        self.onDrawingPath = False
        self.nodesOnPath = []
        self.root.bind("<Key>", self.drawing_key_event)

    def drawing_key_event(self, event):
        if not self.onDrawingPath:
            return
        x = self.cursorPosition[0]
        y = self.cursorPosition[1]
        if event.keysym == 'Left':
            if self.cursorPosition[0] == 0:
                return
            if myMap.get_node(x-1, y) in self.nodesOnPath:
                return
            self.cursorPosition[0] -= 1
        elif event.keysym == 'Right':
            if self.cursorPosition[0] == self.mapWidth-2:
                return
            if myMap.get_node(x+1, y) in self.nodesOnPath:
                return
            self.cursorPosition[0] += 1
        elif event.keysym == 'Up':
            if self.cursorPosition[1] == 0:
                return
            if myMap.get_node(x, y-1) in self.nodesOnPath:
                return
            self.cursorPosition[1] -= 1
        elif event.keysym == 'Down':
            if self.cursorPosition[1] == self.mapHeight-2:
                return
            if myMap.get_node(x, y+1) in self.nodesOnPath:
                return
            self.cursorPosition[1] += 1

        self.nodesOnPath.append(myMap.get_node(self.cursorPosition[0], self.cursorPosition[1]))

        self.cursor.place(
            x=self.cursorPosition[0]*self.gridWidth+self.edgeWidth,
            y=self.cursorPosition[1]*self.gridWidth+self.edgeWidth
        )

        self.canvas.create_line(
            (self.nodesOnPath[-1].x+0.5) * self.gridWidth + self.edgeWidth,
            (self.nodesOnPath[-1].y+0.5) * self.gridWidth + self.edgeWidth,
            (self.nodesOnPath[-2].x+0.5) * self.gridWidth + self.edgeWidth,
            (self.nodesOnPath[-2].y+0.5) * self.gridWidth + self.edgeWidth,
            fill="blue", width=0.5*self.gridWidth
        )

        if self.cursorPosition[0] == self.mapWidth-2 and self.cursorPosition[1] == self.mapHeight-2:
            self.onDrawingPath = False
            self.custom_generate()

    def path_drawing_ui(self):
        self.canvas.delete("all")
        # draw grid
        for x in range(self.mapWidth):
            self.canvas.create_line(
                self.edgeWidth + self.gridWidth*x,
                self.edgeWidth,
                self.edgeWidth + self.gridWidth*x,
                self.edgeWidth + self.gridWidth*(self.mapHeight-1),
                fill="#ddd"
            )
        for y in range(self.mapHeight):
            self.canvas.create_line(
                self.edgeWidth,
                self.edgeWidth + self.gridWidth*y,
                self.edgeWidth + self.gridWidth*(self.mapWidth-1),
                self.edgeWidth + self.gridWidth*y,
                fill="#ddd"
            )

        self.startPoint.place(x=self.edgeWidth, y=self.edgeWidth, width=self.gridWidth, height=self.gridWidth)
        self.cursor.place(x=self.edgeWidth, y=self.edgeWidth, width=self.gridWidth, height=self.gridWidth)
        self.endPoint.place(
            x=self.edgeWidth + (self.mapWidth-2) * self.gridWidth,
            y=self.edgeWidth + (self.mapHeight-2) * self.gridWidth,
            width=self.gridWidth,
            height=self.gridWidth
        )

    def fast_generate(self):
        self.map = Map(self.mapWidth, self.mapHeight)
        self.map.generate_maze()
        self.canvas.delete("all")
        self.display()

    def start_draw_path(self):
        self.map = Map(self.mapWidth, self.mapHeight)
        self.onDrawingPath = True
        self.nodesOnPath = [myMap.get_node(0, 0)]
        self.cursorPosition = [0, 0]
        self.path_drawing_ui()

        self.bt1.config(state="disabled")
        self.bt2.config(state="disabled")
        messagebox.showinfo("Start",
            '''start drawing path:
Use the up, down, left, and right keys to move the cursor to draw the pattern you want.
Move the cursor to the end point (E) and start generating a maze. Press the "Custom generate (drawing path)" button again to redraw.
            '''
        )

    def custom_generate(self):

        self.bt1.config(state="normal")
        self.bt2.config(state="normal")

        for i in range(len(self.nodesOnPath)-1):
            node1 = self.nodesOnPath[i]
            node2 = self.nodesOnPath[i+1]
            if node2.y > node1.y:
                node3: Node = self.map.get_node(node1.x, node1.y+1)
                node4: Node = self.map.get_node(node1.x+1, node1.y+1)
            elif node2.y < node1.y:
                node3: Node = self.map.get_node(node1.x, node1.y)
                node4: Node = self.map.get_node(node1.x+1, node1.y)
            elif node2.x > node1.x:
                node3: Node = self.map.get_node(node1.x+1, node1.y)
                node4: Node = self.map.get_node(node1.x+1, node1.y+1)
            elif node2.x < node1.x:
                node3: Node = self.map.get_node(node1.x, node1.y)
                node4: Node = self.map.get_node(node1.x, node1.y+1)
            else:
                raise IndexError()

            self.map.new_invisible_connection(node3, node4)

        for x in range(self.map.width):
            for y in range(self.map.height):
                print(self.map.get_node(x, y).connections_count, end=" ")
            print()
        self.map.generate_maze(initialize=False)
        self.display()


    def save_as_file(self):
        fileName = filedialog.asksaveasfilename(
            filetypes=[("JPEG", "*.jpg")],
            initialfile="New maze.jpg"
        )
        self.getter(fileName)

    def getter(self, filename):
        white = (222, 222, 220)
        black = (0,0,0)
        width = (self.map.width-1) * self.gridWidth + self.edgeWidth*2
        height = (self.map.height-1) * self.gridWidth + self.edgeWidth*2
        image1 = Image.new("RGB", (width, height), white)
        draw = ImageDraw.Draw(image1)
        for connection in self.map.connectionList:
            if not connection.visible:
                continue
            draw.line(
                [
                    self.edgeWidth + connection.x1 * self.gridWidth,
                    self.edgeWidth + connection.y1 * self.gridWidth,
                    self.edgeWidth + connection.x2 * self.gridWidth,
                    self.edgeWidth + connection.y2 * self.gridWidth,
                ],
                fill=black
            )
        image1.save(filename)

    def display(self):
        for connection in self.map.connectionList:
            if not connection.visible:
                continue
            self.canvas.create_line(
                self.edgeWidth + connection.x1 * self.gridWidth,
                self.edgeWidth + connection.y1 * self.gridWidth,
                self.edgeWidth + connection.x2 * self.gridWidth,
                self.edgeWidth + connection.y2 * self.gridWidth,
                fill="black",
                width=1
            )

        self.root.mainloop()


if __name__ == '__main__':
    myMap = Map(20, 20)
    myMap.generate_maze()
    myUI = UI(myMap)
    myUI.display()
