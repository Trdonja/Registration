import numpy as np
from scipy.ndimage.morphology import binary_erosion
from math import sqrt


def dice(array1, array2):
    intersection = np.count_nonzero(np.logical_and(array1, array2))
    n1 = np.count_nonzero(array1)
    n2 = np.count_nonzero(array2)
    return 2 * intersection / (n1 + n2)


def hausdorff(array1, array2, voxelspacing=None):
    erosion_structure = np.array([[[False], [False], [False]], [[False], [True], [False]], [[False], [False], [False]],
                                  [[False], [True], [False]], [[True], [True], [True]], [[False], [True], [True]],
                                  [[False], [False], [False]], [[False], [True], [False]], [[False], [False], [False]]])
    sp1 = np.transpose(np.array(np.where(np.logical_xor(array1, binary_erosion(array1, erosion_structure)))))
    sp2 = np.transpose(np.array(np.where(np.logical_xor(array2, binary_erosion(array2, erosion_structure)))))
    if voxelspacing is not None:
        assert isinstance(voxelspacing, np.ndarray)
        sp1 = sp1 * voxelspacing
        sp2 = sp2 * voxelspacing
    d1 = np.array([np.sum(np.square(p - sp2), 1).min() for p in sp1]).max()
    d2 = np.array([np.sum(np.square(p - sp1), 1).min() for p in sp2]).max()
    return sqrt(max([d1, d2]))


def metrics(mask_image1, mask_image2, list_of_mask):
    """METRICS similarity between two image masks

    The result is a numpy array with size 2xN, where N is the length of list of mask.
    First row contains DICE coefficients, second row contains Hausdorff distances.
    """
    import nibabel as nib
    m = max(list_of_mask)
    image1 = nib.load(mask_image1)
    image2 = nib.load(mask_image2)
    array1 = image1.get_data()
    array2 = image2.get_data()
    spacing = image1.header['pixdim'][[1, 2, 3]]
    array1[np.where(array2 < 0)] = 0
    array1[np.where(array2 > m)] = 0
    result = np.zeros((2, len(list_of_mask)))
    for i, masknum in enumerate(list_of_mask):
        result[0, i] = dice(array1 == masknum, array2 == masknum)
        result[1, i] = hausdorff(array1 == masknum, array2 == masknum, voxelspacing=spacing)
    return result
