import time
import os
import dataset
import uvicorn
from fastapi import FastAPI
from ProductInformation import ProductCategory
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from config import MODEL_OUTPUT

app = FastAPI()
pickle_in = open(os.path.join(MODEL_OUTPUT, "Product_Prediction_Model.pkl"), "rb")
vocab_in = open(os.path.join(MODEL_OUTPUT, "feature.pkl"), "rb")

# Load model
clf = pickle.load(pickle_in)
vocab = pickle.load(vocab_in)


@app.post('/predict')
def predict_product(data: ProductCategory):
    # keep track of time
    start_time = time.time()
    # get data
    data = data.dict()
    # load the data
    id = data['id']
    if not data['main_text']:
        main_text = 'NO DESCRIPTION AVAILABLE'
    else:
        main_text = data['main_text']
    if not data['add_text']:
        add_text = 'NO DESCRIPTION AVAILABLE'
    else:
        add_text = data['add_text']
    manufacturer = data['manufacturer']
    if main_text == 'NO DESCRIPTION AVAILABLE' and add_text == 'NO DESCRIPTION AVAILABLE':
        result = {"id": id, "Product catergory result": "Insufficient information for product classification"}
        return result
    if not manufacturer:
        manufacturer = 'UNKNOWN-BRAND'
    # Merge the features
    final_text = dataset.clean_text(main_text + ' ' + add_text)

    #Load the TfIdf Features
    tfidf = TfidfVectorizer(vocabulary=vocab)
    text_features = tfidf.fit_transform(np.array([final_text]))

    #Predict
    predictions = clf.predict(text_features)
    mapping = {0: 'WASHINGMACHINES', 1: 'USB MEMORY', 2: 'BICYCLES', 3: 'CONTACT LENSES'}
    for text, predicted in zip([final_text], predictions):
        print('"{}"'.format(text))
        print("  - Predicted as: '{}'".format(mapping[predicted]))
        print("")
        print("time_taken {}".format(str(time.time() - start_time)))
        result = {"id": id, "Product catergory result": mapping[predicted]}
        return result

@app.get("/")
async def read_main():
    return {"message": "Model Api is running"}

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


