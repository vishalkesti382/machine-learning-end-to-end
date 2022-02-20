import os
import pickle
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from config import TRAINING_FILE, MODEL_OUTPUT, TEST_SIZE, RANDOM_STATE, sublinear_tf, min_df, norm, ngram_range, \
    encoding, stop_words
import dataset
import model_dispatcher


def run():
    """
    This function trains the model and saves it
    :param:None
    :return:None
    """
    # read the training data with folds
    columns = ['id', 'productgroup', 'main_text', 'add_text', 'manufacturer']
    df = pd.read_csv(TRAINING_FILE, sep=';')

    # Convert the categorical values into numeric
    df = dataset.preprocess(df)

    # Perform feature engineering
    df = dataset.feature_engineering(df)

    print(df.shape)

    # Vectorize the data
    tfidf = TfidfVectorizer(sublinear_tf=sublinear_tf, min_df=min_df, norm=norm,
                            encoding=encoding, ngram_range=ngram_range,
                            stop_words=stop_words)
    features = tfidf.fit_transform(df.new_feature).toarray()
    labels = df.product_id

    # Save the features for future
    pickle.dump(tfidf.vocabulary_, open(os.path.join(MODEL_OUTPUT, "feature.pkl"), "wb"))

    # Separating Training and validation data
    X_train, X_valid, y_train, y_valid = train_test_split(features, labels, test_size=TEST_SIZE,
                                                          random_state=RANDOM_STATE, stratify=labels)

    # fetch the model from model_dispatcher
    clf = model_dispatcher.models["linear_svc"]

    # fit the model on training data
    clf.fit(X_train, y_train)

    # create predictions for validation samples
    y_pred = clf.predict(X_valid)

    # calculate & print accuracy
    accuracy = metrics.accuracy_score(y_valid, y_pred)
    print(f"Accuracy={accuracy}")

    # classification report
    print(metrics.classification_report(y_valid, y_pred))

    # save the model
    pickle.dump(clf, open(os.path.join(MODEL_OUTPUT, "Product_Prediction_Model.pkl"), "wb"))


if __name__ == "__main__":
    run()
