"""Views for inventory app."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt

from json import loads

from .decorators import authenticate_user

import utilities
from utilities import success_response
from utilities import error_response

import bll as inventory_bll

from .exceptions import BrandNotFound
from .exceptions import CategoryNotFound
from .exceptions import InvalidItemParameters
from .exceptions import UnauthorizedPassword
from .exceptions import UnauthorizedEmail
from .exceptions import UserNotFound
from .exceptions import ItemNotFound
from .exceptions import InvalidVariantParameters
from .exceptions import InvalidVariantPropertyParameters
from .exceptions import VariantNotFound
from .exceptions import PropertyNotFound
from .exceptions import VariantPropertyNotFound
from .exceptions import InvalidUserParameters
from .exceptions import InvalidBrandDetails
from .exceptions import InvalidCategoryDetails
from .exceptions import InvalidItemDetails
from .exceptions import InvalidVariantDetails
from .exceptions import InvalidVariantPropertyDetails
from .exceptions import InvalidUserActionParameters


@csrf_exempt
def user_signup(request):
    """For user signup."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['mandatory_params'] = [
            ('password', 'str'), ('email', 'email'),
            ('first_name', 'str'), ('last_name', 'str')]
        user_dict = utilities.fetch_request_params(request_dict)

        user_data = inventory_bll.user_signup(user_dict)
        data = success_response(user_data)
    except(KeyError, ValueError, InvalidUserParameters) as e:
        data = error_response(e)

    return data


@csrf_exempt
def user_login(request):
    """For user signup."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['mandatory_params'] = [
            ('email', 'email'), ('password', 'str')]
        user_dict = utilities.fetch_request_params(request_dict)
        user_data = inventory_bll.user_login(user_dict)

        data = success_response(user_data)
    except(
            KeyError, ValueError, UnauthorizedEmail,
            UnauthorizedPassword, InvalidUserParameters) as e:
        data = error_response(e)

    return data


@csrf_exempt
def user_logout(request, email):
    """For logging out user."""
    user_dict = {}
    try:
        user_dict['email'] = email
        user_data = user_logout(user_dict)
        data = success_response(user_data)
    except (KeyError, ValueError, UserNotFound) as e:
        data = error_response(e)
    return data


@authenticate_user
def get_brands(request, user=None):
    """For getting brands."""
    request_dict = {}
    try:
        request_dict['received_data'] = request.GET
        brands_dict = utilities.fetch_request_params(request_dict)

        brands_data = inventory_bll.get_brands(brands_dict)
        data = success_response(brands_data)
    except (KeyError, ValueError, InvalidBrandDetails) as e:
        data = error_response(e)
    return data


@authenticate_user
def get_categories(request, user=None):
    """For getting categories."""
    request_dict = {}
    try:
        request_dict['received_data'] = request.GET
        category_dict = utilities.fetch_request_params(request_dict)

        category_data = inventory_bll.get_categories(category_dict)
        data = success_response(category_data)
    except (KeyError, ValueError, InvalidCategoryDetails) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def create_item(request, user=None):
    """For creating item."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['mandatory_params'] = [
            ('brand_id', 'int'), ('category_id', 'int'),
            ('name', 'str'), ('product_code', 'str')]
        item_dict = utilities.fetch_request_params(request_dict)
        item_dict['user'] = user

        item_data = inventory_bll.create_item(item_dict)
        data = success_response(item_data)
    except (
            KeyError, ValueError, BrandNotFound,
            CategoryNotFound, InvalidItemParameters) as e:
        data = error_response(e)
    return data


@authenticate_user
def get_item_list(request, user=None):
    """For getting item list."""
    request_dict = {}
    try:
        request_dict['received_data'] = request.GET
        request_dict['optional_params'] = [
            ('offset', 'int'), ('limit', 'int')]
        item_dict = utilities.fetch_request_params(request_dict)
        item_dict['user'] = user
        print user

        item_data = inventory_bll.get_items(item_dict)
        print item_data
        data = success_response(item_data)
    except (
            KeyError, ValueError, BrandNotFound,
            CategoryNotFound, InvalidItemDetails, InvalidBrandDetails,
            InvalidCategoryDetails) as e:
        data = error_response(e)
    return data


