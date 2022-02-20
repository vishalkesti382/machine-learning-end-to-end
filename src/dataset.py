# This script will create the required dataset to train our model.
# It will also be used to preprocess our data

import re
import string


# Preprocessing the data from the columns
def clean_text(s):
    """
    This function cleans the text a bit
    :param s: string
    :return: cleaned string
    """
    # split by all whitespaces
    s = s.split()

    # join tokens by single space
    s = " ".join(s)

    # remove all punctuations using regex and string module
    s = re.sub(f'[{re.escape(string.punctuation)}]', ' ', s)

    # you can add more cleaning here if you want

    # and then return the cleaned string
    return s


def feature_engineering(data):
    """
    This function performs feature engineering on the columns decided during the EDA
    :param data: pandas dataframe
    :return: data
    """
    # Merging the "main_text" and "add_text" since some times the "main_text" doesn't have any valid description
    data['new_feature'] = data.clean_main_text.astype(str) + " " + data.clean_add_text.astype(str)

    return data


def preprocess(data):
    """
    This function preprocess the data based on the assumptions made during the EDA
    :param data: pandas dataframe
    :return: data
    """
    # Convert the categorical values into numeric
    data['product_id'] = data['productgroup'].factorize()[0]
    category_id_df = data[['productgroup', 'product_id']].drop_duplicates().sort_values('product_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['product_id', 'productgroup']].values)

    # fill NaN values in columns "main_text" , "add_text" and "manufacturer" in any
    data.loc[:, "main_text"] = data.main_text.fillna("NO DESCRIPTION AVAILABLE")
    data.loc[:, "add_text"] = data.add_text.fillna("UNASSIGNED")
    data.loc[:, "manufacturer"] = data.manufacturer.fillna("UNKNOWN-BRAND")

    # Clean the text
    data.loc[:, "clean_main_text"] = data.main_text.apply(clean_text)
    data.loc[:, "clean_add_text"] = data.add_text.apply(clean_text)

    return data
