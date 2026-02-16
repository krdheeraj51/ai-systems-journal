# Scikit-Learn (sklearn) Fundamentals

Scikit-learn is the gold standard library for Machine Learning in Python. It is built on top of **NumPy**, **SciPy**, and **Matplotlib**, providing a consistent interface for various machine learning tasks.

## 1. Core Concepts

* **Estimators:** Any object that can estimate some parameters based on a dataset (e.g., a model). It uses the `.fit()` method.
* **Transformers:** Estimators that also transform the dataset (e.g., scalers). They use the `.transform()` and `.fit_transform()` methods.
* **Predictors:** Estimators capable of making predictions (e.g., classifiers or regressors). They use the `.predict()` method.

## 2. Main Modules

| Module | Purpose | Example Classes |
| --- | --- | --- |
| `preprocessing` | Scaling, encoding, and normalization. | `StandardScaler`, `OneHotEncoder` |
| `model_selection` | Splitting data and tuning hyperparameters. | `train_test_split`, `GridSearchCV` |
| `linear_model` | Traditional linear algorithms. | `LinearRegression`, `LogisticRegression` |
| `ensemble` | Combining multiple models. | `RandomForestClassifier`, `GradientBoosting` |
| `metrics` | Evaluating model performance. | `accuracy_score`, `mean_squared_error` |

---

# The 7-Step Scikit-Learn Workflow

The strength of Scikit-learn is its predictable workflow. Almost every project follows these steps:

### Step 1: Data Preparation

Load your data (often using Pandas) and separate it into features () and targets ().

```python
import pandas as pd
df = pd.read_csv('data.csv')
X = df.drop('target', axis=1)
y = df['target']

```

### Step 2: Split Data

Always set aside a test set to evaluate how your model performs on unseen data.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

```

### Step 3: Preprocessing

Scale or encode your data so the algorithm can process it effectively.

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

```

### Step 4: Choose and Instantiate Model

Pick the algorithm that fits your problem (Classification, Regression, etc.).

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)

```

### Step 5: Train the Model (Fit)

This is where the model "learns" the patterns in your training data.

```python
model.fit(X_train_scaled, y_train)

```

### Step 6: Make Predictions

Use the trained model to predict outcomes for the test set.

```python
y_pred = model.predict(X_test_scaled)

```

### Step 7: Evaluate Performance

Check how well the model did using appropriate metrics.

```python
from sklearn.metrics import accuracy_score
print(f"Model Accuracy: {accuracy_score(y_test, y_pred)}")

```

---

## Pro-Tip: Using Pipelines

To make your code cleaner and prevent data leakage, use the `Pipeline` object to group Step 3, 4, and 5 together:

```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier())
])

pipeline.fit(X_train, y_train) # Fits scaler and then fits classifier

```