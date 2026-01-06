import numpy as np
import glob
import time
import subprocess
import os
import sys
import shutil
from consts import *
from sim_funcs import *


def write_trajectory_file(phi_0,theta_0, run_name):
    output_file = run_name + "/" +TRAJECTORY_FILE_NAME
    out = open(DATA_DIR+output_file, "w")
    for x in range(6): out.write("# \n")
    for day in DAYS:
        theta = W*day + theta_0
        x,y,z = conv_sph_to_cart(R_OBJECT,phi_0,theta)
        jd = D_0 + day
        vtotal = W*R_OBJECT/SEC_PER_DAY *np.cos(phi_0-0.5*np.pi)#km/s total
        r_2d = np.sqrt(x**2 + y**2)
        vx,vy,vz = -y*vtotal/r_2d, x*vtotal/r_2d, 0.0
        x,y,z,vx,vy,vz = conv_lunar_to_ecliptic(x,y,z,vx,vy,vz)
        row = str(jd)+ " " + str(x) + " " + str(y) + " " + str(z) + " " + str(vx) + " " + str(vy) + " " + str(vz) + " \n"
        out.write(row)
    out.flush()


def modify_options_file(run_name):
    with open(OPTIONS_IN, "r") as file:
        lines = file.readlines()
    output_file = DATA_FOLDER + run_name + "/" +TRAJECTORY_FILE_NAME
    offset = 28
    lines[offset+0] = f"{output_file}\n"
    lines[offset+4] = f"{NUM_STEPS}\n"
    lines[offset+5] = f"{LOG_MIN_MASS}\n"
    lines[offset+8] = f"{DATA_FOLDER+run_name}\n"
    with open(OPTIONS_OUT, "w") as file:
        file.writelines(lines)
    time.sleep(1)
    shutil.copy(OPTIONS_OUT, DATA_DIR + run_name + "/options.txt")

def run_moon_impact_simulation():
    phis, thetas, runs = check_failed_runs()
    N_sub = np.size(runs)
    for phi, theta,run_name, counter in zip(phis, thetas, runs, range(N_sub)):
            write_trajectory_file(phi,theta, run_name)
            modify_options_file(run_name)
            print("Current run: "+run_name+" ("+str(counter) +" of " +str(N_sub) + ")")
            os.chdir(MEM3_DIR)
            time.sleep(2)
            result = subprocess.run(MEM3_COMMAND, shell=True, capture_output=True)
            if result.stdout: print("Command Result: {}".format(result.stdout.decode('utf-8')))
            os.chdir(RUN_DIR)
            time.sleep(5)


def check_failed_runs():
    phis,thetas = init_grid()
    failed_list = []
    runs = []
    print(phis)
    for phi, theta in zip(phis, thetas):
        phi_str = str(round(np.degrees(phi),3))
        theta_str = str(round(np.degrees(theta),3))
        run_name = "phi_"+phi_str+"_theta_"+theta_str
        runs.append(run_name)
        run_dir = DATA_DIR+run_name+"/"
        if(not os.path.exists(run_dir)):
            failed_list.append(1.0)
            os.makedirs(run_dir)
        elif(not os.path.exists(run_dir + FAILED_CHECK_FILE)):
            failed_list.append(1.0)
        else:
            failed_list.append(0)
    failed_list = np.array(failed_list)
    runs = np.array(runs)

    filt_ = np.where(failed_list == 1.0)
    return phis[filt_], thetas[filt_], runs[filt_]


os.chdir(RUN_DIR)
run_moon_impact_simulation()
