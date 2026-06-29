class ProductNotFoundException(Exception):
    """
    Raised when a requested product does not exist.
    """

    def __init__(self,product_id:int):
        self.product_id=product_id
        self.message=f"Product with ID {product_id} not found"

        super().__init__(self.message)


class ProductOutOfStockException(Exception):
    """
    Raised when a requested product does not have enough stock
    """

    def __init__(self,product_id:int,):
        self.product_id=product_id
        self.message=f"Product with ID {product_id} does not have enough stock"

        super().__init__(self.message)


class OrderNotFoundException(Exception):
    """
    Raised when a requested order does not exist
    """

    def __init__(self,order_id:int):
        self.order_id=order_id
        self.message=f"Order with ID{order_id} not found"

        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    """
    Raised when login credentials are invalid.
    """

    def __init__(self):
        self.message = "Invalid email or password."

        super().__init__(self.message)


class InvalidTokenException(Exception):
    """
    Raised when a JWT token is invalid or expired.
    """

    def __init__(self):
        self.message = "Invalid or expired access token."

        super().__init__(self.message)

class PermissionDeniedException(Exception):
    """
    Raised when the authenticated user does not have permission.
    """

    def __init__(self):
        self.message = "You do not have permission to perform this action."

        super().__init__(self.message)
    
class InvalidPasswordException(Exception):
    """
    Raised when the current password is incorrect.
    """
    def __init__(self):
        self.message = "current password is incorrect"
        super().__init__(self.message)