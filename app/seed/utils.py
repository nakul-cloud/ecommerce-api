import random

from faker import Faker

from app.seed.constants import (
    MIN_COST_PERCENTAGE,
    MAX_COST_PERCENTAGE,
)

fake = Faker()


# ==================================================
# Product Helpers
# ==================================================

def random_price(
    minimum: float,
    maximum: float,
) -> float:
    """
    Generate a random selling price.
    """
    return round(
        random.uniform(minimum, maximum),
        2,
    )


def random_cost_price(
    selling_price: float,
) -> float:
    """
    Generate a realistic cost price.
    """
    return round(
        selling_price * random.uniform(
            MIN_COST_PERCENTAGE,
            MAX_COST_PERCENTAGE,
        ),
        2,
    )


def random_stock(
    minimum: int = 20,
    maximum: int= 200,
) -> int:
    """
    Generate a random stock quantity.
    """
    return random.randint(
        minimum,
        maximum,
    )


def random_description() -> str:
    """
    Generate a realistic product description.
    """
    return fake.paragraph(
        nb_sentences=3,
    )


# ==================================================
# Order Helpers
# ==================================================

def random_quantity(
    minimum: int = 1,
    maximum: int = 5,
) -> int:
    """
    Generate a random order quantity.
    """
    return random.randint(
        minimum,
        maximum,
    )


# ==================================================
# User Helpers
# ==================================================

def random_username() -> str:
    """
    Generate a random username.
    """
    return fake.user_name()


def random_email() -> str:
    """
    Generate a unique email.
    """
    return fake.unique.email()


def random_phone() -> str:
    """
    Generate a phone number.
    """
    return fake.phone_number()


# ==================================================
# General Helpers
# ==================================================

def random_choice(items):
    """
    Return a random element from a list.
    """
    return random.choice(items)


def random_sample(items, count):
    """
    Return a random sample from a list.
    """
    return random.sample(items, count)