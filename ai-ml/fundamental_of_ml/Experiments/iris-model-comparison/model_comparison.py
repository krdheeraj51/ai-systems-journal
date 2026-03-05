# Import libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# 2. Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Create models
log_reg = LogisticRegression(max_iter=200)
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()

# 4. Train models
log_reg.fit(X_train, y_train)
decision_tree.fit(X_train, y_train)
random_forest.fit(X_train, y_train)

# 5. Make predictions
log_pred = log_reg.predict(X_test)
tree_pred = decision_tree.predict(X_test)
forest_pred = random_forest.predict(X_test)

# 6. Evaluate accuracy
log_acc = accuracy_score(y_test, log_pred)
tree_acc = accuracy_score(y_test, tree_pred)
forest_acc = accuracy_score(y_test, forest_pred)

# 7. Print results
print("Model Accuracy Comparison")
print("-------------------------")
print(f"Logistic Regression: {log_acc:.2f}")
print(f"Decision Tree: {tree_acc:.2f}")
print(f"Random Forest: {forest_acc:.2f}")