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

        self.dragging = False
        self.hovering_ball = False

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
        # ball + hover glow
        x_center = int(self.ball_x)
        y_center = int(self.ball_y)

        x = x_center - self.ball_radius
        y = y_center - self.ball_radius
        diameter = self.ball_radius * 2

        if self.hovering_ball or self.dragging:
            glow_radius = self.ball_radius + 10
            gx = x_center - glow_radius
            gy = y_center - glow_radius
            gdiam = glow_radius * 2

            painter.setBrush(QColor(80, 160, 255, 80))  # transparent glow
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(gx, gy, gdiam, gdiam)

        # actual ball
        painter.setBrush(QColor(80, 160, 255))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x, y, diameter, diameter)




    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            dx = event.x() - self.ball_x
            dy = event.y() - self.ball_y
            if dx * dx + dy * dy <= self.ball_radius ** 2:
                self.dragging = True
                self.drag_offset_x = dx
                self.drag_offset_y = dy
                self.path_points.clear()
                if hasattr(self, "ghost_points"):
                    self.ghost_points.clear()
                self.update()


    def mouseMoveEvent(self, event):
        mx = event.x()
        my = event.y()

        dx = mx - self.ball_x
        dy = my - self.ball_y
        inside_ball = dx * dx + dy * dy <= self.ball_radius ** 2

        # update hover state
        self.hovering_ball = inside_ball and not self.dragging

        # If dragging, move the ball
        if self.dragging:
            new_x = mx - self.drag_offset_x
            new_y = my - self.drag_offset_y

            r = self.ball_radius
            w = self.width()
            h = self.height()

            new_x = max(r, min(new_x, w - r))
            new_y = max(r, min(new_y, h - r))

            self.ball_x = new_x
            self.ball_y = new_y

        self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False

            parent = self.parent()
            if parent is not None and hasattr(parent, "update_ghost_path"):
                parent.update_ghost_path()
            self.update()

    def leaveEvent(self, event):
        self.hovering_ball = False
        self.update()
        super().leaveEvent(event)



