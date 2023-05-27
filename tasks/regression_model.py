from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt



def regression_model(X, Y,filename):

  x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=1)

  lr = LogisticRegression(max_iter=10000,n_jobs=-1).fit(x_train, y_train)
  lr_proba = lr.predict_proba(x_test)
  lr_proba = lr_proba[:,1]

  fpr, tpr, asd = roc_curve(y_test, lr_proba)
  roc_auc = auc(fpr, tpr)

  #Нарисовать plt.plot
  plt.plot(fpr, tpr)
  plt.plot([0,1], [0,1])
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('ROC-кривая')
  plt.savefig('output/plot-'+filename+'.png')

  return roc_auc