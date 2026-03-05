# Iris Model Comparison

## Overview
This project compares three machine learning models on the Iris dataset using Scikit-learn.

Models tested:
- Logistic Regression
- Decision Tree
- Random Forest

## Dataset
The Iris dataset contains 150 samples of iris flowers with four features:
- sepal length
- sepal width
- petal length
- petal width

The goal is to classify flowers into three species.

## Method
1. Load the dataset using Scikit-learn
2. Split data into training (80%) and testing (20%)
3. Train three models:
   - Logistic Regression
   - Decision Tree
   - Random Forest
4. Evaluate models using accuracy on the test set.

## Results

| Model | Accuracy |
|------|------|
| Logistic Regression | 1.00 |
| Decision Tree | 0.93 |
| Random Forest | 1.00 |

## Best Model
Random Forest and Logistic Regression achieved the highest accuracy.

## Reflection
Random Forest often performs well because it combines multiple decision trees, reducing overfitting and improving generalization. Logistic Regression also performed well because the Iris dataset is relatively simple and linearly separable.

Decision Trees can sometimes overfit the training data, which may slightly reduce performance on the test set.