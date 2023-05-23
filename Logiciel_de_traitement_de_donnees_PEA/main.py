import subprocess
import sys
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.animation import FFMpegWriter
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ipywidgets as widgets
from IPython.display import display


class Datatoplotgif:
    """Allow to load and plot the data choosed from {CD, EF}
    This creates an animation that can be saved as a .gif file"""
    def __init__(self, data_type, results_folder, x_axis_type, sample_thickness, sound_velocity, sampling, nb_frames, x_left_lim,x_right_lim, x_peak1, x_peak2, x_max_CD):
        """
        data_type: 'CD' or 'EF' 
        results_folder: path to results folder (not CD or EF but the results folder)
        x_axis_type: 'points' or 'time' or 'position'
        sample_thickness: in micrometer
        sound_velocity: in m/s
        sampling: in GHz = Gpoints/sec
        nb_frames: number of frames in the data
        (x_left_lim,x_right_lim): x axis limits (read from labView given limits)
        (x_peak1, x_peak2): x coordinate of left peak and right peak
        x_max_CD: x coordinate where charge density is the highest (in micrometer !!)
        """
        self.data_type = data_type
        self.res_folder = results_folder
        self.iteration = [str(a).zfill(3) for a in range(nb_frames)]
        self.x_left_lim = x_left_lim
        self.x_right_lim = x_right_lim
        self.x_peak1 = x_peak1
        self.x_peak2 = x_peak2
        self.x_max_CD = x_max_CD
        self.load_data(self.data_type)
        self.sample_thick = sample_thickness #display in micrometer
        self.sound_velocity = sound_velocity
        self.calculate_sample_time_width()
        self.sampling = sampling #display in ns
        self.x_axis_type = x_axis_type
        self.paused = False
        self.current_frame = 0
        self.fig, self.ax = plt.subplots(figsize = (8,6))
        self.load_x_axis()
        self.data_type_name()
        self.display_widgets()
        self.init_ani()
        self.ani = animation.FuncAnimation(self.fig, self.animate, frames=len(self.data), init_func=self.init_ani, interval=20, blit=True)
        plt.show()
        

    def calculate_sample_time_width(self):
        self.time_width = self.sample_thick/self.sound_velocity*10**3
        #We force the x values to respect the distance between first peak and second peak

    def load_data(self, data_type):
        if data_type == "CD":
            os.chdir(self.res_folder + "\\CD")
            
        elif data_type =="EF":
            os.chdir(self.res_folder + "\\EF")
        
        elif data_type =="EP":
            os.chdir(self.res_folder + "\\EP")
        
        self.data = np.array([np.loadtxt(data_type + self.iteration[i] + '.dat') for i in range(len(self.iteration))])

    def load_x_axis(self):
        self.points =[e for e in range(-self.x_peak1,len(self.data[0])-self.x_peak1,1)]
        if self.x_axis_type == "points":
            self.x_axis = self.points
            self.line, = self.ax.plot(self.points, self.data[0])
        elif self.x_axis_type == "time" :
            self.time = list(map(lambda x: x/self.sampling), self.points)
            self.x_axis = self.time
            self.line, = self.ax.plot(self.time, self.data[0])
        else:
            #default
            self.position = list(map(lambda x: x/self.sampling/self.time_width*self.sample_thick, self.points ))
            self.x_axis = self.position
            self.line, = self.ax.plot(self.position, self.data[0])

    def data_type_name(self):
        if self.data_type == "CD":
            return "Charge Density(C/m3)"
        elif self.data_type == "EF":
            return "Electric Field (kV/mm)"
        elif self.data_type == "EP":
            return "Electric Potential"
        else :
            return ""
            
    def init_ani(self):
        # Set up the axis labels and grid
        
        #Keep the plots between the max y value and the min y value of all frames
        ymin = []
        ymax = []
        for i in range(len(self.data)):
            ymin.append(np.min(self.data[i]))
            ymax.append(np.max(self.data[i]))
        yminmin = np.min(ymin)
        ymaxmax = np.max(ymax)
        #max value + 10%, min_value-10%
        if 1000>ymaxmax >=0:
            if yminmin>=0 : self.ax.set_ylim(yminmin-yminmin/10, ymaxmax+ymaxmax/10)                 
            else : self.ax.set_ylim(yminmin+yminmin/10, ymaxmax+ymaxmax/10) 
            
        elif ymaxmax<0: 
            if yminmin>=0 : self.ax.set_ylim(yminmin-yminmin/10, ymaxmax-ymaxmax/10) 
            else : self.ax.set_ylim(yminmin+yminmin/10, ymaxmax-ymaxmax/10) 
            
        else: 
            self.ax.set_ylim(-2000, 2000) 
        
        #temporary just for space charges
        #self.ax.set_ylim(-200, 200) 
        """#temporary just for EF"""
        #self.ax.set_ylim(-125, 125) 
        
        
        # X axis limit values in points
        # We take the values given by the user and change them in order to place the 1st peak at x=0
       
        x_real_left_lim = self.x_left_lim - self.x_peak1
        x_real_right_lim = self.x_right_lim - self.x_peak1
        
        
        # Add vertical lines for peaks (in points)
        x1 = 0  #peak 1 - cathode
        x2 = self.x_peak2 - self.x_peak1 #peak 2 - anode
        
        # Add a vertical line for x coordinate where there is max charge density (in points)
        x3 = x2 - self.x_max_CD*self.sampling*self.time_width//self.sample_thick

        if self.x_axis_type == "points":
            self.ax.set_xlim(x_real_left_lim,x_real_right_lim)
            self.x_axis_plot = "Points"
            # Add gray backgrounds on the left and right of x1 and x2
            self.ax.axvspan(x_real_left_lim, x1, alpha=0.1, color='gray')
            self.ax.axvspan(x2,x_real_right_lim, alpha=0.1, color='gray')
            
        elif self.x_axis_type == "time":
            self.ax.set_xlim(x_real_left_lim/self.sampling, x_real_right_lim/self.sampling)
            self.x_axis_plot = "Time (ns)"
            x1 = x1/self.sampling
            x2 = x2/self.sampling
            x3 = x3/self.sampling
            # Add gray backgrounds on the left and right of x1 and x2
            self.ax.axvspan(x_real_left_lim/self.sampling, x1, alpha=0.1, color='gray')
            self.ax.axvspan(x2,x_real_right_lim/self.sampling, alpha=0.1, color='gray')
        else :
            self.ax.set_xlim(x_real_left_lim/self.sampling/self.time_width*self.sample_thick,x_real_right_lim/self.sampling/self.time_width*self.sample_thick)
            self.x_axis_plot = "Position(μm)"
            x1 = x1/self.sampling/self.time_width*self.sample_thick
            x2 = x2/self.sampling/self.time_width*self.sample_thick
            x3 = x2 - self.x_max_CD
            
            # Add gray backgrounds on the left and right of x1 and x2
            self.ax.axvspan(x_real_left_lim/self.sampling/self.time_width*self.sample_thick, x1, alpha=0.1, color='gray')
            self.ax.axvspan(x2,x_real_right_lim/self.sampling/self.time_width*self.sample_thick, alpha=0.1, color='gray')
            

          
        self.ax.axvline(x=x1, color='red', linestyle='--', label = "cathode")
        self.ax.axvline(x=x2, color='green', linestyle='--', label = "anode")
        self.ax.axvline(x=x3, color = 'black', linestyle='--', label = "penetration depth")
        

        plt.grid(True)
      
                 
        line, = self.ax.plot([],[])
        return line,

        
        

    def animate(self, frame_num):
        self.line.set_ydata(self.data[frame_num])  # Update the line data

        # Calculate time in minutes and seconds
        time_sec = frame_num * 5
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
        self.ax.set_title(f'{DC_status} - {irradiating_status} - {self.data_type_name()} - Time: {minutes:02d}:{seconds:02d}', color=title_color)
        self.ax.set_xlabel(self.x_axis_plot)
        self.ax.set_ylabel(self.data_type_name())
        return self.line,

    def display_widgets(self):
        # Create the buttons and scrollbar
        play_pause_button = widgets.Button(description='Pause')
        play_pause_button.on_click(self.on_play_pause_button_click)

        save_gif_button = widgets.Button(description='Save as GIF')
        save_gif_button.on_click(self.save_animation)

        save_frame_button = widgets.Button(description='Save Frame')
        save_frame_button.on_click(self.save_frame)

        save_mp4_button = widgets.Button(description='Save as MP4')
        save_mp4_button.on_click(self.save_animation_mp4)

        scrollbar = widgets.IntSlider(min=0, max=len(self.data)-1, step=1, value=0, description='Frame')
        scrollbar.observe(self.on_scroll_change, names='value')

        # Display the widgets
        display(play_pause_button)
        display(save_gif_button)
        display(save_frame_button)
        display(scrollbar)
        display(save_mp4_button)

    def on_play_pause_button_click(self, button):
        if self.paused:
            self.ani.event_source.start()
            button.description = 'Pause'
        else:
            self.ani.event_source.stop()
            button.description = 'Play'
        self.paused = not self.paused

    def on_scroll_change(self, change):
        self.current_frame = change['new']
        if not self.paused:
            self.ani.event_source.stop()
        self.animate(self.current_frame)

    def save_animation(self, button):
        writer = animation.PillowWriter(fps=15)
        os.chdir(self.res_folder) #save the animation in results folder
        self.ani.save(f'{self.data_type}.gif', writer=writer)

    def save_frame(self, button): ###THIS PART IS NOT UPDATED
        # Calculate time in minutes and seconds
        time_sec2 = self.current_frame * 5
        minutes, seconds = divmod(time_sec2, 60)

        fig, ax = plt.subplots()
        ax.plot(self.points, self.data[self.current_frame])
        ymin = []
        ymax = []
        yminmin, ymaxmax = 0,0
        for i in range(len(self.data)):
            ymin.append(np.min(self.data[i]))
            ymax.append(np.max(self.data[i]))
        yminmin = np.min(ymin)
        ymaxmax = np.max(ymax)
        ax.set_ylim(yminmin+yminmin/10, ymaxmax+ymaxmax/10)
        ax.set_xlim(-130/self.sampling/self.time_width*self.sample_thick,150/self.sampling/self.time_width*self.sample_thick )
        ax.set_xlabel(self.x_axis_plot)
        ax.set_ylabel(self.data_type_name())
        if 0 <= minutes < 1 or 21 <= minutes < 51:
            title_color = 'blue'
        elif 1 <= minutes < 21:
            title_color = 'red'
        else:
            title_color = 'black'
        DC_status = "DC applied" if 0 <= minutes <= 51 else "No DC applied"
        irradiating_status = "Shutter open: irradiation" if 1 <= minutes <= 20 else "Shutter closed: no irradiation"
        self.ax.set_title(f'{DC_status} - {irradiating_status} - {self.data_type_name()} - Time: {minutes:02d}:{seconds:02d}', color=title_color)
        plt.grid(True)

        plt.savefig(f'frame_{self.current_frame:03d}.png')
        plt.close(fig)

    def save_animation_mp4(self, button):
        plt.rcParams['animation.ffmpeg_path'] = r'D:\Programmes\ffmpeg-2023-03-30-git-4d216654ca-full_build\bin'  # Replace this with the path to your FFmpeg executable
        writer = FFMpegWriter(fps=15, bitrate=1800, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'], metadata={'artist': 'Your_Name'})
        self.ani.save(f'{self.data_type}.mp4', writer=writer)
    
    
    




#230516K1
plot = Datatoplotgif(data_type = "CD", results_folder= "C:\\Users\\pierr\\Desktop\\PEA\\230516K1\\results",  x_axis_type = "position", sample_thickness = 127.8, sound_velocity = 2200, sampling = 1.25, nb_frames = 984, x_left_lim = 144, x_right_lim=257, x_peak1=164, x_peak2=237, x_max_CD = 38.817)
