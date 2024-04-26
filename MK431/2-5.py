import pandas as pd
from sklearn.model_selection import train_test_split


csv_data = pd.read_csv(r"C:\Users\Bean1777\Documents\Codes\Daily\Data\temperature_icecream.csv")
# print(csv_data.head(5))
X = csv_data.iloc[:, :-1]
Y = csv_data.iloc[:, -1]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=40)
print(X_train)
print("=" * 20)
print(X_test)