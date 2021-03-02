from sklearn.svm import SVC
from SVM import match
from sklearn.model_selection import GridSearchCV


tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
train_vec, y = match('jtys_1.txt', 'jtys_2.txt')  # 语义叠加和标签项
model = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring='f1')
model.fit(train_vec, y)  # 匹配
print(model.best_params_)
print("#######################")
means = model.cv_results_['mean_test_score']
params = model.cv_results_['params']
for mean, param in zip(means, params):
    print("%f  with:   %r" % (mean, param))


