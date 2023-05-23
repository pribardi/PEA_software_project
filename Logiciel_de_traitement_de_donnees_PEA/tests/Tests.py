import os
import sys
scriptpath ="D:\pierr\Documents\GitHub\Logiciel_de_traitement_de_donnees_PEA\main.py"
sys.path.append(os.path.abspath(scriptpath))
import main
from main import Datatoplotgif


"""os.system("python D:\pierr\Documents\GitHub\Logiciel_de_traitement_de_donnees_PEA\main.py")"""
"""import sys
sys.path.append('D:\pierr\Documents\GitHub\Logiciel_de_traitement_de_donnees_PEA\code_source')

from ..code_source import main """

#230516K1
plot = Datatoplotgif(data_type = "CD", results_folder= "C:\\Users\\pierr\\Desktop\\PEA\\230516K1\\results",  x_axis_type = "position", sample_thickness = 127.8, sound_velocity = 2200, sampling = 1.25, nb_frames = 984, x_left_lim = 144, x_right_lim=257, x_peak1=164, x_peak2=237, x_max_CD = 38.817)
