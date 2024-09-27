from pydantic import BaseModel


class ProductBase(BaseModel):
    '''Base model shemas Product'''

    name: str
    description: str
    price: float | int
    count_in_storage: int

    class Config:
        from_orm = True


class ProductCreate(ProductBase):
    pass


class ProductList(ProductBase):
    id: int


class ProductOne(ProductBase):
    id: int


class ProductUpdate(ProductBase):
    pass
