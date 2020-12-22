
import Meta_config
from Meta_config import WIN

if WIN:
	DATASET_ROOT = "C:\\Users\\Lenovo\\Desktop\\TIMIT\\"
else:
	DATASET_ROOT = "/Users/liaoyuanda/Desktop/Deep Learning Collection/TIMIT/"
TEST_ROOT  = DATASET_ROOT + "TEST";
TRAIN_ROOT = DATASET_ROOT + "TRAIN";

if WIN:
	PROJ_ROOT = "C:\\Users\\Lenovo\\Desktop\\LP_cocktail"
else:
	PROJ_ROOT = "/Users/liaoyuanda/Desktop/LP_cocktail"

GEND = ['F', 'M'] # genders
NUM_SPK = 630

Fs = 16000  # all waves should have Fs = 16000

NUM_DR = 8  # 8 dialectic regions in each TEST/TRAIN

SA_SENT_ID_RANGE = [1, 2]
SX_SENT_ID_RANGE = [3, 452]
SI_SENT_ID_RANGE = [453, 2342]

NON_PHONE = ["pau", "epi", "h#"]