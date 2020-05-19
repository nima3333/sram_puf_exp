import sys
sys.path.append('src')
from extractor import *

a = np.load("test_same_1.npy", allow_pickle=True)
b = np.load("test_other.npy", allow_pickle=True)
print(np.array_equal(a,b))
_, binary_array = get_arrays_from_save(a)
prob, length = get_proba_array(binary_array)
disp_array = get_displayed_array(prob, binary_array, length)
_, binary_array2 = get_arrays_from_save(b)
print(np.array_equal(binary_array,binary_array2))
prob2, length = get_proba_array(binary_array2)
print(np.array_equal(prob,prob2))
disp_array2 = get_displayed_array(prob2, binary_array2, length)
print(np.array_equal(disp_array,disp_array2))

display_array(disp_array, "first")

print(np.count_nonzero(disp_array==disp_array2))
print(distance.hamming(disp_array, disp_array2)*disp_array.shape[0])
