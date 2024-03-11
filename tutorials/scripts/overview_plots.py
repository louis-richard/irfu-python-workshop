from cdflib import CDF
import os
import numpy as np
from pyrfu import pyrf, plot, mms
import xarray as xr
import matplotlib.pyplot as plt

shock_id = 2

destpath = 'shock' + str(shock_id) + '/'
directory = os.listdir(destpath)

# load B field data
t = []
Bdsl = np.ndarray([])
j = 1
for i in range(0, len(directory)):
    if "mms1_fgm_brst_l2" in directory[i]:
        file_path = 'shock' + str(shock_id) + '/' + \
                    directory[i]
        temp_cdf = CDF(file_path)

        t_temp = temp_cdf.varget('Epoch')
        t = np.append(t, t_temp)

        Bdsl_temp = temp_cdf.varget('mms1_fgm_b_dmpa_brst_l2')

        if j == 1:
            Bdsl = Bdsl_temp
            j += 1
        else:
            Bdsl = np.append(Bdsl, Bdsl_temp, axis=0)
            j += 1

Bdsl = Bdsl[:, 0:3]
IX = np.argsort(t)
t = pyrf.cdfepoch2datetime64(np.int64(t))
Bdsl = pyrf.ts_vec_xyz(t[IX], Bdsl[IX, :])

# load E field data
t = []
Edsl = np.ndarray([])
j = 1
for i in range(0, len(directory)):
    if "mms1_edp_brst_l2" in directory[i]:
        file_path = 'shock' + str(shock_id) + '/' + \
                    directory[i]
        temp_cdf = CDF(file_path)

        t_temp = temp_cdf.varget('mms1_edp_epoch_brst_l2')
        t = np.append(t, t_temp)

        Edsl_temp = temp_cdf.varget('mms1_edp_dce_dsl_brst_l2')

        if j == 1:
            Edsl = Edsl_temp
            j += 1
        else:
            Edsl = np.append(Edsl, Edsl_temp, axis=0)
            j += 1

Edsl = Edsl[:, 0:3]
IX = np.argsort(t)
t = pyrf.cdfepoch2datetime64(np.int64(t))
Edsl = pyrf.ts_vec_xyz(t[IX], Edsl[IX, :])

# load Electron moments and omni distribution
t = []
j = 1
for i in range(0, len(directory)):
    if "mms1_fpi_brst_l2_des-moms" in directory[i]:
        file_path = 'shock' + str(shock_id) + '/' + \
                    directory[i]
        temp_cdf = CDF(file_path)

        t_temp = temp_cdf.varget('Epoch')
        t = np.append(t, t_temp)

        Ne_temp = temp_cdf.varget('mms1_des_numberdensity_brst')
        Ve_temp = temp_cdf.varget('mms1_des_bulkv_dbcs_brst')
        Te_temp = temp_cdf.varget('mms1_des_temptensor_dbcs_brst')
        E_temp = temp_cdf.varget('mms1_des_energy_brst')
        F_temp = temp_cdf.varget('mms1_des_energyspectr_omni_brst')

        if j == 1:
            Ne = Ne_temp
            Ve = Ve_temp
            Te = Te_temp
            E = E_temp
            F = F_temp
            j += 1
        else:
            Ne = np.append(Ne, Ne_temp, axis=0)
            Ve = np.append(Ve, Ve_temp, axis=0)
            Te = np.append(Te, Te_temp, axis=0)
            E = np.append(E, E_temp, axis=0)
            F = np.append(F, F_temp, axis=0)
            j += 1
IX = np.argsort(t)
t = pyrf.cdfepoch2datetime64(np.int64(t))
Ne = pyrf.ts_scalar(t[IX], Ne[IX])
Ve = pyrf.ts_vec_xyz(t[IX], Ve[IX, :])
Te = pyrf.ts_tensor_xyz(t[IX], Te[IX, :])
Te = (Te[:, 0, 0] + Te[:, 1, 1] + Te[:, 2, 2]) / 3
E = np.nanmean(E, axis=0)
ePDisto = xr.DataArray(data=F[IX, :], dims=["time", "Energy"], coords=[t[IX], E])

# load Ion distribution
t = []
j = 1
for i in range(0, len(directory)):
    if "mms1_fpi_brst_l2_dis-dist" in directory[i]:
        file_path = 'shock' + str(shock_id) + '/' + \
                    directory[i]
        temp_cdf = CDF(file_path)

        t_temp = temp_cdf.varget('Epoch')
        t = np.append(t, t_temp)

        E_temp = temp_cdf.varget('mms1_dis_energy_brst')
        E_temp_delta = temp_cdf.varget('mms1_dis_energy_delta_brst')
        F_temp = temp_cdf.varget('mms1_dis_dist_brst')
        ph_temp = temp_cdf.varget('mms1_dis_phi_brst')
        if j == 1:

            E = E_temp
            E_delta = E_temp_delta
            F = F_temp
            ph = ph_temp
            th = temp_cdf.varget('mms1_dis_theta_brst')
            j += 1
        else:

            E = np.append(E, E_temp, axis=0)
            E_delta = np.append(E_delta, E_temp_delta, axis=0)
            F = np.append(F, F_temp, axis=0)
            ph = np.append(ph, ph_temp, axis=0)
            j += 1

