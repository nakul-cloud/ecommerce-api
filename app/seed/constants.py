"""
Application constants used for database seeding.
"""

# ==================================================
# Product Categories
# ==================================================

PRODUCT_CATEGORIES = {
    "Electronics": {
        "brands": [
            "Sony",
            "LG",
            "Samsung",
            "Philips",
            "Panasonic",
        ],
        "products": [
            "Smart TV",
            "Bluetooth Speaker",
            "Wireless Earbuds",
            "Smart Watch",
            "Power Bank",
            "Sound Bar",
            "Projector",
            "Monitor",
        ],
        "price_range": (2000, 150000),
        "stock_range": (20, 150),
    },

    "Mobiles": {
        "brands": [
            "Apple",
            "Samsung",
            "Google",
            "OnePlus",
            "Nothing",
            "Xiaomi",
            "Motorola",
            "Realme",
        ],
        "products": [
            "iPhone",
            "Galaxy",
            "Pixel",
            "Nord",
            "Phone",
            "Edge",
            "Redmi",
        ],
        "price_range": (15000, 150000),
        "stock_range": (10, 80),
    },

    "Laptops": {
        "brands": [
            "Apple",
            "Dell",
            "HP",
            "Lenovo",
            "ASUS",
            "Acer",
            "MSI",
        ],
        "products": [
            "MacBook",
            "XPS",
            "ThinkPad",
            "Victus",
            "ROG",
            "Inspiron",
            "ZenBook",
        ],
        "price_range": (35000, 250000),
        "stock_range": (5, 40),
    },

    "Gaming": {
        "brands": [
            "Logitech",
            "Razer",
            "SteelSeries",
            "HyperX",
            "Corsair",
        ],
        "products": [
            "Gaming Mouse",
            "Gaming Keyboard",
            "Gaming Headset",
            "Gaming Chair",
            "Gaming Monitor",
            "Controller",
        ],
        "price_range": (1000, 80000),
        "stock_range": (15, 120),
    },

    "Books": {
        "brands": [
            "O'Reilly",
            "Pearson",
            "Packt",
            "Penguin",
        ],
        "products": [
            "Python Programming",
            "Clean Code",
            "Atomic Habits",
            "Deep Work",
            "Design Patterns",
            "Machine Learning",
            "AI Fundamentals",
        ],
        "price_range": (300, 3000),
        "stock_range": (80, 300),
    },

    "Fashion": {
        "brands": [
            "Nike",
            "Adidas",
            "Puma",
            "Levis",
            "Zara",
            "H&M",
        ],
        "products": [
            "T-Shirt",
            "Jeans",
            "Sneakers",
            "Running Shoes",
            "Jacket",
            "Hoodie",
        ],
        "price_range": (500, 12000),
        "stock_range": (50, 250),
    },

    "Sports": {
        "brands": [
            "Nike",
            "Yonex",
            "SG",
            "Cosco",
        ],
        "products": [
            "Football",
            "Cricket Bat",
            "Yoga Mat",
            "Dumbbells",
            "Basketball",
            "Tennis Racket",
        ],
        "price_range": (500, 25000),
        "stock_range": (30, 150),
    },

    "Beauty": {
        "brands": [
            "Loreal",
            "Nivea",
            "Maybelline",
            "Lakme",
        ],
        "products": [
            "Perfume",
            "Face Wash",
            "Lipstick",
            "Hair Dryer",
            "Body Lotion",
            "Shampoo",
        ],
        "price_range": (200, 10000),
        "stock_range": (50, 250),
    },

    "Home": {
        "brands": [
            "Philips",
            "Prestige",
            "LG",
            "Samsung",
        ],
        "products": [
            "Coffee Maker",
            "Vacuum Cleaner",
            "Dining Table",
            "LED Lamp",
            "Air Purifier",
            "Mixer Grinder",
        ],
        "price_range": (500, 60000),
        "stock_range": (20, 150),
    },

    "Accessories": {
        "brands": [
            "Boat",
            "Anker",
            "Amazon",
            "TP-Link",
            "Logitech",
        ],
        "products": [
            "Laptop Bag",
            "USB-C Hub",
            "Backpack",
            "Wireless Charger",
            "Phone Stand",
            "HDMI Cable",
        ],
        "price_range": (300, 15000),
        "stock_range": (80, 300),
    },
}


# ==================================================
# Product Variants
# ==================================================

PRODUCT_VARIANTS = [
    "Pro",
    "Plus",
    "Ultra",
    "Max",
    "Lite",
    "Mini",
    "Prime",
    "Air",
    "Wireless",
    "RGB",
    "Gen 2",
    "2026 Edition",
    "Series X",
    "Series 10",
]


# ==================================================
# User Seeder
# ==================================================

DEFAULT_ADMIN = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
}

TOTAL_CUSTOMERS = 100


# ==================================================
# Product Seeder
# ==================================================

TOTAL_PRODUCTS = 250


# ==================================================
# Order Seeder
# ==================================================

TOTAL_ORDERS = 1000

MIN_PRODUCTS_PER_ORDER = 1
MAX_PRODUCTS_PER_ORDER = 6

MIN_QUANTITY = 1
MAX_QUANTITY = 4

ORDER_STATUSES = [
    "Pending",
    "Processing",
    "Shipped",
    "Delivered",
]


# ==================================================
# Business Rules
# ==================================================

MIN_COST_PERCENTAGE = 0.55
MAX_COST_PERCENTAGE = 0.82