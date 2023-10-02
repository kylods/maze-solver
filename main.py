from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
    def __init__(self, w, h):
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.canvas = Canvas(width = w, height = h)
        self.canvas.pack()
        self.__is_running = False
        #Triggers self.close when window is closed
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running == True:
            self.redraw()
        
    def close(self):
        self.__is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
            )
        canvas.pack()

class Cell():
    def __init__(self, p1, p2, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = p1.x
        self.x2 = p2.x
        self.y1 = p1.y
        self.y2 = p2.y
        self._win = window
        self.visited = False

    def draw(self):
        tl = Point(self.x1, self.y1)
        br = Point(self.x2, self.y2)
        tr = Point(self.x2, self.y1)
        bl = Point(self.x1, self.y2)
 
        if self.has_left_wall:
            self._win.draw_line(Line(tl, bl), 'black')
        else:
            self._win.draw_line(Line(tl, bl), 'white')
        if self.has_right_wall:
            self._win.draw_line(Line(tr, br), 'black')
        else:
            self._win.draw_line(Line(tr, br), 'white')
        if self.has_top_wall:
            self._win.draw_line(Line(tl, tr), 'black')
        else:
            self._win.draw_line(Line(tl, tr), 'white')
        if self.has_bottom_wall:
            self._win.draw_line(Line(bl, br), 'black')
        else:
            self._win.draw_line(Line(bl, br), 'white')

    def draw_move(self, to_cell, undo=False):
        self_center = Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        to_center = Point((to_cell.x1 + to_cell.x2) // 2, (to_cell.y1 + to_cell.y2) // 2)
        if undo == False:
            self._win.draw_line(Line(self_center, to_center), 'blue')
        else:
            self._win.draw_line(Line(self_center, to_center), 'gray')

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        

        for i in range(self.num_cols):
            working_list = []

            for j in range(self.num_rows):
                working_list.append(Cell(
                    Point(self.cell_size_x * i + self.x1, self.cell_size_y * j + self.y1),
                    Point(self.cell_size_x * (i + 1) + self.x1, self.cell_size_y * (j + 1) + self.y1),
                    self._win
                    ))

            self._cells.append(working_list)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_dfs(0, 0)
        self._reset_cells_visited()

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        
        cell.draw()

        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[self.num_cols - 1][self.num_rows - 1]

        exit_cell.has_bottom_wall = False
        entrance_cell.has_top_wall = False
        
        self._draw_cell(0, 0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)
        
    def _break_walls_dfs(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        directions = [
            ('North', 0, -1),
            ('South', 0, 1),
            ('West', -1, 0),
            ('East', 1, 0)
        ]
        
        random.shuffle(directions)
        
        for direction, dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
                if direction == 'North':
                    current_cell.has_top_wall = False
                    self._cells[ni][nj].has_bottom_wall = False
                elif direction == 'South':
                    current_cell.has_bottom_wall = False
                    self._cells[ni][nj].has_top_wall = False
                elif direction == 'West':
                    current_cell.has_left_wall = False
                    self._cells[ni][nj].has_right_wall = False
                elif direction == 'East':
                    current_cell.has_right_wall = False
                    self._cells[ni][nj].has_left_wall = False
                
                self._break_walls_dfs(ni, nj)
        
        self._draw_cell(i, j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False
        
    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i=0, j=0):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        directions = [
            ('North', 0, -1),
            ('South', 0, 1),
            ('West', -1, 0),
            ('East', 1, 0)
        ]

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        
        for direction, dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
                if direction == 'North' and not current_cell.has_top_wall:
                    current_cell.draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    else:
                        current_cell.draw_move(self._cells[ni][nj], undo=True)
                if direction == 'South' and not current_cell.has_bottom_wall:
                    current_cell.draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    else:
                        current_cell.draw_move(self._cells[ni][nj], undo=True)
                if direction == 'East' and not current_cell.has_right_wall:
                    current_cell.draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    else:
                        current_cell.draw_move(self._cells[ni][nj], undo=True)
                if direction == 'West' and not current_cell.has_left_wall:
                    current_cell.draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    else:
                        current_cell.draw_move(self._cells[ni][nj], undo=True)

                
        
        return False
        

def main():
    win = Window(800, 600)

    #line1 = Line(Point(12), Point(415, 244))
    #line2 = Line(Point(400, 242), Point(400, 5))
    #win.draw_line(line1, 'black')
    #win.draw_line(line2, 'red')
    maze = Maze(10, 10, 19, 26, 30, 30, win)
    maze.solve()
    win.wait_for_close()

main()