import subprocess
from os import environ


def add_elastix_to_path():
    elastix_path = '/home/domen/Registracija/Elastix/bin'
    elastix_lib_path = '/home/domen/Registracija/Elastix/lib'
    if elastix_path not in environ['PATH'].split(':'):
        environ['PATH'] = elastix_path + ':' + environ['PATH']
    if elastix_lib_path not in environ['LD_LIBRARY_PATH'].split(':'):
        environ['LD_LIBRARY_PATH'] = elastix_lib_path + ':' + environ['LD_LIBRARY_PATH']


def add_cuda_to_path():
    cuda_path = '/usr/local/cuda-7.5/bin'
    cuda_lib_path = '/usr/local/cuda-7.5/lib64'
    if cuda_path not in environ['PATH'].split(':'):
        environ['PATH'] = cuda_path + ':' + environ['PATH']
    if cuda_lib_path not in environ['LD_LIBRARY_PATH'].split(':'):
        environ['LD_LIBRARY_PATH'] = cuda_lib_path + ':' + environ['LD_LIBRARY_PATH']


def elastix(fixed_image, moving_image, output_dir, parameters=('rigid', 'spline')):
    add_elastix_to_path()
    parameters_rigid = '/home/domen/Registracija/Parametri/' + parameters[0] + '.txt'
    parameters_spline = '/home/domen/Registracija/Parametri/' + parameters[1] + '.txt'
    subprocess.run(['elastix -f ' + fixed_image + ' -m ' + moving_image +
                    ' -out ' + output_dir +
                    ' -p ' + parameters_rigid + ' -p ' + parameters_spline
                    ], shell=True, stdout=subprocess.PIPE, universal_newlines=True)


