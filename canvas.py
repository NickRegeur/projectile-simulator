from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygonF


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

        self.show_trajectory = True
        self.ghost_points = []

        self.setMinimumSize(600,400)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(250,250,252))

        #ground line
        ground_y = self.height()
        painter.setPen(QColor(200, 200, 200))
        painter.drawLine(0, ground_y - 1, self.width(), ground_y - 1)

        if len(self.ghost_points) >= 2:
            ghost_pen = QPen(QColor(160, 160, 160, 130))
            ghost_pen.setWidth(1)
            ghost_pen.setStyle(Qt.DashLine)
            ghost_pen.setCapStyle(Qt.RoundCap)
            ghost_pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(ghost_pen)
            painter.setBrush(Qt.NoBrush)

            ghost_qpoints = [QPointF(px, py) for (px, py) in self.ghost_points]
            painter.drawPolyline(QPolygonF(ghost_qpoints))

        #trajectory
        if self.show_trajectory and len(self.path_points) >= 2:
            points = [QPointF(px, py) for (px, py) in self.path_points]

            pen = QPen(QColor(120, 120, 120, 180))
            pen.setWidth(2)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            painter.drawPolyline(QPolygonF(points))

            tail_points = points[-20:] if len(points) > 20 else points
            pen_tail = QPen(QColor(80, 160, 255, 220))
            pen_tail.setWidth(3)
            pen_tail.setCapStyle(Qt.RoundCap)
            pen_tail.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen_tail)
            painter.drawPolyline(QPolygonF(tail_points))

        #ball
        x_center = int(self.ball_x)
        y_center = int(self.ball_y)

        x = x_center - self.ball_radius
        y = y_center - self.ball_radius
        diameter = self.ball_radius*2

        painter.setBrush(QColor(80,160,255))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x,y,diameter,diameter)
