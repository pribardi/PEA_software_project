import os
import sys
scriptpath =r"D:\pierr\Documents\GitHub\Logiciel_de_traitement_de_donnees_PEA"
sys.path.append(os.path.abspath(scriptpath))
from main import Datatoplotgif
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PEA Animation Creator")
        self.setGeometry(200, 200, 1400, 400)

        self.data = []
        
        #Main widget 
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Create the matplotlib figure and canvas in center of the window
        animation_widget = QWidget()
        animation_layout = QVBoxLayout()
        animation_widget.setLayout(animation_layout)
        self.fig = plt.figure(figsize=(12, 4))
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMinimumSize(400,300)
        self.canvas.setMaximumSize(1200,900)
        animation_layout.addWidget(self.canvas)

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

        # Create the layout for buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.play_pause_button)
        buttons_layout.addWidget(self.save_animation_button)
        buttons_layout.addWidget(self.save_frame_button)
        buttons_layout.addWidget(self.save_animation_mp4_button)
        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(buttons_layout)


        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ani = None
        
        #Left column widget
        user_input_widget = QWidget()
        user_input_layout = QVBoxLayout()
        user_input_widget.setLayout(user_input_layout)
        
        # Create labels
        input_label = QLabel("Fill in the information: ", self)
        data_type_label = QLabel("Data Type:", self)
        results_folder_label = QLabel("Results Folder:", self)
        x_axis_type_label = QLabel("X-Axis Type:", self)
        sample_thickness_label = QLabel("Sample Thickness (µm):", self)
        sound_velocity_label = QLabel("Sound Velocity (m/s):", self)
        sampling_label = QLabel("Sampling (GHz):", self)
        nb_frames_label = QLabel("Number of Frames:", self)
        x_left_lim_label = QLabel("X Left Limit:", self)
        x_right_lim_label = QLabel("X Right Limit:", self)
        x_peak1_label = QLabel("X Peak 1:", self)
        x_peak2_label = QLabel("X Peak 2:", self)
        x_max_CD_label = QLabel("X Max CD (µm):", self)
        y_lim_min_label = QLabel("Y-axis limit (ymin, ymax)", self)
        y_lim_max_label = QLabel("Y-axis limit (ymin, ymax)", self)
        

        # Create input fields             
        self.data_type_input = QLineEdit(self)
        self.results_folder_input = QLineEdit(self)
        self.x_axis_type_input = QLineEdit(self)
        self.sample_thickness_input = QLineEdit(self)
        self.sound_velocity_input = QLineEdit(self)
        self.sampling_input = QLineEdit(self)
        self.nb_frames_input = QLineEdit(self)
        self.x_left_lim_input = QLineEdit(self)
        self.x_right_lim_input = QLineEdit(self)
        self.x_peak1_input = QLineEdit(self)
        self.x_peak2_input = QLineEdit(self)
        self.x_max_CD_input = QLineEdit(self)
        self.y_lim_min_input = QLineEdit(self)
        self.y_lim_max_input = QLineEdit(self)
        
        #Add labels and inputs to column widget
        user_input_layout.addWidget(input_label)
        
        user_input_layout.addWidget(data_type_label)
        user_input_layout.addWidget(self.data_type_input)
        user_input_layout.addWidget(results_folder_label)
        user_input_layout.addWidget(self.results_folder_input)
        user_input_layout.addWidget(x_axis_type_label)
        user_input_layout.addWidget(self.x_axis_type_input)
        user_input_layout.addWidget(sample_thickness_label)
        user_input_layout.addWidget(self.sample_thickness_input)
        user_input_layout.addWidget(sound_velocity_label)
        user_input_layout.addWidget(self.sound_velocity_input)
        user_input_layout.addWidget(sampling_label)
        user_input_layout.addWidget(self.sampling_input)
        user_input_layout.addWidget(nb_frames_label)
        user_input_layout.addWidget(self.nb_frames_input)
        user_input_layout.addWidget(x_left_lim_label)
        user_input_layout.addWidget(self.x_left_lim_input)
        user_input_layout.addWidget(x_right_lim_label)
        user_input_layout.addWidget(self.x_right_lim_input)
        user_input_layout.addWidget(x_peak1_label)
        user_input_layout.addWidget(self.x_peak1_input)
        user_input_layout.addWidget(x_peak2_label)
        user_input_layout.addWidget(self.x_peak2_input)
        user_input_layout.addWidget(x_max_CD_label)
        user_input_layout.addWidget(self.x_max_CD_input)
        user_input_layout.addWidget(y_lim_min_label)
        user_input_layout.addWidget(self.y_lim_min_input)
        user_input_layout.addWidget(y_lim_max_label)
        user_input_layout.addWidget(self.y_lim_max_input)
        
        generate_animation = QPushButton("Generate !", self)
        generate_animation.clicked.connect(self.create_animation)
        user_input_layout.addWidget(generate_animation)
        
        #Add everything to main layout
        main_layout.addWidget(user_input_widget)
        main_layout.addWidget(animation_widget)
        main_layout.addWidget(self.bottom_widget)
        
        
    def create_animation(self):
        plot = Datatoplotgif(data_type = str(self.data_type_input.text()),\
            results_folder= str(self.results_folder_input.text()),\
                x_axis_type = str(self.x_axis_type_input.text()),\
                    sample_thickness = float(self.sample_thickness_input.text()),\
                        sound_velocity = float(self.sound_velocity_input.text()),\
                            sampling = float(self.sampling_input.text()),\
                                nb_frames = int(self.nb_frames_input.text()),\
                                    x_left_lim = int(self.x_left_lim_input.text()),\
                                        x_right_lim=int(self.x_left_lim_input.text()),\
                                            x_peak1=int(self.x_peak1_input.text()),\
                                                x_peak2=int(self.x_peak2_input.text()),\
                                                    x_max_CD = float(self.x_max_CD_input.text()),\
                                                        ylim_min = float(self.y_lim_min_input.text()),\
                                                            ylim_max = float(self.y_lim_max_input.text()))
        
        self.fig, self.ax = plot.fig, plot.ax
        self.ani = plot.ani


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
