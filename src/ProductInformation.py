from pydantic import BaseModel
# 2. Class which describes Product description
class ProductCategory(BaseModel):
    id: str 
    main_text: str 
    add_text: str 
    manufacturer: str