"""Bll for inventory app."""
from django.db.models import Q

import dal as inventory_dal

import utilities

from .exceptions import UnauthorizedPassword
from .exceptions import InvalidUserParameters
from .exceptions import InvalidBrandDetails
from .exceptions import InvalidCategoryDetails
from .exceptions import InvalidItemDetails
from .exceptions import InvalidVariantDetails
from .exceptions import InvalidVariantPropertyDetails

from .constants import USER_ACTION_STATUS_CREATED
from .constants import USER_ACTION_STATUS_UPDATED
from .constants import USER_ACTION_STATUS_DELETED


def user_signup(user_dict):
    """For signing up user."""
    user = inventory_dal.create_user(user_dict)
    user_data = get_user_details(user)

    return user_data


def user_login(user_dict):
    """For user login."""
    user = inventory_dal.validate_user(user_dict)
    user_data = get_user_details(user)

    return user_data


def user_logout(user_dict):
    """For logging out user."""
    user = inventory_dal.get_user_by_id(user_dict['email'])
    inventory_dal.generate_user_access_token(user)
    user.save()

    return {'success': True}


def get_user_details(user):
    """For getting user data by user."""
    try:
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'access_token': user.access_token
        }
    except:
        raise InvalidUserParameters

    return user_data


def get_brands(brands_dict):
    """For getting brands."""
    brands = inventory_dal.get_all_brands()
    brand_data = {}
    brand_data['brands'] = []

    for brand in brands:
        brand_details = get_brand_details(brand)
        brand_data['brands'].append(brand_details)

    return brand_data


def get_brand_details(brand):
    """For getting brand details."""
    try:
        brand_details = {
            'brand_id': brand.id,
            'brand_name': brand.name
        }
    except:
        raise InvalidBrandDetails

    return brand_details


def get_categories(category_dict):
    """For getting categories."""
    categories = inventory_dal.get_all_categories()

    category_data = {}
    category_data['categories'] = []

    for category in categories:
        category_details = get_category_details(category)
        category_data['categories'].append(category_details)

    return category_data


def get_category_details(category):
    """For category details."""
    try:
        category_details = {
            'category_id': category.id,
            'category_name': category.name
        }
    except:
        raise InvalidCategoryDetails

    return category_details


def create_item(item_dict):
    """For creating items."""
    item_dict['brand'] = inventory_dal.get_brand_by_id(item_dict['brand_id'])
    item_dict['category'] = inventory_dal.get_category_by_id(
        item_dict['category_id'])
    item = inventory_dal.create_item_obj(item_dict)

    item_dict['action'] = 'item ' + item.name
    item_dict['status'] = USER_ACTION_STATUS_CREATED
    inventory_dal.create_user_action(item_dict)

    return {'success': True, 'item_id': item.id}


def get_items(item_dict):
    """For getting item list of data."""
    item_data = {}
    item_data['items'] = []

    item_dict = utilities.setup_default_meta_data(item_dict)
    item_dict['objects'] = inventory_dal.get_all_items()
    item_dict['count'] = item_dict['objects'].count('item')
    item_dict['items'] = utilities.setup_query_limit(item_dict)

    for item in item_dict['items']:
        item_details = get_item_data(item)
        print get_item_data(item)
        item_data['items'].append(item_details)

    return item_data


def get_item_details(item_dict):
    """For getting specific item details."""
    item = inventory_dal.get_item_by_id(item_dict['item_id'])
    item_data = get_item_data(item)
    item_data['variants'] = []

    item_dict = utilities.setup_default_meta_data(item_dict)
    item_dict['objects'] = inventory_dal.filter_variants_by_item(item)
    item_dict['count'] = item_dict['objects'].count()
    item_dict['variants'] = utilities.setup_query_limit(item_dict)

    for variant in item_dict['variants']:
        variant_details = get_variant_data(variant)

        variant_details['properties'] = []
        variant_properties = \
            inventory_dal.filter_variant_properties_by_variant(variant)
        for variant_property in variant_properties:
            property_details = get_variant_property_data(variant_property)
            variant_details['properties'].append(property_details)
        item_data['variants'].append(variant_details)

    return item_data


def get_item_data(item):
    """For getting item data."""
    try:
        item_details = {
            'id': item.id,
            'name': item.name,
            'product_code': item.product_code
        }
    except:
        raise InvalidItemDetails
    item_details.update(get_brand_details(item.brand))
    item_details.update(get_category_details(item.category))

    return item_details


def update_item_details(item_dict):
    """For updating item obj."""
    item_dict['item'] = inventory_dal.get_item_by_id(item_dict['item_id'])
    item_dict['action'] = 'item '
    item_dict = inventory_dal.update_item_data(item_dict)

    item_dict['status'] = USER_ACTION_STATUS_UPDATED
    inventory_dal.create_user_action(item_dict)

    return {'success': True}


def delete_item(item_dict):
    """For deleting item."""
    item = inventory_dal.get_item_by_id(item_dict['item_id'])

    item_dict['action'] = 'item ' + item.name
    item_dict['status'] = USER_ACTION_STATUS_DELETED
    inventory_dal.create_user_action(item_dict)

    data = inventory_dal.delete_item_obj(item)

    return data


