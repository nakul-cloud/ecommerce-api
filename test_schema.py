from app.schemas.product_schema import ProductCreate
product = ProductCreate(
    name="A",
    description="Phone",
    category="E",
    price=-100,
    stock_quantity=-5,
    cost_price=0
)

print(product)

