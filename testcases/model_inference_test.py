from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_api_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Model Api is running"}


def test_product_category_contact_lense():
    """
    Test if the product category is correctly identified
    :input: Product description json
    :output: The product should be classified as CONTACT LENSES
    """
    data = {
        "id": "16292628",
        "main_text": "MERALENS A0395 GREEN WEREWOLF KONTAKTLINSEN MIT PFLEGEMITTEL MIT BEHAELTER OHNE STAERKE, 1ER PACK (1 X 2 STUECK)",
        "add_text": "HEALTH&PERSONALCARE__3100OPTICS__3104COLOUREDCONTACTLENSES",
        "manufacturer": "BOSCH"
    }
    response = client.post('http://127.0.0.1:8000/predict', json=data)
    result = response.json()
    expected = {'id': '16292628', 'Product catergory result': 'CONTACT LENSES'}

    assert expected == result


def test_product_category_washing_machine():
    """
    Test if the product category is correctly identified
    :input: Product description json
    :output: The product should be classified as WASHING MACHINE
    """
    data = {
        "id": "26229701",
        "main_text": "WAQ284E25",
        "add_text": "WASCHMASCHINEN",
        "manufacturer": "BOSCH"
    }
    response = client.post('http://127.0.0.1:8000/predict', json=data)
    result = response.json()
    expected = {'id': '26229701', 'Product catergory result': 'WASHINGMACHINES'}

    assert expected == result


def test_product_category_bicycle():
    """
    Test if the product category is correctly identified
    :input: Product description json
    :output: The product should be classified as BICYCLE
    """
    data = {
        "id": "19764614",
        "main_text": "DAHON SPEED D7\xa0SCHWARZ\xa0?\xa0FALTRAD",
        "add_text": "SPORTS__30000WHEELED__30070BIKES",
        "manufacturer": "DAHON"
    }
    response = client.post('http://127.0.0.1:8000/predict', json=data)
    result = response.json()
    expected = {'id': '19764614', 'Product catergory result': 'BICYCLES'}

    assert expected == result


def test_product_usb_memory():
    """
    Test if the product category is correctly identified
    :input: Product description json
    :output: The product should be classified as USB MEMORY
    """
    data = {
        "id": "16576864",
        "main_text": "LEEF IBRIDGE MOBILE SPEICHERERWEITERUNG FUER IPHONE, IPAD UND IPOD - MIT LIGHTNING UND USB, 128 GB",
        "add_text": "PC__1100COMPUTINGMEMORY__1110MEMORYCARDS",
        "manufacturer": "LEEF"
    }
    response = client.post('http://127.0.0.1:8000/predict', json=data)
    result = response.json()
    expected = {'id': '16576864', 'Product catergory result': 'USB MEMORY'}

    assert expected == result


def test_product_information_insufficient():
    """
    Test if the product category is correctly identified
    :input: Product description json
    :output: The product should be classified as CONTACT LENSES
    """
    data = {
        "id": "16292628",
        "main_text": "",
        "add_text": "",
        "manufacturer": "UNBRANDED"
    }
    response = client.post('http://127.0.0.1:8000/predict', json=data)
    result = response.json()
    expected = {'id': '16292628', 'Product catergory result': 'Insufficient information for product classification'}

    assert expected == result
