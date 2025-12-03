from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QDoubleSpinBox, QComboBox, QApplication, QCheckBox, QFrame)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
import math


from canvas import SimulationCanvas
from simulation import update_projectile


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Projectile Motion Simulator - v1')
        self.setMinimumSize(800, 600)

        # single canvas
        self.canvas = SimulationCanvas(self)

        self.initial_ball_x = self.canvas.ball_x
        self.initial_ball_y = self.canvas.ball_y
        self.earth_g_pixels = self.canvas.g

        self.is_running = False

        # === ROOT LAYOUT: canvas on top, controls below ===
        root_layout = QVBoxLayout()
        self.setLayout(root_layout)

        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(8)

        root_layout.addWidget(self.canvas, 1)


        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_layout = QVBoxLayout()
        controls_frame.setLayout(controls_layout)

        root_layout.addWidget(controls_frame, 0)

        controls_layout.setContentsMargins(10, 8, 10, 8)
        controls_layout.setSpacing(6)
        controls_frame.setMaximumHeight(260)

        # ---- Title ----
        title_label = QLabel("Projectile Simulator")
        title_label.setObjectName("titleLabel")

        subtitle_label = QLabel("Adjust settings and fire")
        subtitle_label.setObjectName("subtitleLabel")

        # ---- Parameter rows ----
        params_layout = QVBoxLayout()

        # row 1: speed + angle  (Launch parameters)
        row1 = QHBoxLayout()
        self.speed_label = QLabel('Speed:')
        self.speed_input = QDoubleSpinBox()
        self.speed_input.setRange(0.0, 1000.0)
        self.speed_input.setValue(400.0)
        self.speed_input.setSingleStep(50.0)
        self.speed_input.setSuffix(" px/s")

        self.angle_label = QLabel("Angle:")
        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(0.0, 90.0)
        self.angle_input.setValue(45.0)
        self.angle_input.setSingleStep(5.0)
        self.angle_input.setSuffix(" °")

        row1.addWidget(self.speed_label)
        row1.addWidget(self.speed_input)
        row1.addWidget(self.angle_label)
        row1.addWidget(self.angle_input)
        params_layout.addLayout(row1)

        # row 2: gravity + ball type
        row2 = QHBoxLayout()
        self.gravity_label = QLabel('Gravity:')
        self.gravity_combo = QComboBox()
        self.gravity_combo.addItem("Earth (9.81 m/s²)", 9.81)
        self.gravity_combo.addItem("Moon (1.62 m/s²)", 1.62)
        self.gravity_combo.addItem("Mars (3.71 m/s²)", 3.71)

        self.ball_type_label = QLabel("Ball type:")
        self.ball_type_combo = QComboBox()
        self.ball_type_combo.addItem("Normal")
        self.ball_type_combo.addItem("Heavy")
        self.ball_type_combo.addItem("Bouncy")

        row2.addWidget(self.gravity_label)
        row2.addWidget(self.gravity_combo)
        row2.addWidget(self.ball_type_label)
        row2.addWidget(self.ball_type_combo)
        params_layout.addLayout(row2)

        # row 3: wall restitution  (Collisions)
        row3 = QHBoxLayout()
        self.wall_restitution_label = QLabel("Wall Restitution:")
        self.wall_restitution_input = QDoubleSpinBox()
        self.wall_restitution_input.setRange(0.0, 1.0)
        self.wall_restitution_input.setSingleStep(0.05)
        self.wall_restitution_input.setValue(0.7)
        self.wall_restitution_input.setSuffix(" bounce")

        row3.addWidget(self.wall_restitution_label)
        row3.addWidget(self.wall_restitution_input)
        params_layout.addLayout(row3)

        # ---- Buttons row (centered) ----
        buttons_row = QHBoxLayout()
        self.start_button = QPushButton('Fire')
        self.start_button.setObjectName("fireButton")
        self.stop_button = QPushButton('Pause')
        self.stop_button.setObjectName("pauseButton")
        self.reset_button = QPushButton('Reset')
        self.reset_button.setObjectName("resetButton")

        buttons_row.addStretch()
        buttons_row.addWidget(self.start_button)
        buttons_row.addWidget(self.stop_button)
        buttons_row.addWidget(self.reset_button)
        buttons_row.addStretch()

        # trajectory toggle
        self.show_traj_checkbox = QCheckBox("Show trajectory")
        self.show_traj_checkbox.setChecked(True)

        self.stats_label = QLabel("Max height: –   Range: –   Time: –")
        self.stats_label.setObjectName("statsLabel")

        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setFrameShadow(QFrame.Sunken)

        line_mid = QFrame()
        line_mid.setFrameShape(QFrame.HLine)
        line_mid.setFrameShadow(QFrame.Sunken)

        # ---- Assemble controls layout ----
        controls_layout.setContentsMargins(10, 8, 10, 8)
        controls_layout.setSpacing(6)

        controls_layout.addWidget(title_label)
        controls_layout.addWidget(subtitle_label)
        controls_layout.addWidget(line_top)
        controls_layout.addLayout(params_layout)
        controls_layout.addWidget(line_mid)
        controls_layout.addLayout(buttons_row)
        controls_layout.addWidget(self.show_traj_checkbox)
        controls_layout.addWidget(self.stats_label)

        self.speed_input.setToolTip("Initial launch speed (pixels per second)")
        self.angle_input.setToolTip("Launch angle relative to the horizontal")
        self.gravity_combo.setToolTip("Select the planet / gravity")
        self.ball_type_combo.setToolTip("Choose ball mass & bounciness")
        self.wall_restitution_input.setToolTip("How much energy walls keep on bounce")


        #connections
        self.gravity_combo.currentIndexChanged.connect(self.on_gravity_changed)
        self.on_gravity_changed(self.gravity_combo.currentIndex())

        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)
        self.reset_button.clicked.connect(self.reset_simulation)

        self.show_traj_checkbox.toggled.connect(self.on_show_traj_toggled)

        self.speed_input.valueChanged.connect(lambda _: self.update_ghost_path())
        self.angle_input.valueChanged.connect(lambda _: self.update_ghost_path())

        self.ball_type_combo.currentIndexChanged.connect(self.on_ball_type_changed)
        self.on_ball_type_changed(self.ball_type_combo.currentIndex())



        # timer
        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()

        self.update_ghost_path()

        self.setStyleSheet("""
                    QWidget {
                        background-color: #20232a;
                        color: #e0e0e0;
                        font-family: Segoe UI, Arial;
                        font-size: 12px;
                    }
                    QFrame#controlsFrame {
                        background-color: #181a20;
                        border-radius: 10px;
                        padding: 8px;
                    }
                    QLabel#titleLabel {
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QLabel#subtitleLabel {
                        font-size: 11px;
                        color: #9a9fb0;
                    }
                    QDoubleSpinBox, QComboBox {
                        background-color: #2b2f3a;
                        border: 1px solid #3a3f4d;
                        border-radius: 6px;
                        padding: 2px 6px;
                    }
                    QPushButton {
                        background-color: #2b2f3a;
                        border-radius: 6px;
                        padding: 6px 10px;
                    }
                    QPushButton:hover {
                        background-color: #3a3f4d;
                    }
                    QPushButton#fireButton {
                        background-color: #ff7a3c;
                        color: #111;
                        font-weight: bold;
                    }
                    QPushButton#fireButton:hover {
                        background-color: #ff955f;
                    }
                    QPushButton#pauseButton {
                        background-color: #ffaa2b;
                        color: #111;
                    }
                    QPushButton#resetButton {
                        background-color: #e04f5f;
                        color: #f5f5f5;
                    }
                """)

    def start_simulation(self):
        c = self.canvas
        c.path_points.clear()


        speed = self.speed_input.value()
        angle_deg = self.angle_input.value()
        angle_rad = math.radians(angle_deg)

        c.vx = speed * math.cos(angle_rad)
        c.vy = -speed * math.sin(angle_rad)

        self.canvas.wall_restitution = self.wall_restitution_input.value()

        c.ghost_points.clear()

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

        self.on_ball_type_changed(self.ball_type_combo.currentIndex())

        c.update()

        self.update_ghost_path()

    def update_ghost_path(self):
        c = self.canvas

        ghost_points = []

        x = c.ball_x
        y = c.ball_y
        x0 = c.ball_x
        y0 = c.ball_y
        min_y = y0

        speed = self.speed_input.value()
        angle_deg = self.angle_input.value()
        angle_rad = math.radians(angle_deg)

        vx = speed * math.cos(angle_rad)
        vy = -speed * math.sin(angle_rad)

        g = c.g
        dt = 0.016

        width = c.width()
        height = c.height()

        max_steps = 600

        for _ in range(max_steps):
            vy += g * dt
            x += vx * dt
            y += vy * dt


            if y < min_y:
                min_y = y


            if y > height:
                break


            if x < 0 or x > width:
                break

            ghost_points.append((x, y))

        c.ghost_points = ghost_points

        if hasattr(self, "stats_label"):
            if ghost_points:
                last_x, last_y = ghost_points[-1]
                flight_time = len(ghost_points) * dt
                max_height = max(0.0, y0 - min_y)
                range_px = abs(last_x - x0)

                self.stats_label.setText(
                    f"Max height: {max_height:.1f} px   "
                    f"Range: {range_px:.1f} px   "
                    f"Time: {flight_time:.2f} s"
                )
            else:
                self.stats_label.setText("Max height: –   Range: –   Time: –")

        c.update()

    def on_gravity_changed(self, index):
        real_g = self.gravity_combo.itemData(index)

        earth_real_g = 9.81
        scale = self.earth_g_pixels / earth_real_g

        self.canvas.g = real_g * scale

        self.update_ghost_path()

    def update_simulation(self):
        if not self.is_running:
            return

        still_running = update_projectile(self)
        if not still_running:
            self.is_running = False

            self.update_ghost_path()

        self.canvas.update()

    def on_show_traj_toggled(self, checked):
        self.canvas.show_trajectory = checked
        self.canvas.update()

    def on_ball_type_changed(self, index):
        c = self.canvas
        ball_type = self.ball_type_combo.currentText()

        if ball_type == "Normal":
            c.ball_radius = 20
            c.floor_restitution = 0.7
            c.floor_friction = 0.98
            c.ball_color = QColor(80, 160, 255)
            c.wall_restitution = self.wall_restitution_input.value()

        elif ball_type == "Heavy":
            c.ball_radius = 24
            c.floor_restitution = 0.45
            c.floor_friction = 0.90
            c.ball_color = QColor(50, 80, 140)
            c.wall_restitution = self.wall_restitution_input.value() * 0.8

        elif ball_type == "Bouncy":
            c.ball_radius = 16
            c.floor_restitution = 0.9
            c.floor_friction = 0.995
            c.ball_color = QColor(255, 140, 0)
            c.wall_restitution = min(1.0, self.wall_restitution_input.value() * 1.2)

        self.update_ghost_path()
        c.update()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())



