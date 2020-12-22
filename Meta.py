DATASET_ROOT = "/Users/liaoyuanda/Desktop/Deep Learning Collection/TIMIT/"
TEST_ROOT  = DATASET_ROOT + "TEST";
TRAIN_ROOT = DATASET_ROOT + "TRAIN";

PROJ_ROOT = "/Users/liaoyuanda/Desktop/LP_cocktail/"

GEND = ['F', 'M'] # genders
NUM_SPK = 630

Fs = 16000  # all waves should have Fs = 16000

NUM_DR = 8  # 8 dialectic regions in each TEST/TRAIN

SA_SENT_ID_RANGE = [1, 2]
SX_SENT_ID_RANGE = [3, 452]
SI_SENT_ID_RANGE = [453, 2342]

NON_PHONE = ["pau", "epi", "h#"]