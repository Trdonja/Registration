import os
import registration


# case_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16]
cases = ['case_S00033274',
         'case_S07558976',
         'case_S08959108',
         'case_S11000130',
         'case_S12626131',
         'case_S00610196',
         'case_S08072795',
         'case_S08963381',
         'case_S11020898',
         'case_S13675251',
         'case_S00891770',
         'case_S08080681',
         'case_S09281791',
         'case_S11066610',
         'case_S13728456',
         'case_S01093053',
         'case_S08165656',
         'case_S09714882',
         'case_S11486669',
         'case_S02396331',
         'case_S08229148',
         'case_S09825894',
         'case_S11495165',
         'case_S04372280',
         'case_S08676777',
         'case_S10596211',
         'case_S11715851',
         'case_S05495767',
         'case_S08805574',
         'case_S10674703',
         'case_S12524229']

for case_num in cases:  # case_numbers
    # case_folder = '/home/domen/Registracija/Slike_Stanford/case_S' + str(case_num) + '/'
    case_folder = '/home/domen/Registracija/Slike4/' + case_num + '/'
    ctimage = case_folder + 'CT_crop.nii'
    mrimage = case_folder + 'MR_t12.nii'  # 'MR_t1.nii'
    ctmask = case_folder + 'Manual_Segmentations/CT_crop.nii'
    # output_dir = '/home/domen/Registracija/Rezultati_Stanford/' + str(case_num) + '/elastix/'
    output_dir = '/home/domen/Registracija/Rezultati4/' + case_num + '/ants/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # registration.elastix(ctimage, mrimage, output_dir)
    # registration.transformix_masks(ctmask, output_dir)
    registration.ants(ctimage, mrimage, output_dir, parameters='bulat')
    # registration.ants_transform_mask(mrimage, ctmask, output_dir, use_inverse=False)
