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

### What's Next?

Model performance is often dependent on the specific way data is split. To ensure our model is truly reliable and representative, the next step is **Cross-validation**, which splits the data into multiple "folds" to get a more robust estimate of performance.

Would you like me to create a summary table comparing **Ridge** and **Lasso** regularization for your notes?
