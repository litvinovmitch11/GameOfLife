from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


width = 800
height = 600

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)


class Point(object):
    def __init__(self, x, y, key=0):
        self.x = x
        self.y = y
        self.key = key

    def draw(self):
        def set_color(key):
            if key == 0:
                return Color(1., 1., 1.)
            elif key == 1:
                return Color(0, 0, 0)

        set_color(self.key)
        Rectangle(pos=(self.x * 10 + 1, self.y * 10 + 1), size=(8, 8))


class Grid(object):
    def __init__(self):
        self.grid = []
        for i in range(width//10):
            line = []
            for j in range(height//10):
                line.append(Point(i, j))
            self.grid.append(line)

    def update(self):

        def point_value(x, y):
            try:
                return self.grid[x][y].key
            except IndexError:
                return 0

        birth = []
        death = []

        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                mas = 0

                mas += point_value(i - 1, j - 1)
                mas += point_value(i - 1, j)
                mas += point_value(i - 1, j + 1)
                mas += point_value(i, j - 1)
                mas += point_value(i, j + 1)
                mas += point_value(i + 1, j - 1)
                mas += point_value(i + 1, j)
                mas += point_value(i + 1, j + 1)

                if mas == 3 and self.grid[i][j].key == 0:
                    birth.append([i, j])
                elif mas == 2 or mas == 3:
                    pass
                else:
                    death.append([i, j])

        for pair in birth:
            self.grid[pair[0]][pair[1]].key = 1
        for pair in death:
            self.grid[pair[0]][pair[1]].key = 0


class Canvas(Widget):
    def __init__(self):
        super(Canvas, self).__init__()
        self.grid = Grid()
        self.draw_grid()
        Clock.schedule_interval(lambda dt: self.logic(), 0.01)

    key = 0

    @staticmethod
    def switch():
        Canvas.key ^= 1

    def logic(self):
        if Canvas.key == 1:
            self.grid.update()
        self.draw_points()

    def on_touch_down(self, touch):
        if Canvas.key == 0:
            a, b = touch.pos
            x, y = (round(a))//10, (round(b) - 2)//10
            self.grid.grid[x][y].key ^= 1

    def draw_grid(self):
        with self.canvas:
            Color(1., 1., 1.)
            Rectangle(pos=(0, 0), size=(width, height))

            Color(0.882, 0.882, 0.882)
            for i in range(width // 10):
                Line(points=[i * 10, 0, i * 10, height], width=2)
            for j in range(height // 10):
                Line(points=[0, j*10, width, j*10], width=2)

    def draw_points(self):
        with self.canvas:
            for line in self.grid.grid:
                for point in line:
                    point.draw()


class MyApp(App):

    def build(self):
        layout = FloatLayout(size=(width, height))
        canvas = Canvas()
        button = Button(
            text="click to start/stop",
            font_size=15,
            size_hint=(.2, .05),
            pos=(0, 0),
            on_press=lambda _: canvas.switch())
        layout.add_widget(canvas)
        layout.add_widget(button)
        return layout


if __name__ == '__main__':
    MyApp().run()
