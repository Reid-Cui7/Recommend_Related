train_file=/Users/mac/Codes/Projects/Dataset/mksz297/train_data.txt
item_vec_file=/Users/mac/Codes/Projects/Recommend_Related/MK297/production/item_vec.txt
../bin/word2vec -train $train_file -output $item_vec_file -cbow 0 -size 128 -window 5 -negative 5 -hs 1 -sample 1e-3 -threads 20 -binary 0 -iter 50