def transformix_masks(mask_image, output_dir):
    add_elastix_to_path()
    subprocess.run(['sed', '-i', '-e', 's/FinalBSplineInterpolationOrder 3/FinalBSplineInterpolationOrder 0/g',
                    output_dir + 'TransformParameters.1.txt'])
    try:
        subprocess.run(['transformix -in ' + mask_image + ' -out ' + output_dir +
                        ' -tp ' + output_dir + 'TransformParameters.1.txt'
                        ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    finally:
        subprocess.run(['sed', '-i', '-e', 's/FinalBSplineInterpolationOrder 0/FinalBSplineInterpolationOrder 3/g',
                        output_dir + 'TransformParameters.1.txt'])


def ants(fixed_image, moving_image, output_dir, parameters='default'):
    environ['ANTSPATH'] = '/home/domen/Registracija/ANTs/'
    parameter_list = {
        'default':
        ['/home/domen/Registracija/ANTs/antsRegistration -d 3 ' +
         '-r [' + fixed_image + ', ' + moving_image + ', 0] ' +
         '-m Mattes[' + fixed_image + ', ' + moving_image + ', 1, 32, random, 0.3] ' +
         '-t translation[0.1] ' +
         '-c [10000x10000x10000, 1.e-8, 20] ' +
         '-s 4x2x1vox ' +
         '-f 6x2x1 -l 1 ' +
         '-m Mattes[' + fixed_image + ', ' + moving_image + ', 1, 32, random, 0.3] ' +
         '-t rigid[0.1] ' +
         '-c [10000x10000x10000, 1.e-8, 20] ' +
         '-s 4x2x1vox ' +
         '-f 3x2x1 -l 1 ' +
         # '-m Mattes[' + fixed_image + ', ' + moving_image + ', 1, 32, random, 0.1] ' +
         # '-t affine[0.1] ' +
         # '-c [600x300x150, 1.e-8, 20] ' +
         # '-s 2x1x0mm ' +
         # '-f 4x2x1 -l 1 ' +
         '-m Mattes[' + fixed_image + ', ' + moving_image + ', 1, 32, random, 0.1] ' +
         '-t SyN[0.2, 3, 0] ' +
         '-c [100x100x50, -0.01, 5] ' +
         '-s 1x0.5x0vox ' +
         '-f 4x2x1 -l 1 -u 1 -z 1 ' +
         '-o [' + output_dir + ', ' + output_dir + 'image.nii.gz]'  # ' + output_dir + '/Fixed.mha]'
         ],
        'bulat':
        ['/home/domen/Registracija/ANTs/antsRegistration -d 3 ' +
         '-r [' + fixed_image + ', ' + moving_image + ', 0] ' +
         '-t Rigid[0.1] -c [1000x500x250x100, 1.e-8, 20] -s 3x2x1x0mm -f 4x2x2x1 -l 1 ' +
         '-m MI[' + fixed_image + ', ' + moving_image + ', 1, 32, regular, 0.25] ' +
         '-t Similarity[0.1] -c [1000x500x250x5, 1.e-8, 20] -s 3x2x1x0mm -f 4x2x2x1 -l 1 ' +
         '-m MI[' + fixed_image + ', ' + moving_image + ', 1, 32, regular, 0.15] ' +
         '-t BSplineSyN[0.1, 40, 0, 3] -c [100x70x50x20, 0, 5] -s 3x2x1x0mm -f 6x4x2x1 -l 1 ' +
         '-u 1 -z 1 --float 1 ' +
         '-m MI[' + fixed_image + ', ' + moving_image + ', 1, 32, regular, 0.25] ' +
         '-o [' + output_dir + ', ' + output_dir + 'image.nii.gz]'
         ]
    }
    if parameters not in parameter_list:
        print('Unrecognized parameters option. Using default instead.')
        cmd = parameter_list['default']
    else:
        cmd = parameter_list[parameters]
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)


def ants_bulat(fixed_image, moving_image, output_dir):
    environ['ANTSPATH'] = '/home/domen/Registracija/ANTs/'
    cmd = ['/home/domen/Registracija/ANTs/antsRegistration -d 3 ' +
           '-r [' + fixed_image + ', ' + moving_image + ', 0] ' +
           '-t Rigid[0.1] -c [1000x500x250x100, 1.e-8, 20] -s 3x2x1x0mm -f 4x2x2x1 -l 1 ' +
           '-m MI[' + fixed_image + ', ' + moving_image + ', 1, 32, regular, 0.25] ' +
           '-t Similarity[0.1] -c [1000x500x250x5, 1.e-8, 20] -s 3x2x1x0mm -f 4x2x2x1 -l 1 ' +
           '-m MI[' + fixed_image + ', ' + moving_image + ', 1, 32, regular, 0.15] ' +
           '-t BSplineSyN[0.1, 40, 0, 3] -c [100x70x50x20, 0, 5] -s 3x2x1x0mm -f 6x4x2x1 -l 1 -u 1 -z 1 --float 1 ' +
           '-m MI[' + fixed_image + ', ' + moving_image + ', 1, 32, regular, 0.25] ' +
           '-o [' + output_dir + ', ' + output_dir + 'image.nii.gz]'
           ]
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    # print(p.stdout)


def ants_transform_mask(fixed_image, mask_image, output_dir, use_inverse=False):
    if use_inverse:
        warp = '1InverseWarp.nii.gz'
    else:
        warp = '1Warp.nii.gz'
    subprocess.run(['/home/domen/Registracija/ANTs/antsApplyTransforms -d 3' +
                    ' -i ' + mask_image + ' -r ' + fixed_image + ' -o ' + output_dir + 'mask.nii.gz'
                    ' -t ' + output_dir + warp + ' -t ' + output_dir + '0GenericAffine.mat' +
                    ' -n NearestNeighbor -v 98'
                    ], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    subprocess.run(['/home/domen/Registracija/CastImageFilter/bin/CastImageFilter',
                    output_dir + 'mask.nii.gz', 'char', output_dir + 'mask.nii.gz'
                    ], shell=True, stdout=subprocess.PIPE, universal_newlines=True)


def niftyreg(fixed_image, moving_image, output_dir):
    add_cuda_to_path()
    subprocess.run(['/home/domen/Registracija/NiftyReg/install/bin/reg_aladin' +
                    ' -ref ' + fixed_image +
                    ' -flo ' + moving_image +
                    ' -aff ' + output_dir + 'affine.txt' +
                    ' -rigOnly'  # odstrani -rigOnly, če želiš imeti polno afino preslikavo in ne zgolj togo
                    ], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    subprocess.run(['/home/domen/Registracija/NiftyReg/install/bin/reg_f3d' +
                    ' -ref ' + fixed_image +
                    ' -flo ' + moving_image +
                    ' -aff ' + output_dir + 'affine.txt' +
                    ' -cpp ' + output_dir + 'deformable.nii.gz' +
                    ' -res ' + output_dir + 'image.nii.gz' +
                    ' -sx 40 -sy 40 -sz 40 -be 0 -gpu -pad -1'
                    ], shell=True, stdout=subprocess.PIPE, universal_newlines=True)


def niftyreg_transform_mask(fixed_image, mask_image, output_dir):
    subprocess.run(['/home/domen/Registracija/NiftyReg/install/bin/reg_resample' +
                    ' -ref ' + fixed_image +
                    ' -flo ' + mask_image +
                    ' -trans ' + output_dir + 'deformable.nii.gz' +
                    ' -res ' + output_dir + 'mask.nii.gz' +
                    ' -inter 0 -pad 10'
                    ], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