def create_item_variants(item_dict):
    """For creating item variants."""
    item = inventory_dal.get_item_by_id(item_dict['item_id'])
    item_dict['item'] = item
    variant = inventory_dal.create_variant_object(item_dict)

    item_dict['action'] = 'variant ' + variant.name
    item_dict['status'] = USER_ACTION_STATUS_CREATED
    inventory_dal.create_user_action(item_dict)

    for variant_property_dict in item_dict['variant_properties']:
        variant_property_dict['variant'] = variant
        variant_property_dict['property'] = inventory_dal.get_property_by_id(
            variant_property_dict['property_id'])
        variant_property = inventory_dal.create_variant_property_object(
            variant_property_dict)

        item_dict['action'] = 'variant property ' + \
            variant_property.property_value + ' of variant ' + variant.name
        inventory_dal.create_user_action(item_dict)

    return {'success': True}


def get_variant_data(variant):
    """For getting variant data."""
    try:
        variant_details = {
            'id': variant.id,
            'name': variant.name,
            'selling_price': variant.selling_price,
            'cost_price': variant.cost_price,
            'quantity': variant.quantity
        }
    except:
        raise InvalidVariantDetails

    return variant_details


def update_variants(variant_dict):
    """For updating variant details."""
    variant_dict['variant'] = inventory_dal.get_variant_by_id(
        variant_dict['variant_id'])
    inventory_dal.update_variant_obj(variant_dict)

    variant_dict['action'] = 'variant ' + variant_dict['variant'].name
    variant_dict['status'] = USER_ACTION_STATUS_UPDATED
    inventory_dal.create_user_action(variant_dict)

    return {'success': True}


def delete_variant(variant_dict):
    """For deleting variant."""
    variant = inventory_dal.get_variant_by_id(variant_dict['variant_id'])

    variant_dict['action'] = 'variant ' + variant_dict['variant'].name
    variant_dict['status'] = USER_ACTION_STATUS_DELETED
    inventory_dal.create_user_action(variant_dict)

    data = inventory_dal.delete_variant_obj(variant)

    return data


def create_variant_properties(variant_dict):
    """For creating variant properties."""
    variant_dict['variant'] = inventory_dal.get_variant_by_id(
        variant_dict['variant_id'])
    variant_dict['property'] = inventory_dal.get_property_by_id(
        variant_dict['property_id'])
    variant_property = inventory_dal.create_variant_property_object(
        variant_dict)

    variant_dict['action'] = 'variant property ' + \
        variant_property.property_value + ' of variant ' + \
        variant_dict['variant'].name
    variant_dict['status'] = USER_ACTION_STATUS_CREATED
    inventory_dal.create_user_action(variant_dict)

    return {'variant_property': variant_property.id}


def get_variant_property_data(variant_property):
    """For getting variant property data."""
    try:
        property_details = {
            'id': variant_property.id,
            'property_id': variant_property.property.id,
            'property': variant_property.property.name,
            'property_value': variant_property.property_value
        }
    except:
        raise InvalidVariantPropertyDetails

    return property_details


def update_variant_property_details(variant_dict):
    """For updaing variant property details."""
    variant_dict['variant_property'] = \
        inventory_dal.get_variant_property_by_id(
        variant_dict['variant_property_id'])
    data = inventory_dal.update_variant_property_data(variant_dict)

    variant_dict['action'] = 'variant property ' + \
        variant_dict['variant_property'].property_value + ' of variant ' + \
        variant_dict['variant'].name
    variant_dict['status'] = USER_ACTION_STATUS_UPDATED
    inventory_dal.create_user_action(variant_dict)

    return data


def delete_variant_property(variant_dict):
    """For deleting variant property."""
    variant_property = inventory_dal.get_variant_property_by_id(
        variant_dict['variant_property_id'])

    variant_dict['action'] = 'variant property ' + \
        variant_dict['variant_property'].property_value + ' of variant ' + \
        variant_dict['variant'].name
    variant_dict['status'] = USER_ACTION_STATUS_DELETED
    inventory_dal.create_user_action(variant_dict)

    data = inventory_dal.delete_variant_property_obj(variant_property)

    return data


def get_user_actions(user_dict):
    """For getting user actions."""
    user_data = {}
    user_data['actions'] = []

    user_actions = inventory_dal.filter_user_actions(user_dict)
    for user_action in user_actions:
        user_action_details = {
            'id': user_action.id,
            'user': user_action.actor,
            'action': user_action.action,
            'status': user_action.status,
            'edited_time': str(user_action.edited_time),
            'message': (
                user_action.actor + ' ' + user_action.status + ' ' +
                user_action.action)
        }
        user_data['actions'].append(user_action_details)

    return user_data


def get_property_data(property_dict):
    """For getting property data."""
    properties = inventory_dal.get_all_properties()
    property_data = {}
    property_data['properties'] = []

    for property_obj in properties:
        property_dict = {
            'property_id': property_obj.id,
            'property_name': property_obj.name
        }
        property_data['properties'].append(property_dict)

    return property_data
