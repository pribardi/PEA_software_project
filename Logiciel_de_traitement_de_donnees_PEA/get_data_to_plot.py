
import os
import numpy as np
from IPython.display import display


class GetDataToPlot:
    def __init__(self, data_type='CD', results_folder="C:\\Users\\pierr\\Desktop\\PEA\\230516K1\\results", x_axis_type='position', sample_thickness=127.8, sound_velocity=2200, sampling=1.25, x_left_lim=144,x_right_lim=257, x_peak1=164, x_peak2=237, x_max_CD=38.817, ylim_min=0, ylim_max=0):
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
        #Retieve data from input
        self.data_type = data_type
        self.res_folder = results_folder
        self.x_left_lim = x_left_lim
        self.x_right_lim = x_right_lim
        self.x_peak1 = x_peak1
        self.x_peak2 = x_peak2
        self.x_max_CD = x_max_CD
        self.ylim_min = ylim_min
        self.ylim_max = ylim_max
        self.sample_thick = sample_thickness #display in micrometer
        self.sound_velocity = sound_velocity
        self.sampling = sampling #display in ns
        self.x_axis_type = x_axis_type
        
        #We create self.y holding all the data for each frame
        self.data_type_name = ""
        self.y = np.empty((3,4))
        self.x = np.empty((3,4))
        self.load_y_axis(self.data_type) #reassign self.y 
        self.load_x_axis() #reassign self.x 
        
        
       
    def get_nb_frames(self,folder_path, data_type):
        try:
            file_list = os.listdir(folder_path)
            file_count = 0

            for file in file_list:
                if file.startswith(data_type) and file.endswith(".dat"):
                    file_count += 1
            return file_count

        except FileNotFoundError:
            print("Folder not found.")
            return [], 0
    
    def load_y_axis(self, data_type):
        if data_type in {"CD","cd","charge density","Charge Density","Charge density","chargedensity","Chargedensity","ChargeDensity","dc","DC","density charge"}:
            os.chdir(self.res_folder + "\\CD")
            self.data_type_name = "Charge Density(C/m3)"
        elif data_type in {"EF","ef","fe","FE","Ef","Fe","electric field","Electric Field","Electric field","field electric","electric Field"}:
            os.chdir(self.res_folder + "\\EF")
            self.data_type_name = "Electric Field (kV/mm)"
        elif data_type in {"EP", "ep","Ep","eP","electric potential","potential electric","Electric potential","Electric Potential","electric Potential"}:
            os.chdir(self.res_folder + "\\EP")
            self.data_type_name = "Electric Potential"
        try:
            nb_frames = self.get_nb_frames(os.getcwd(), data_type)
            self.iteration = [str(a).zfill(3) for a in range(nb_frames)]
            self.y = np.array([np.loadtxt(data_type + self.iteration[i] + '.dat') for i in range(len(self.iteration))])
        
        except FileNotFoundError:
            nb_frames = self.get_nb_frames(os.getcwd(), data_type)
            self.iteration_2 = [str(a)for a in range(nb_frames)]
            self.y = np.array([np.loadtxt(data_type + self.iteration_2[i] + '.dat') for i in range(len(self.iteration_2))])
        
            
            
    def load_x_axis(self):
        self.points =[e for e in range(-self.x_peak1,len(self.y[0])-self.x_peak1,1)]
        if self.x_axis_type in {"points","Points","point","Point","POINT","POINTS","p","P"}:
            self.x = self.points
        elif self.x_axis_type in {"time", "Time","TIME","times","Times","TIMES","t","T"}:
            self.x = list(map(lambda x: x/self.sampling), self.points)
        else:
            #default
            self.time_width = self.sample_thick/self.sound_velocity*10**3
            self.x = list(map(lambda x: x/self.sampling/self.time_width*self.sample_thick, self.points ))
           
            
def main():
    data = GetDataToPlot()
    return data

if __name__ == "__main__":
    main()
    



"""#230516K1
plot = Datatoplotgif(data_type = "CD", results_folder= "C:\\Users\\pierr\\Desktop\\PEA\\230516K1\\results",  x_axis_type = "position", sample_thickness = 127.8, sound_velocity = 2200, sampling = 1.25, nb_frames = 984, x_left_lim = 144, x_right_lim=257, x_peak1=164, x_peak2=237, x_max_CD = 38.817)
"""