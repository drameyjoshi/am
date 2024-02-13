import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import column_or_1d
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

training_data = 'aum_sam_summary.csv'
test_data = 'test_1_summary.csv'

orig_data = pd.read_csv(training_data)
orig_data.columns = ['mean', 'std', 'min', 'q1', 'q2', 'q3', 'max', 'who']
X = orig_data[['min', 'q1', 'mean', 'q3', 'max']]
y = column_or_1d(orig_data[['who']])
clf = LogisticRegression(random_state=0).fit(X, y)
print(f"Model score = {clf.score(X, y)}.")

test_data = pd.read_csv(test_data)
test_data.columns = ['mean', 'std', 'min', 'q1', 'q2', 'q3', 'max', 'who']
X1 = test_data[['min', 'q1', 'mean', 'q3', 'max']]
y1 = column_or_1d(test_data[['who']])
yp = clf.predict(X1)

accuracy = accuracy_score(y_true=y1, y_pred=yp)
print(f"Accuracy score = {accuracy}.")
cm = confusion_matrix(y_true=y1, y_pred=yp)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot()
plt.show()
