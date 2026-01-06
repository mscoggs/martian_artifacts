import numpy as np
N = 50
OBLIQ = np.radians(1.9)
SOUTHPOLEANGLE = 7
R_OBJECT = 3396.2*1.04 #R_mars, km
D_0 = 2451544.5000000 #J2000 date
NUM_STEPS = 15
RHO_PARTICLE = 3 #grams/cm**3
R_PARTICLE = 0.12 #cm
SEC_PER_DAY = 86400
SEC_PER_YEAR = 3.154e+7
T_ECLIPTIC = 1.02749
W = 2*np.pi/T_ECLIPTIC
TOTAL_DAYS = 3
DAYS = np.linspace(0, T_ECLIPTIC, NUM_STEPS*TOTAL_DAYS)

#RUN_DIR = 'C:/Users/matth/Dropbox/github_repos/martian_artifacts/'
RUN_DIR = 'C:/Users/Matthew/Dropbox/github_repos/martian_artifacts/'
MEM3_DIR = RUN_DIR+"MEM3_Windows/"
OPTIONS_IN = MEM3_DIR+"options_template.txt"
OPTIONS_OUT = MEM3_DIR+"options.txt"
DATA_FOLDER = "data_1000_m6/"
DATA_DIR = MEM3_DIR+DATA_FOLDER
LOG_MIN_MASS = -6.0
TRAJECTORY_FILE_NAME = "trajectory.txt"
MEM3_COMMAND = "MEM3Windows.exe"
FAILED_CHECK_FILE = "HiDensity/cube_avg.txt"
#m = log_min_mass(RHO_PARTICLE, R_PARTICLE)


BASE_LENGTH = 100
BASE_WIDTH = 100
BASE_HEIGHT = 10
BASE_SURF_AREA = 2*BASE_HEIGHT*(BASE_WIDTH+BASE_LENGTH) + BASE_WIDTH*BASE_LENGTH
