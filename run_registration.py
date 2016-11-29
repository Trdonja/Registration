import registration
from metrics import metrics
import numpy as np


# ===== Switch registrations on|off, provide output folders and specify parameters. =====

b_elastix_t1 = True
b_elastix_t2 = False
b_ants_t1 = False
b_ants_t2 = False
b_niftyreg_t1 = False
b_niftyreg_t2 = False

f_elastix = 'elastixtp'
f_ants = 'ants_bulat'
f_niftyreg = 'niftyreg'
f_results = 'rezultatiTP'

p_elastix = ('rigid', 'spline')
p_ants = 'bulat'

# =======================================================================================

results_t1 = np.zeros((15, 16))
results_t2 = np.zeros((15, 16))
i_row = 0

for n in range(1, 6):
    # n is an image number
    ctimage = '/home/domen/Registracija/Slike/' + str(n) + '_CT.nii.gz'
    ctmask = '/home/domen/Registracija/Slike/' + str(n) + '_CT_mask.nii.gz'
    mrt1image = '/home/domen/Registracija/Slike/' + str(n) + '_MR_T1.nii.gz'
    mrt2image = '/home/domen/Registracija/Slike/' + str(n) + '_MR_T2.nii.gz'
    mrmask = '/home/domen/Registracija/Slike/' + str(n) + '_MR_mask.nii.gz'
    output_dir = '/home/domen/Registracija/Rezultati/' + str(n) + '/'

    list_of_mask = [1, 2, 3, 4, 5, 6, 7, 8]
    if n == 3:
        list_of_mask = [1, 3, 5, 6, 7]

    i_dice = (np.array(list_of_mask) - 1) * 2
    i_hsdf = i_dice + 1

    # --- Elastix ---

    output_dir_elastix = output_dir + f_elastix

    if b_elastix_t1:
        registration.elastix(ctimage, mrt1image, output_dir_elastix + '/T1/', parameters=p_elastix)
        registration.transformix_masks(mrmask, output_dir_elastix + '/T1/')
        a = metrics(ctmask, output_dir_elastix + '/T1/result.nii.gz', list_of_mask)
        results_t1[i_row, i_dice] = a[0, :]
        results_t1[i_row, i_hsdf] = a[1, :]
    if b_elastix_t2:
        registration.elastix(ctimage, mrt2image, output_dir_elastix + '/T2/', parameters=p_elastix)
        registration.transformix_masks(mrmask, output_dir_elastix + '/T2/')
        a = metrics(ctmask, output_dir_elastix + '/T2/result.nii.gz', list_of_mask)
        results_t2[i_row, i_dice] = a[0, :]
        results_t2[i_row, i_hsdf] = a[1, :]

    i_row += 1

    # --- ANTs ---

    output_dir_ants = output_dir + f_ants

    if b_ants_t1:
        registration.ants(ctimage, mrt1image, output_dir_ants + '/T1/', parameters=p_ants)
        registration.ants_transform_mask(ctimage, mrmask, output_dir_ants + '/T1/')
        a = metrics(ctmask, output_dir_ants + '/T1/mask.nii.gz', list_of_mask)
        results_t1[i_row, i_dice] = a[0, :]
        results_t1[i_row, i_hsdf] = a[1, :]
    if b_ants_t2:
        registration.ants(ctimage, mrt2image, output_dir_ants + '/T2/', parameters=p_ants)
        registration.ants_transform_mask(ctimage, mrmask, output_dir_ants + '/T2/')
        a = metrics(ctmask, output_dir_ants + '/T2/mask.nii.gz', list_of_mask)
        results_t2[i_row, i_dice] = a[0, :]
        results_t2[i_row, i_hsdf] = a[1, :]

    i_row += 1

    # --- NiftyReg ---

    output_dir_niftyreg = output_dir + f_niftyreg

    if b_niftyreg_t1:
        registration.niftyreg(ctimage, mrt1image, output_dir_niftyreg + '/T1/')
        registration.niftyreg_transform_mask(ctimage, mrmask, output_dir_niftyreg + '/T1/')
        a = metrics(ctmask, output_dir_niftyreg + '/T1/mask.nii.gz', list_of_mask)
        results_t1[i_row, i_dice] = a[0, :]
        results_t1[i_row, i_hsdf] = a[1, :]
    if b_niftyreg_t2:
        registration.niftyreg(ctimage, mrt2image, output_dir_niftyreg + '/T2/')
        registration.niftyreg_transform_mask(ctimage, mrmask, output_dir_niftyreg + '/T2/')
        a = metrics(ctmask, output_dir_niftyreg + '/T2/mask.nii.gz', list_of_mask)
        results_t2[i_row, i_dice] = a[0, :]
        results_t2[i_row, i_hsdf] = a[1, :]

    i_row += 1

# --- Write results in file ---

f = open('/home/domen/Registracija/Rezultati/' + f_results + '.txt', 'w')
f.write('T1\n')
for i in range(0, 15):
    for j in range(0, 16):
        f.write(str(results_t1[i, j]) + '\t')
    f.write('\n')
f.write('T2\n')
for i in range(0, 15):
    for j in range(0, 16):
        f.write(str(results_t2[i, j]) + '\t')
    f.write('\n')
f.close()
