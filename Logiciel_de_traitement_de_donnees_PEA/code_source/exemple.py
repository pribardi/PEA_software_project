import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Datatoplotgif:
    def __init__(self):
        self.x = np.linspace(0, 10, 100)
        self.y = np.sin(self.x)

    def update_data(self):
        self.y += 0.1 * np.random.randn(len(self.x))

    def get_data(self):
        return self.x, self.y


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animation Demo")
        self.setGeometry(200, 200, 800, 600)

        self.data = Datatoplotgif()

        # Create the matplotlib figure and canvas
        self.fig = plt.figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)

        # Create the play/pause button
        self.play_pause_button = QPushButton("Play", self)
        self.play_pause_button.clicked.connect(self.on_play_pause_button_click)

        # Create the save buttons
        self.save_animation_button = QPushButton("Save Animation (GIF)", self)
        self.save_animation_button.clicked.connect(self.save_animation)

        self.save_frame_button = QPushButton("Save Frame (PNG)", self)
        self.save_frame_button.clicked.connect(self.save_frame)

        self.save_animation_mp4_button = QPushButton("Save Animation (MP4)", self)
        self.save_animation_mp4_button.clicked.connect(self.save_animation_mp4)

        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.play_pause_button)
        layout.addWidget(self.save_animation_button)
        layout.addWidget(self.save_frame_button)
        layout.addWidget(self.save_animation_mp4_button)

        # Create a central widget to hold the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ani = None

    def start_animation(self):
        self.ani = FuncAnimation(
            self.fig,
            self.update_plot,
            frames=100,
            interval=100,
            repeat=True
        )

    def update_plot(self, frame):
        self.data.update_data()
        x, y = self.data.get_data()

        self.ax.clear()
        self.ax.plot(x, y, 'b-')
        self.ax.set_xlim([0, 10])
        self.ax.set_ylim([-3, 3])
        self.ax.set_title("Animation Demo")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)

        self.canvas.draw()

    def on_play_pause_button_click(self):
        if self.ani is None:
            self.play_pause_button.setText("Pause")
            self.start_animation()
        else:
            if self.ani.event_source is None:
                self.play_pause_button.setText("Pause")
                self.ani.event_source = self.canvas.new_timer(0)
                self.ani.event_source.add_callback(self.ani._step)
                self.ani.event_source.start()
            else:
                self.play_pause_button.setText("Play")
                self.ani.event_source.stop()
                self.ani.event_source = None

    def save_animation(self):
        self.ani.save("animation.gif", writer="pillow")

    def save_frame(self):
        self.fig.savefig("frame.png")

    def save_animation_mp4(self):
        self.ani.save("animation.mp4", writer="ffmpeg")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

