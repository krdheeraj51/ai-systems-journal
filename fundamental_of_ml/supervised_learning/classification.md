## 📘 Supervised Learning Overview

Supervised learning is like learning with a teacher 👩‍🏫. You provide the model with **labeled data** (input data + the correct answer) so it can learn the relationship between them.

### 🗂️ The Two Main Types

| Type | Goal | Example |
| --- | --- | --- |
| **Classification** | Predicting a **category** or discrete label. | Is this email "Spam" or "Not Spam"? 📧 |
| **Regression** | Predicting a **continuous** or numeric value. | What will the price of a house be? 🏠 |

### 🛠️ Data Preparation

Before a model can learn, the data must be:

* **Clean**: No missing or corrupted values.
* **Numeric**: Computers understand numbers better than text 🔢.
* **Formatted**: Organized into features (inputs) and targets (outputs).

---

## 🤖 The Scikit-Learn Workflow

The `scikit-learn` library is the industry standard for Python 🐍. It follows a consistent 4-step "API" for almost every model:

1. **Import**: Bring the model into your code.
2. **Instantiate**: Create an instance of the model (often setting "hyperparameters").
3. **Fit**: The actual "training" step where the model learns from the labeled data.
4. **Predict**: Using the trained model to guess labels for new data.

---

## 📍 k-Nearest Neighbors (KNN)

KNN is an intuitive algorithm that works on the principle of **proximity**. It assumes that similar data points stay close to each other.

* **How it works**: To predict the label for a new point, the model looks at the  closest points (neighbors) in the training data.
* **Voting**: The new point is assigned the label that the majority of its neighbors have.

---

To show how the **Scikit-learn** workflow functions in practice, let's use a classic example: classifying flowers based on their measurements.

The "4-step API" is designed to be consistent regardless of which model you use. Here is how it looks using the **K-Nearest Neighbors (KNN)** algorithm we discussed:

### 🛠️ The Scikit-Learn 4-Step Workflow

1. **Import**: Bring the specific algorithm and necessary tools into your environment.
```python
from sklearn.neighbors import KNeighborsClassifier

```


2. **Instantiate**: Create the model "object." This is where you choose your settings, like how many neighbors () to look at.
```python
model = KNeighborsClassifier(n_neighbors=3)

```


3. **Fit**: This is the "training" phase. You give the model your labeled data so it can learn the patterns.
```python
model.fit(X_train, y_train)

```


4. **Predict**: Now that the model is trained, you give it new, unseen data to see what it guesses.
```python
predictions = model.predict(X_new)

```
---
Measuring model performance is a critical part of the machine learning workflow. It helps us understand how well our model can actually make decisions on data it hasn't seen before.

---

## 📈 The Goal of Measuring Performance

In supervised learning, specifically classification, we want to know how often our model gets the answer right.

* 
**Accuracy**: This is a common metric used to quantify performance.


* 
**Formula**: Accuracy is calculated as the number of correct predictions divided by the total number of observations.



---

## 🏗️ The Train/Test Split

A major pitfall in machine learning is measuring accuracy on the same data used to train the model. This doesn't show if the model can **generalize** to new data. Instead, we follow a specific process:

1. 
**Split data**: Divide your dataset into two pieces: a **Training set** and a **Test set**.


2. 
**Fit**: Train the classifier only on the training set.


3. 
**Evaluate**: Calculate the accuracy by checking predictions against the "unseen" test set.



---

## 🐍 Implementation in Scikit-Learn

To perform this split in Python, we use the `train_test_split` function.

```python
from sklearn.model_selection import train_test_split

# Split into 70% training and 30% testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=21, stratify=y)

# Fit the model and check the score
knn.fit(X_train, y_train)
print(knn.score(X_test, y_test))

```

* 
**stratify=y**: This ensures the split reflects the proportion of labels in the original dataset.

---

To visualize how our model is performing, we can plot a **model complexity curve**. This helps us see the relationship between the number of neighbors () and the model's accuracy.

We typically use the `matplotlib` library to create this plot. Here is the process used in the materials:

### 🛠️ Plotting Steps in Python

1. 
**Initialize dictionaries**: Create empty dictionaries to store your training and testing accuracies.


2. 
**Generate a range**: Use `np.arange(1, 26)` to create a list of  values to test.


3. 
**Loop and fit**: For each , instantiate the model, fit it to the training data, and record the scores for both the training and test sets.


4. **Create the plot**:
* 
`plt.plot()`: Plot the training accuracy and testing accuracy against the number of neighbors.


* 
`plt.xlabel()` and `plt.ylabel()`: Label your axes "Number of Neighbors" and "Accuracy".


* 
`plt.legend()`: Add a legend to distinguish between the two lines.





### 📉 Understanding the Results

* 
**Overfitting**: When  is small, training accuracy is very high (often 1.0), but test accuracy may be lower because the model is too complex.


* 
**Underfitting**: When  is large, the model becomes too simple, and both training and test accuracy might decrease.


* 
**The "Sweet Spot"**: We look for the  value where **Testing Accuracy** is at its highest point.
