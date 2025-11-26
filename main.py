from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QDoubleSpinBox, QComboBox, QApplication, QCheckBox)
from PyQt5.QtCore import QTimer
import math

from canvas import SimulationCanvas
from simulation import update_projectile


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Projectile Motion Simulator - v1')
        self.setMinimumSize(800, 600)

        self.canvas = SimulationCanvas(self)

        self.initial_ball_x = self.canvas.ball_x
        self.initial_ball_y = self.canvas.ball_y

        self.earth_g_pixels = self.canvas.g

        self.is_running = False

        # main layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # parameter row
        params_layout = QHBoxLayout()

        self.speed_label = QLabel('Speed:')
        self.speed_input = QDoubleSpinBox()
        self.speed_input.setRange(0.0, 1000.0)
        self.speed_input.setValue(400.0)
        self.speed_input.setSingleStep(50.0)
        self.speed_input.setSuffix(" px/s")

        self.angle_label = QLabel("Angle:")
        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(0.0, 90.0)  # degrees
        self.angle_input.setValue(45.0)       # default angle
        self.angle_input.setSingleStep(5.0)
        self.angle_input.setSuffix(" °")

        self.gravity_label = QLabel('Gravity:')
        self.gravity_combo = QComboBox()

        self.gravity_combo.addItem("Earth (9.81 m/s²)", 9.81)
        self.gravity_combo.addItem("Moon (1.62 m/s²)", 1.62)
        self.gravity_combo.addItem("Mars (3.71 m/s²)", 3.71)

        self.wall_restitution_label = QLabel("Wall Restitution:")
        self.wall_restitution_input = QDoubleSpinBox()
        self.wall_restitution_input.setRange(0.0, 1.0)
        self.wall_restitution_input.setSingleStep(0.05)
        self.wall_restitution_input.setValue(0.7)
        self.wall_restitution_input.setSuffix(" bounce")

        params_layout.addWidget(self.speed_label)
        params_layout.addWidget(self.speed_input)
        params_layout.addWidget(self.angle_label)
        params_layout.addWidget(self.angle_input)
        params_layout.addWidget(self.gravity_label)
        params_layout.addWidget(self.gravity_combo)

        params_layout.addWidget(self.wall_restitution_label)
        params_layout.addWidget(self.wall_restitution_input)

        layout.addLayout(params_layout)

        # controls layout
        controls_layout = QHBoxLayout()

        self.start_button = QPushButton('Fire')
        self.stop_button = QPushButton('Pause')
        self.reset_button = QPushButton('Reset')

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.reset_button)

        self.show_traj_checkbox = QCheckBox("Show trajectory")
        self.show_traj_checkbox.setChecked(True)
        controls_layout.addWidget(self.show_traj_checkbox)

        layout.addLayout(controls_layout)
        self.setLayout(layout)

        #connections
        self.gravity_combo.currentIndexChanged.connect(self.on_gravity_changed)
        self.on_gravity_changed(self.gravity_combo.currentIndex())

        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)
        self.reset_button.clicked.connect(self.reset_simulation)

        self.show_traj_checkbox.toggled.connect(self.on_show_traj_toggled)

        # timer
        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()

    def start_simulation(self):
        c = self.canvas
        c.path_points.clear()

        c.ball_x = self.initial_ball_x
        c.ball_y = self.initial_ball_y

        c.path_points.clear()

        speed = self.speed_input.value()
        angle_deg = self.angle_input.value()
        angle_rad = math.radians(angle_deg)

        c.vx = speed * math.cos(angle_rad)
        c.vy = -speed * math.sin(angle_rad)

        self.canvas.wall_restitution = self.wall_restitution_input.value()

        self.is_running = True
        c.update()

    def stop_simulation(self):
        self.is_running = False  # stop button functionality

    def reset_simulation(self):
        c = self.canvas
        c.ball_x = self.initial_ball_x
        c.ball_y = self.initial_ball_y

        c.vx = 0.0
        c.vy = 0.0

        c.path_points.clear()

        self.is_running = False
        c.update()

    def on_gravity_changed(self, index):
        real_g = self.gravity_combo.itemData(index)

        earth_real_g = 9.81
        scale = self.earth_g_pixels / earth_real_g

        self.canvas.g = real_g * scale

    def update_simulation(self):
        if not self.is_running:
            return

        still_running = update_projectile(self)
        if not still_running:
            self.is_running = False

        self.canvas.update()

    def on_show_traj_toggled(self, checked):
        self.canvas.show_trajectory = checked
        self.canvas.update()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



