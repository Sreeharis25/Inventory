"""Exceptions for inventory app."""


class UnauthorizedEmail(Exception):
    """Request method is unauthorized."""

    def __init__(self):
        """Initial values."""
        self.message = 'Unauthorized Email.'
        self.code = 'u-1'
        self.status_code = 403

    def __str__(self):
        """Object returning."""
        return self.message


class UnauthorizedPassword(Exception):
    """Request method is unauthorized."""

    def __init__(self):
        """Initial values."""
        self.message = 'Unauthorized Password.'
        self.code = 'u-2'
        self.status_code = 403

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidUserParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid User Parameters.'
        self.code = 'u-3'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class UserNotFound(Exception):
    """Request method is not found."""

    def __init__(self):
        """Initial values."""
        self.message = 'User Not Found.'
        self.code = 'u-4'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidUserActionParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid User Action Parameters.'
        self.code = 'u-5'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class BrandNotFound(Exception):
    """Request method is not Found."""

    def __init__(self):
        """Initial values."""
        self.message = 'Brand Not Found.'
        self.code = 'i-1'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message


class CategoryNotFound(Exception):
    """Request method is not Found."""

    def __init__(self):
        """Initial values."""
        self.message = 'Category Not Found.'
        self.code = 'i-2'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidItemParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Item Parameters.'
        self.code = 'i-3'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidBrandDetails(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Brand Details.'
        self.code = 'i-4'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidCategoryDetails(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Category Details.'
        self.code = 'i-5'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidItemDetails(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Item Details.'
        self.code = 'i-6'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidVariantDetails(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Variant Details.'
        self.code = 'i-7'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidVariantPropertyDetails(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Variant Property Details.'
        self.code = 'i-8'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class ItemNotFound(Exception):
    """Request method is not found."""

    def __init__(self):
        """Initial values."""
        self.message = 'Item Not Found.'
        self.code = 'i-9'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidVariantParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Variant Parameters.'
        self.code = 'i-10'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidVariantPropertyParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Variant Property Parameters.'
        self.code = 'i-11'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class VariantNotFound(Exception):
    """Request method is not found."""

    def __init__(self):
        """Initial values."""
        self.message = 'Variant Not Found.'
        self.code = 'i-12'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message


class PropertyNotFound(Exception):
    """Request method is not found."""

    def __init__(self):
        """Initial values."""
        self.message = 'Property Not Found.'
        self.code = 'i-13'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message


class VariantPropertyNotFound(Exception):
    """Request method is not found."""

    def __init__(self):
        """Initial values."""
        self.message = 'Variant Property Not Found.'
        self.code = 'i-14'
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message
