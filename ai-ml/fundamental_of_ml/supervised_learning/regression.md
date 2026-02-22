## 📈 1. Introduction to Linear Regression

Linear regression is used to model the relationship between a **dependent variable** (target) and one or more **independent variables** (features).

### Simple Linear Regression

* **Definition**: Models the relationship between two variables by fitting a linear equation to observed data.


* **The Equation**: $y = ax + b$.
  * $y$: The target variable.
  * $x$: The single feature.
  * $a$: The slope (coefficient).
  * $b$: The intercept.
 ![simple_liner-regression](https://github.com/user-attachments/assets/0e10a540-7db8-4088-82bc-7b01906c72bf)

### Multiple Linear Regression

* **Definition**: An expansion of regression to include scenarios with more than one feature.
* **The Equation**: $y = a_1x_1 + a_2x_2 + ... + a_nx_n + b$.
* **Key Concept**: Each feature is assigned its own coefficient, allowing the model to handle more complex relationships
---

## ⚙️ 2. Mechanics: Ordinary Least Squares (OLS)

How do we choose the "best" line? We use a loss function to minimize error.

* **Residuals**: The difference between the observed value and the predicted value.


* **OLS Objective**: Aims to minimize the **Residual Sum of Squares (RSS)**:
  
![RSS Formula](https://latex.codecogs.com/png.latex?RSS=\sum_{i=1}^{n}(y_i-\hat{y}_i)^2)

---

## 📏 3. Performance Metrics

To assess how well your model generalizes to unseen data, we use specific metrics:

| Metric | Description |
| --- | --- |
| **R² (R-squared)** | Quantifies the variance in target values explained by the features (ranges from 0 to 1). |
| **MSE** | Mean Squared Error; measured in target units squared. |
| **RMSE** | Root Mean Squared Error; the square root of MSE, measuring error in the same units as the target variable. |

---

## 💻 4. Practical Application in Scikit-Learn

The workflow involves splitting data, fitting the model, and evaluating performance.

### Implementation Example

Using the `LinearRegression` class to predict a target (e.g., sales) based on features.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

# 1. Create feature (X) and target (y) arrays
X = sales_df.drop("sales", axis=1).values
y = sales_df["sales"].values

# 2. Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. Fit the model
reg = LinearRegression()
reg.fit(X_train, y_train)

# 4. Make predictions
y_pred = reg.predict(X_test)

# 5. Evaluate performance
print(f"R-squared: {reg.score(X_test, y_test)}")
print(f"RMSE: {root_mean_squared_error(y_test, y_pred)}")

```

(Note: `root_mean_squared_error` is the modern scikit-learn equivalent for RMSE.)

---
## 🔄 5. Cross-Validation: A More Robust Evaluation

Model performance can depend heavily on exactly how we split the data. If we get a "lucky" or "unlucky" split, the performance score might not represent how the model will actually behave on totally new data.

Cross-validation solves this by using **multiple splits**.

### 🧩 The Mechanics: k-fold CV

The most common approach is **k-fold cross-validation**. Here is the general process:

  1. **Split** the data into  equal groups, called **folds**.
  2. **Train** the model on  folds and **test** it on the remaining fold.
  3. **Repeat** this process until every fold has served as the test set exactly once.
  4. **Average** the results to get a more robust performance metric.



### 💻 Implementation in Scikit-Learn

To do this in Python, we use `cross_val_score`. Instead of getting one single  score, we get an array of scores—one for each fold.

```python
from sklearn.model_selection import cross_val_score, KFold

# 1. Define how many folds (e.g., 6)
kf = KFold(n_splits=6, shuffle=True, random_state=42)

# 2. Compute the scores
cv_results = cross_val_score(reg, X, y, cv=kf)

# 3. Look at the mean and standard deviation
print(np.mean(cv_results), np.std(cv_results))

```