IX = np.argsort(t)
t = pyrf.cdfepoch2datetime64(np.int64(t))

F = np.transpose(F, [0, 3, 1, 2])

# Get the global attributes
glob_attrs = temp_cdf.globalattsget()
glob_attrs = {**glob_attrs, **{"tmmode": 'brst', "species": 'Ions'}}
glob_attrs["delta_energy_plus"] = E_delta[IX, :]
glob_attrs["delta_energy_minus"] = E_delta[IX, :]

dist_attrs = temp_cdf.varattsget("mms1_dis_dist_brst")
# Get CDF keys to Epoch, energy, azimuthal and elevation angle
# zVariables
dpnd_keys = [dist_attrs[f"DEPEND_{i:d}"] for i in range(4)]
_, depend1_key, depend2_key, depend3_key = dpnd_keys

# Get coordinates attributes
coords_names = ["time", "phi", "theta", "energy"]
coords_attrs = {n: temp_cdf.varattsget(k) for n, k in zip(coords_names, dpnd_keys)}

iPDist = pyrf.ts_skymap(t[IX], F[IX, :, :, :], E[IX, :], ph[IX, :], th, attrs=dist_attrs, coords_attrs=coords_attrs,
                        glob_attrs=glob_attrs)

# Number of Monte Carlo iterations per bin. Decrease to improve performance, increase to improve plot.
n_mc = 2e2

# rotation matrix to new coordinate system
# (this new coordinate system will define the directions along which the distribution will be reduced)
nvec = [1, 0, 0]
t1vec = [0, 1, 0]
t2vec = [0, 0, 1]
r_mat = np.float64(np.stack([nvec, t1vec, t2vec]))

# Reduce ion distribution
# Define velocity grid
v_lim = [-1000.0, 1000.0]  # km/s
v_1d = np.linspace(v_lim[0], v_lim[1], 100) * 1e3
v_nif = np.zeros(3)

f1d = mms.reduce(iPDist, projection_dim="1d", xyz=r_mat, n_mc=n_mc, vg=v_1d)
f1d = f1d.assign_coords(vx=f1d.vx.data - np.dot(v_nif, nvec) / 1e3)

legend_options = dict(
    handlelength=1, ncol=1, frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0)
)

f, axs = plt.subplots(7, sharex="all", figsize=(11, 15))
f.subplots_adjust(hspace=0, left=0.1, right=0.9, bottom=0.05, top=0.95)
plot.plot_line(axs[0], Bdsl)
axs[0].legend(["$B_{x}$", "$B_{y}$", "$B_{z}$"], **legend_options)
axs[0].set_ylabel("$\\mathbf{B}~[\\mathrm{nT}]$")

plot.plot_line(axs[1], Edsl)
axs[1].legend(["$E_{x}$", "$E_{y}$", "$E_{z}$"], **legend_options)
axs[1].set_ylabel("$\\mathbf{E}~[\\mathrm{mV/m}]$")


plot.plot_line(axs[2], Ne)
axs[2].legend(["$Ne$"], **legend_options)
axs[2].set_ylabel("$N_e~[\\mathrm{cm^{-3}}]$")

plot.plot_line(axs[3], Ve)
axs[3].legend(["$V_{ex}$", "$V_{ey}$", "$V_{ez}$"], **legend_options)
axs[3].set_ylabel("$\\mathbf{V_e}~[\\mathrm{km/s}]$")

plot.plot_line(axs[4], Te)
axs[4].legend(["$Te$"], **legend_options)
axs[4].set_ylabel("$T_e~[\\mathrm{eV}]$")

axs[5], caxs5 = plot.plot_spectr(axs[5], ePDisto, yscale="log", cscale="log")
axs[5].set_ylabel("$E~[eV]$")
caxs5.set_ylabel("DEF" + "\n" + "[keV (cm$^2$ s sr keV)$^{-1}$]")

axs[6], caxs6 = plot.plot_spectr(axs[6], f1d, cscale="log")
axs[6].set_ylabel("$v_n~[\\mathrm{km} \\; \\mathrm{s}^{-1}]$")
caxs6.set_ylabel("$F_i~[\\mathrm{s}~\\mathrm{m}^{-4}]$")
plt.show()
