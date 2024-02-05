import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.utils.validation import column_or_1d

orig_data = pd.read_csv('aum_sam_summary.csv')
orig_data.columns = ['mean', 'std', 'min', 'q1', 'q2', 'q3', 'max', 'who']
X = orig_data[['min', 'q1', 'mean', 'q3', 'max']]
y = column_or_1d(orig_data[['who']])
clf = LogisticRegression(random_state=0).fit(X, y)
print(f"Model score = {clf.score(X, y)}.")
