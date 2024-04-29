python="/Users/mac/.venvs/pt/bin/python"
user_rating_file="/Users/mac/Codes/Projects/Dataset/mksz297/ratings.csv"
train_file="/Users/mac/Codes/Projects/Dataset/mksz297/train_data.txt"
item_vec_file="/Users/mac/Codes/Projects/Recommend_Related/MK297/production/item_vec.txt"
item_sim_file="/Users/mac/Codes/Projects/Recommend_Related/MK297/production/item_sim.txt"
if [ -f $user_rating_file ]; then
    $python produce_train_data.py $user_rating_file $train_file
else
    echo "user_rating_file not found"
    exit 1
fi
if [ -f $train_file ]; then
    sh train.sh $train_file $item_vec_file
else
    echo "train_file not found"
    exit 1
fi
if [ -f $item_vec_file ]; then
    $python produce_item_sim.py $item_vec_file $item_sim_file
else
    echo "item_vec_file not found"
    exit 1
fi