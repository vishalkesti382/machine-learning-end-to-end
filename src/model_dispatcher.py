#This script will dispatch our models to our training script.
# model_dispatcher.py

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

models = {
	"rf": RandomForestClassifier(n_estimators=400, max_depth=3, random_state=0),
	"linear_svc": LinearSVC(),
	"multi_nb": MultinomialNB(),
	"lr": LogisticRegression(random_state=0)
}

