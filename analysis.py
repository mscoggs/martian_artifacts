import pandas as pd
import os
import numpy as np
# from scipy.interpolate import griddata
# from scipy.interpolate import Rbf
from consts import *
import glob




def get_flux_avg(dir_):
    flux_file = dir_+"/HiDensity/flux_avg.txt"
    colnames = ["phi", "theta"]+[str(x) for x in list(np.arange(80))]
    df = pd.read_csv(flux_file, skiprows=8,names = colnames,sep='\s+')
    return df

def get_cube_avg_flux(dir_):
    l,w,h = BASE_LENGTH, BASE_WIDTH, BASE_HEIGHT
    cube_avg_filehi = dir_+"/HiDensity/cube_avg.txt"
    cube_avg_filelo = dir_+"/LoDensity/cube_avg.txt"
    names = ["velocity", "+x", "-x", "+y", "-y", "+z", "-z", "Earth", "Sun", "anti-Sun", "rot (x)", "rot (y)", "rot (z)"]
    df = pd.read_csv(cube_avg_filehi, skiprows=9,sep='\s+',names=names)
    df2 = pd.read_csv(cube_avg_filelo, skiprows=9,sep='\s+',names=names)
    v,x,y,z = df["velocity"],df["+x"]+df["-x"]+df2["+x"]+df2["-x"], df["+y"]+df["-y"]+df2["+y"]+df2["-y"], df["+z"]+df2["+z"]
    v,x,y,z = v.values, x.values, y.values, z.values
    flux = z*l*w  + x*h*w + y*l*h

    # cube_std_filehi = dir_+"/HiDensity/cube_std.txt"
    # cube_std_filelo = dir_+"/LoDensity/cube_std.txt"
    # names = ["velocity", "+x", "-x", "+y", "-y", "+z", "-z", "Earth", "Sun", "anti-Sun", "rot (x)", "rot (y)", "rot (z)"]
    # df = pd.read_csv(cube_std_filehi, skiprows=9,sep='\s+',names=names)
    # df2 = pd.read_csv(cube_std_filelo, skiprows=9,sep='\s+',names=names)
    # A_x_sq,A_y_sq,A_z_sq = (l*h)**2,(w*h)**2,(l*w)**2
    # x_std_sq = (np.power(df["+x"].values,2)  +  np.power(df["-x"].values,2)  +  np.power(df2["+x"].values,2)  +  np.power(df2["-x"].values,2) ) * A_x_sq
    # y_std_sq = (np.power(df["+y"].values,2)  +  np.power(df["-y"].values,2)  +  np.power(df2["+y"].values,2)  +  np.power(df2["-y"].values,2) ) * A_y_sq
    # z_std_sq = (np.power(df["+z"].values,2)  +  np.power(df2["+z"].values,2)  ) * A_z_sq
    # std_sq = x_std_sq+y_std_sq+z_std_sq

    #return v,flux,std_sq
    return v,flux#,std_sq



def get_density_profile(dir_, lo=False):
    density_profile_file = dir_+"/hidensity.txt"
    if(lo): density_profile_file = dir_+"/lodensity.txt"
    colnames = ["rho_min", "rho_max",   "fraction"]
    df = pd.read_csv(density_profile_file, skiprows=2,names = colnames,sep='\s+')
    return df

# def get_avg_flux(dir_):
#     local = 1
#     cube_avg_file = dir_+"/HiDensity/cube_avg.txt"
#     file = open(cube_avg_file, 'r')
#     lines = file.readlines()
#     for line in lines:
#         if "total cross-sectional flux" in line:
#             return float(line.split()[-2])



def get_all_sim_dirs(data_folder = DATA_FOLDER):
    dir_ = MEM3_DIR +data_folder
    print("Globbing from this dir:", dir_)
    return list(glob.iglob(dir_+"*"))

def pull_phi_theta(fname):
    tail = fname.split("\\")[-1]
    phi = float((tail.split("phi_")[-1]).split("_")[0])
    theta = float(tail.split("_")[-1])
    return phi,theta


def consolidate_sims(save_name, data_folder = DATA_FOLDER,vmin = 0, vmax=90):
    data_folders = get_all_sim_dirs(data_folder = data_folder)


    phis, thetas, flux,stds=[],[],[],[]
    for run_name in data_folders:
        phi, theta = pull_phi_theta(run_name)
        #v,flux_dist,std_sq = get_cube_avg_flux(run_name)
        v,flux_dist = get_cube_avg_flux(run_name)
        args_ = np.where((v>vmin) & (v<vmax))
        avg_flux = np.sum(flux_dist[args_])
        #std = np.sqrt(np.sum(std_sq[args_]))

        phis.append(phi)
        thetas.append(theta)
        flux.append(avg_flux)
        #stds.append(std)

    #thetas,phis, flux,stds = np.array(thetas),np.array(phis), np.array(flux),np.array(stds)
    #df = pd.DataFrame(data={'theta': thetas, 'phi': phis, 'flux': flux, "std": stds})
    thetas,phis, flux = np.array(thetas),np.array(phis), np.array(flux)
    df = pd.DataFrame(data={'theta': thetas, 'phi': phis, 'flux': flux})
    df.to_csv("flux_files/"+save_name)

def read_flux_file(name):
    df = pd.read_csv("flux_files/"+name)
    thetas = np.array(df["theta"])
    phis = np.array(df["phi"])
    impact_rate = np.array(df["flux"])
    return thetas, phis, impact_rate


def interp_impact_rates(phi,theta,name):
    thetas, phis, impact_rate = read_flux_file(name)
    rbf3 = Rbf(thetas, phis, impact_rate, function="multiquadric", smooth=2)
    impact_rate = rbf3(theta, phi)
    return impact_rate
