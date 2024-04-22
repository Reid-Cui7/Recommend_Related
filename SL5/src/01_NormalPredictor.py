from surprise import NormalPredictor
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split


if __name__ == "__main__":
    # load data
    data = Dataset.load_builtin('ml-100k')
    # split data
    trainset, testset = train_test_split(data, test_size=.25)
    # create model
    algo = NormalPredictor()
    # train model
    algo.fit(trainset)
    #  predict
    predictions = algo.test(testset)
    prediction = algo.predict("1", "112")
    # evaluate
    print(f"Accuracy: {accuracy.rmse(predictions)}")