@authenticate_user
def get_item_details(request, item_id, user=None):
    """For getting item details."""
    request_dict = {}
    try:
        request_dict['received_data'] = request.GET
        request_dict['optional_params'] = [
            ('offset', 'int'), ('limit', 'int')]
        # offset and limit for variants
        item_dict = utilities.fetch_request_params(request_dict)
        item_dict['user'] = user
        item_dict['item_id'] = item_id

        item_data = inventory_bll.get_item_details(item_dict)
        data = success_response(item_data)
    except (
            KeyError, ValueError, ItemNotFound,
            InvalidItemDetails, InvalidVariantParameters,
            InvalidVariantDetails, InvalidVariantPropertyParameters,
            InvalidVariantPropertyDetails) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def update_item_details(request, item_id, user=None):
    """For updating item."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['optional_params'] = [
            ('brand_id', 'int'), ('category_id', 'int'),
            ('name', 'str'), ('product_code', 'str')]
        item_dict = utilities.fetch_request_params(request_dict)
        item_dict['user'] = user
        item_dict['item_id'] = item_id

        item_data = inventory_bll.update_item_details(item_dict)
        data = success_response(item_data)
    except (
            KeyError, ValueError, ItemNotFound,
            InvalidItemParameters, BrandNotFound, CategoryNotFound) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def delete_item(request, item_id, user=None):
    """For deleting item."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        item_dict = utilities.fetch_request_params(request_dict)
        item_dict['user'] = user
        item_dict['item_id'] = item_id

        item_data = inventory_bll.delete_item(item_dict)
        data = success_response(item_data)
    except (
            KeyError, ValueError, ItemNotFound,
            InvalidItemParameters) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def create_item_variant(request, item_id, user=None):
    """For creating item variant."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['mandatory_params'] = [
            ('name', 'str'), ('cost_price', 'str'), ('selling_price', 'str'),
            ('quantity', 'str'), ('variant_properties', 'list')]
        item_dict = utilities.fetch_request_params(request_dict)
        item_dict['user'] = user
        item_dict['item_id'] = item_id

        item_data = inventory_bll.create_item_variants(item_dict)
        data = success_response(item_data)
    except (
            KeyError, ValueError, ItemNotFound,
            InvalidVariantParameters, InvalidVariantPropertyParameters,
            PropertyNotFound) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def update_variant_details(request, variant_id, user=None):
    """For updating variant."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['optional_params'] = [
            ('name', 'str'), ('cost_price', 'str'), ('selling_price', 'str'),
            ('quantity', 'str'), ('variant_properties', 'list')]
        variant_dict = utilities.fetch_request_params(request_dict)
        variant_dict['user'] = user
        variant_dict['variant_id'] = variant_id

        variant_data = inventory_bll.update_variants(variant_dict)
        data = success_response(variant_data)
    except (
            KeyError, ValueError, VariantNotFound,
            InvalidVariantParameters) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def delete_variant(request, variant_id, user=None):
    """For deleting variant."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        variant_dict = utilities.fetch_request_params(request_dict)
        variant_dict['user'] = user
        variant_dict['variant_id'] = variant_id

        variant_data = inventory_bll.delete_variant(variant_dict)
        data = success_response(variant_data)
    except (
            KeyError, ValueError, VariantNotFound,
            InvalidVariantParameters) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def create_variant_properties(request, variant_id, user=None):
    """For creating item variant."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['mandatory_params'] = [
            ('property_id', 'int'), ('property_value', 'str')]
        variant_dict = utilities.fetch_request_params(request_dict)
        variant_dict['user'] = user
        variant_dict['variant_id'] = variant_id

        variant_data = inventory_bll.create_variant_properties(variant_dict)
        data = success_response(variant_data)
    except (
            KeyError, ValueError, VariantNotFound,
            InvalidVariantPropertyParameters, PropertyNotFound) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def update_variant_property_details(request, variant_property_id, user=None):
    """For updating variant property."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        request_dict['optional_params'] = [
            ('property_id', 'int'), ('property_value', 'str')]
        variant_dict = utilities.fetch_request_params(request_dict)
        variant_dict['user'] = user
        variant_dict['variant_property_id'] = variant_property_id

        variant_data = inventory_bll.update_variant_property_details(
            variant_dict)
        data = success_response(variant_data)
    except (
            KeyError, ValueError, VariantPropertyNotFound,
            InvalidVariantPropertyParameters, PropertyNotFound) as e:
        data = error_response(e)
    return data


@csrf_exempt
@authenticate_user
def delete_variant_property(request, variant_property_id, user=None):
    """For deleting variant."""
    request_dict = {}
    try:
        request_dict['received_data'] = loads(request.body)
        variant_property_dict = utilities.fetch_request_params(request_dict)
        variant_property_dict['user'] = user
        variant_property_dict['variant_property_id'] = variant_property_id

        variant_property_data = inventory_bll.delete_variant_property(
            variant_property_dict)
        data = success_response(variant_property_data)
    except (
            KeyError, ValueError, VariantPropertyNotFound,
            InvalidItemParameters) as e:
        data = error_response(e)
    return data


@authenticate_user
def get_user_actions(request, user=None):
    """For deleting variant."""
    request_dict = {}
    try:
        request_dict['received_data'] = request.GET
        request_dict['optional_params'] = [
            ('log_date', 'date')]
        user_dict = utilities.fetch_request_params(request_dict)
        user_dict['user'] = user

        user_data = inventory_bll.get_user_actions(user_dict)
        data = success_response(user_data)
    except (
            KeyError, ValueError, InvalidUserActionParameters) as e:
        data = error_response(e)
    return data


@authenticate_user
def get_properties(request, user=None):
    """For getting all properties."""
    request_dict = {}
    try:
        request_dict['received_data'] = request.GET
        property_dict = utilities.fetch_request_params(request_dict)

        property_data = inventory_bll.get_property_data(property_dict)
        data = success_response(property_data)
    except (KeyError, ValueError) as e:
        data = error_response(e)

    return data
