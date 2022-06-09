import tkinter as tk
from tkinter import ttk

class Ghost():
    def __init__(self, x, y):
        self.back = -2
        self.x = x
        self.y = y
        self.visited=[x, y]
        self.color = 'white'

    @property
    def back(self):
        return self._back

    @back.setter
    def back(self, value):
        self._back = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value
    
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def save(self):
        return (self.back, self.x, self.y, self.visited)