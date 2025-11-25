from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor


class SimulationCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ball_x = 100.0
        self.ball_y = 300.0
        self.ball_radius = 20

        self.vx = 200.0
        self.vy = -400.0

        self.g = 800

        self.path_points = []

        self.wall_restitution = 0.7

        self.setMinimumSize(600,400)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(240,240,240))

        #ground line
        ground_y = self.height()
        painter.setPen(QColor(180, 180, 180))
        painter.drawLine(0, ground_y - 1, self.width(), ground_y - 1)

        #trajectory
        if self.path_points:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(120, 120, 120))
            dot_radius = 3
            for px, py in self.path_points:
                cx = int(px)
                cy = int(py)
                painter.drawEllipse(cx - dot_radius, cy - dot_radius,
                                    dot_radius * 2, dot_radius * 2)

        #ball
        x_center = int(self.ball_x)
        y_center = int(self.ball_y)

        x = x_center - self.ball_radius
        y = y_center - self.ball_radius
        diameter = self.ball_radius*2

        painter.setBrush(QColor(80,160,255))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x,y,diameter,diameter)
