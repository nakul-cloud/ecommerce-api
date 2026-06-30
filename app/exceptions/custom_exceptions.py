class AppException(Exception):
    """
    Base exception class for all application-specific errors.
    """

    def __init__(self, message: str, status_code: int = 500, errors: list = None):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(self.message)


class BadRequestException(AppException):
    """
    Raised when the client sends a bad request (HTTP 400).
    """

    def __init__(self, message: str = "Bad request", errors: list = None):
        super().__init__(message, status_code=400, errors=errors)


class UnauthorizedException(AppException):
    """
    Raised when authentication is required and has failed or has not yet been provided (HTTP 401).
    """

    def __init__(self, message: str = "Unauthorized", errors: list = None):
        super().__init__(message, status_code=401, errors=errors)


class ForbiddenException(AppException):
    """
    Raised when the user does not have permission (HTTP 403).
    """

    def __init__(self, message: str = "Forbidden", errors: list = None):
        super().__init__(message, status_code=403, errors=errors)


class NotFoundException(AppException):
    """
    Raised when a requested resource is not found (HTTP 404).
    """

    def __init__(self, message: str = "Resource not found", errors: list = None):
        super().__init__(message, status_code=404, errors=errors)


class ConflictException(AppException):
    """
    Raised when there is a state conflict (HTTP 409).
    """

    def __init__(self, message: str = "Conflict", errors: list = None):
        super().__init__(message, status_code=409, errors=errors)


# ==================================================
# Domain-Specific Exceptions
# ==================================================

class ProductNotFoundException(NotFoundException):
    """
    Raised when a requested product does not exist.
    """

    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class ProductOutOfStockException(ConflictException):
    """
    Raised when a requested product does not have enough stock.
    """

    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} does not have enough stock")


class OrderNotFoundException(NotFoundException):
    """
    Raised when a requested order does not exist.
    """

    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} not found")


class InvalidCredentialsException(UnauthorizedException):
    """
    Raised when login credentials are invalid.
    """

    def __init__(self):
        super().__init__("Invalid email or password.")


class InvalidTokenException(UnauthorizedException):
    """
    Raised when a JWT token is invalid or expired.
    """

    def __init__(self):
        super().__init__("Invalid or expired access token.")


class PermissionDeniedException(ForbiddenException):
    """
    Raised when the authenticated user does not have permission.
    """

    def __init__(self):
        super().__init__("You do not have permission to perform this action.")


class InvalidPasswordException(BadRequestException):
    """
    Raised when the current password is incorrect.
    """

    def __init__(self):
        super().__init__("Current password is incorrect.")