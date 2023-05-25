import os
import sys
scriptpath =r"D:\pierr\Documents\GitHub\Logiciel_de_traitement_de_donnees_PEA"
sys.path.append(os.path.abspath(scriptpath))
from get_data_to_plot import GetDataToPlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QButtonGroup
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Initialize the plot variables
        self.data_type = "0"
        self.folder_path= "C:\\Users\\pierr\\Desktop\\PEA\\230516K1\\results"
        self.x_axis_type = "position"
        self.sample_thickness = 127.8
        self.sound_velocity = 2200
        self.sampling = 1.25
        self.nb_frames = 984
        self.x_left_lim = 144
        self.x_right_lim=257
        self.x_peak1=164
        self.x_peak2=237
        self.x_max_CD = 38.817

        self.setWindowTitle("PEA Animation Creator")
        self.setGeometry(200, 200, 1400, 400)

        #Main widget 
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Create the matplotlib figure and canvas in center of the window
        animation_widget = QWidget()
        animation_layout = QVBoxLayout()
        animation_widget.setLayout(animation_layout)
        self.fig = plt.figure(figsize=(8, 6))
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
        self.data = None

        
        #Left column widget
        user_input_widget = QWidget()
        user_input_layout = QVBoxLayout()
        user_input_widget.setLayout(user_input_layout)
        
        
        ##Create buttons
        self.folder_button = QPushButton("Select folder", self)
        self.folder_button.setGeometry(50, 50, 200, 100)
        self.folder_button.clicked.connect(self.select_folder)
        
        #Buttons for y-axis
        self.y_axis_group_button = QButtonGroup()
        
        self.CD_button = QPushButton("Charge density", self)
        self.CD_button.setCheckable(True)
        self.y_axis_group_button.addButton(self.CD_button)
        self.CD_button.clicked.connect(self.y_axis_buttonClicked)
        
        self.EF_button = QPushButton("Electric Field", self)
        self.EF_button.setCheckable(True)
        self.y_axis_group_button.addButton(self.EF_button)
        self.EF_button.clicked.connect(self.y_axis_buttonClicked)
        
        self.points_button = QPushButton("Points", self)
        self.points_button.clicked.connect(lambda: setattr(self, 'x_axis_type', 'points'))
        self.time_button = QPushButton("Time", self)
        self.time_button.clicked.connect(lambda: setattr(self, 'x_axis_type', 'time'))
        self.position_button = QPushButton("Position", self)
        self.position_button.clicked.connect(lambda: setattr(self, 'x_axis_type', 'position'))
        
        # Create labels
        folder_path_label = QLabel("Results Folder (where CD, EF folders are):",self)
        data_type_label = QLabel("Data Type:", self)
        x_axis_type_label = QLabel("X-Axis Type:", self)
        sample_thickness_label = QLabel("Sample Thickness (µm):", self)
        sound_velocity_label = QLabel("Sound Velocity (m/s):", self)
        sampling_label = QLabel("Sampling (GHz):", self)
        x_left_lim_label = QLabel("X-axis Left Limit (points):", self)
        x_right_lim_label = QLabel("X-axis Right Limit (points):", self)
        y_lim_min_label = QLabel("Y-axis Min Limit (points)", self)
        y_lim_max_label = QLabel("Y-axis Max Limit (points)", self)
        x_peak1_label = QLabel("Left electrode (points):", self)
        x_peak2_label = QLabel("Right electrode (points):", self)
        x_max_CD_label = QLabel("Penetration Depth (µm):", self)
        
        

        # Create input fields             
        self.sample_thickness_input = QLineEdit(self)
        self.sound_velocity_input = QLineEdit(self)
        self.sampling_input = QLineEdit(self)
        self.x_left_lim_input = QLineEdit(self)
        self.x_right_lim_input = QLineEdit(self)
        self.x_peak1_input = QLineEdit(self)
        self.x_peak2_input = QLineEdit(self)
        self.x_max_CD_input = QLineEdit(self)
        self.y_lim_min_input = QLineEdit(self)
        self.y_lim_max_input = QLineEdit(self)
        
        #Add labels and inputs to column widget
        user_input_layout.addWidget(folder_path_label)
        user_input_layout.addWidget(self.folder_button)
        user_input_layout.addWidget(data_type_label)
        user_input_layout.addWidget(self.CD_button)
        user_input_layout.addWidget(self.EF_button)
        user_input_layout.addWidget(x_axis_type_label)
        user_input_layout.addWidget(self.points_button)
        user_input_layout.addWidget(self.time_button)
        user_input_layout.addWidget(self.position_button)
        user_input_layout.addWidget(sample_thickness_label)
        user_input_layout.addWidget(self.sample_thickness_input)
        user_input_layout.addWidget(sound_velocity_label)
        user_input_layout.addWidget(self.sound_velocity_input)
        user_input_layout.addWidget(sampling_label)
        user_input_layout.addWidget(self.sampling_input)
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
    
    def y_axis_buttonClicked(self):
        sender = self.sender()

        if sender == self.CD_button:
            setattr(self, 'data_type', 'CD')
            self.CD_button.setChecked(True)
            self.EF_button.setChecked(False)
            
        elif sender == self.EF_button:
            setattr(self, 'data_type', 'EF')
            self.EF_button.setChecked(True)
            self.CD_button.setChecked(False)
            
    
    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", os.getcwd())
        if self.folder_path:
            os.chdir(self.folder_path)
            
        
    def process_inputs(self):
        
        if self.CD_button or self.EF_button or self.points_button or self.time_button or self.position_button\
            or self.folder_path or self.sample_thickness_input.text()!='' or self.sound_velocity_input.text()!=''\
                or self.sampling_input.text()!='' or self.x_left_lim_input.text()!='' or self.x_right_lim_input.text()!=''\
                    or self.x_peak1_input.text()!='' or self.x_peak2_input.text()!='' or self.x_max_CD_input.text()!='' or self.y_lim_min_input.text()!='' or self.y_lim_max_input.text()!='':
            
            self.sample_thickness= float(self.sample_thickness_input.text())
            self.sound_velocity = float(self.sound_velocity_input.text())
            self.sampling = float(self.sampling_input.text()) 
            self.x_left_lim= int(self.x_left_lim_input.text())
            self.x_right_lim = int(self.x_right_lim_input.text())
            self.x_peak1 = int(self.x_peak1_input.text())
            self.x_peak2 = int(self.x_peak2_input.text())
            self.x_max_CD = float(self.x_max_CD_input.text())
            self.y_lim_min = float(self.y_lim_min_input.text())
            self.y_lim_max = float(self.y_lim_max_input.text())
            
            self.no_inputs = False
        else: 
            self.no_inputs = True
        
        
    def create_animation(self):
        self.process_inputs()
        if self.no_inputs == False: 
            self.data = GetDataToPlot(data_type = self.data_type,\
                results_folder= self.folder_path,\
                    x_axis_type = self.x_axis_type,\
                        sample_thickness =self.sample_thickness,\
                            sound_velocity = self.sound_velocity,\
                                sampling = self.sampling,\
                                        x_left_lim = self.x_left_lim,\
                                            x_right_lim=self.x_right_lim,\
                                                x_peak1=self.x_peak1,\
                                                    x_peak2=self.x_peak2,\
                                                        x_max_CD = self.x_max_CD,\
                                                            ylim_min = self.y_lim_min,\
                                                                ylim_max = self.y_lim_max)
        else: 
                       
            self.data = GetDataToPlot()
        
        self.start_animation()
        
        
    def init_ani(self):
        #Set up the axis labels and grid
        
        #Set up the y axis
        if self.y_lim_min_input.text()!='' or self.y_lim_max_input.text()!='':
            self.ax.set_ylim(self.y_lim_min, self.y_lim_max)
        else:
             #Keep the plots between the max y value and the min y value of all frames
            ymin = []
            ymax = []
            for i in range(len(self.data.y)):
                ymin.append(np.min(self.data.y[i]))
                ymax.append(np.max(self.data.y[i]))
            
            yminmin = np.min(ymin) if len(ymin) > 0 else -200
            ymaxmax = np.max(ymax) if len(ymin) > 0 else 200
            #max value + 10%, min_value-10%
            
            if 1000>ymaxmax >=0:
                if yminmin>=0 : self.ax.set_ylim(yminmin-yminmin/10, ymaxmax+ymaxmax/10)                 
                else : self.ax.set_ylim(yminmin+yminmin/10, ymaxmax+ymaxmax/10) 
                
            elif ymaxmax<0: 
                if yminmin>=0 : self.ax.set_ylim(yminmin-yminmin/10, ymaxmax-ymaxmax/10) 
                else : self.ax.set_ylim(yminmin+yminmin/10, ymaxmax-ymaxmax/10) 
    
            else: 
                self.ax.set_ylim(-2000, 2000) 
        
        
        self.time_width = self.sample_thickness/self.sound_velocity*10**3
        #We force the x values to respect the distance between first peak and second peak

        
        # X axis limit given values are in points
        # We take the values given by the user and change them in order to place the 1st peak at x=0
        x_real_left_lim = self.x_left_lim - self.x_peak1
        x_real_right_lim = self.x_right_lim - self.x_peak1
                
        # Add vertical lines for peaks (in points)
        x1 = 0  #peak 1 - cathode
        x2 = self.x_peak2 - self.x_peak1 #peak 2 - anode
        
        # Add a vertical line for the penetration depth (in points)
        x3 = x2 - self.x_max_CD*self.sampling*self.time_width//self.sample_thickness

        if self.x_axis_type in {"points","Points","point","Point","POINT","POINTS","p","P"}:
            self.ax.set_xlim(x_real_left_lim,x_real_right_lim)
            self.x_axis_plot = "Points"
            # Add gray backgrounds on the left and right of x1 and x2
            self.ax.axvspan(x_real_left_lim, x1, alpha=0.1, color='gray')
            self.ax.axvspan(x2,x_real_right_lim, alpha=0.1, color='gray')
            
        elif self.x_axis_type in {"time", "Time","TIME","times","Times","TIMES","t","T"}:
            self.ax.set_xlim(x_real_left_lim/self.sampling, x_real_right_lim/self.sampling)
            self.x_axis_plot = "Time (ns)"
            x1 = x1/self.sampling
            x2 = x2/self.sampling
            x3 = x3/self.sampling
            # Add gray backgrounds on the left and right of x1 and x2
            self.ax.axvspan(x_real_left_lim/self.sampling, x1, alpha=0.1, color='gray')
            self.ax.axvspan(x2,x_real_right_lim/self.sampling, alpha=0.1, color='gray')
        else :
            self.ax.set_xlim(x_real_left_lim/self.sampling/self.time_width*self.sample_thickness,x_real_right_lim/self.sampling/self.time_width*self.sample_thickness)
            self.x_axis_plot = "Position(μm)"
            x1 = x1/self.sampling/self.time_width*self.sample_thickness
            x2 = x2/self.sampling/self.time_width*self.sample_thickness
            x3 = x2 - self.x_max_CD
            # Add gray backgrounds on the left and right of x1 and x2
            self.ax.axvspan(x_real_left_lim/self.sampling/self.time_width*self.sample_thickness, x1, alpha=0.1, color='gray')
            self.ax.axvspan(x2,x_real_right_lim/self.sampling/self.time_width*self.sample_thickness, alpha=0.1, color='gray')
                  
        self.ax.axvline(x=x1, color='red', linestyle='--', label = "Cathode")
        self.ax.axvline(x=x2, color='green', linestyle='--', label = "Anode")
        self.ax.axvline(x=x3, color = 'black', linestyle='--', label = "Penetration depth")
        self.line, = self.ax.plot(self.data.x, self.data.y[0], color='black')
        

        return self.line,
                 
    
    def start_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, frames=len(self.data.y), init_func=self.init_ani, interval=20, blit=True, repeat=True)
        

    def update_plot(self, frame):
        
        self.frame = frame
        self.line.set_ydata(self.data.y[frame])
        #self.line, = self.ax.plot(self.data.x, self.data.y[frame], 'b-')
      
        # Calculate time in minutes and seconds
        time_sec = frame * 5
        minutes, seconds = divmod(time_sec, 60)

        # Change title color and label based on time
        if 0 <= minutes < 2 or 22 <= minutes < 52:
            title_color = 'blue'
        elif 2 <= minutes < 22:
            title_color = 'red'
        else:
            title_color = 'black'
        DC_status = "DC applied" if 0 <= minutes < 52 else "No DC applied"
        irradiating_status = "Shutter open: irradiation" if 2 <= minutes < 22 else "Shutter closed: no irradiation"
        self.ax.set_title(f'{DC_status} - {irradiating_status} - {self.data.data_type_name} - Time: {minutes:02d}:{seconds:02d}', color=title_color)
        self.ax.set_xlabel(self.x_axis_plot)
        self.ax.set_ylabel(self.data.data_type_name)
        self.ax.grid(True)

        self.canvas.draw()
        return self.line,

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
        writer = animation.PillowWriter(fps=15)
        os.chdir(self.folder_path)
        self.ani.save(f"{self.data_type}_gif.gif", writer=writer)

    def save_frame(self):
        os.chdir(self.folder_path)
        self.fig.savefig(f"{self.data_type}_frame{self.frame}.png")

    def save_animation_mp4(self):
        os.chdir(self.folder_path)
        self.ani.save(f"{self.data_type}_animation.mp4", writer="ffmpeg")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
