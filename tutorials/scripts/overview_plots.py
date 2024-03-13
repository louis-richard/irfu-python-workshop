from cdflib import CDF
import os
import numpy as np
from pyrfu import pyrf

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