"""Dal for inventory app."""
from uuid import uuid4
import datetime

from .models import Customuser
from .models import Brand
from .models import Category
from .models import Item
from .models import Property
from .models import Action
from .models import Variant
from .models import VariantProperty

from .exceptions import BrandNotFound
from .exceptions import CategoryNotFound
from .exceptions import InvalidItemParameters
from .exceptions import UnauthorizedEmail
from .exceptions import InvalidUserParameters
from .exceptions import UserNotFound
from .exceptions import InvalidUserActionParameters
from .exceptions import ItemNotFound
from .exceptions import InvalidVariantParameters
from .exceptions import InvalidVariantPropertyParameters
from .exceptions import VariantNotFound
from .exceptions import PropertyNotFound
from .exceptions import VariantPropertyNotFound

from .models import db


def create_user(user_dict):
    """For creating new user object."""
    try:
        user = Customuser(
            first_name=user_dict['first_name'],
            last_name=user_dict['last_name'],
            email=user_dict['email'],
            password=user_dict['password'])
        generate_user_access_token(user)
        db.session.add(user)
        db.session.commit()
    except:
        raise InvalidUserParameters

    return user


def validate_user(user_dict):
    """For getting user by email."""
    try:
        user = Customuser.query.filter_by(
            email=user_dict['email'],
            password=user_dict['password']).one()
    except:
        raise UnauthorizedEmail

    return user


def get_user_by_id(id):
    """For getting user by id."""
    try:
        user = Customuser.objects.get(id=id)
    except:
        raise UserNotFound

    return user


def generate_user_access_token(user):
    """For generating user access token."""
    user.access_token = uuid4().hex


def get_all_brands():
    """For getting all item brand objects."""
    brands = Brand.query.all()

    return brands


def get_brand_by_id(id):
    """For getting brand by id."""
    try:
        brand = Brand.query.get(id)
    except:
        raise BrandNotFound

    return brand


def get_all_categories():
    """For getting all item categories objects."""
    categories = Category.query.all()

    return categories


def get_category_by_id(id):
    """For getting category by id."""
    try:
        category = Category.query.get(id)
    except:
        raise CategoryNotFound

    return category


def create_user_action(action_dict):
    """For creating user actions."""
    try:
        actor = action_dict['user'].first_name + action_dict['user'].last_name
        user_action = Action(
            actor=actor,
            action=action_dict['action'],
            status=action_dict['status'],
            edited_time=datetime.datetime.today())
        db.session.add(user_action)
        db.session.commit()
    except:
        raise InvalidUserActionParameters

    return user_action


def create_item_obj(item_dict):
    """For creating item object."""
    try:
        item = Item(
            brand=item_dict['brand'],
            category=item_dict['category'],
            name=item_dict['name'],
            product_code=item_dict['product_code'])
        # item.save()
        db.session.add(item)
        db.session.commit()
    except:
        raise InvalidItemParameters

    return item


def get_all_items():
    """For getting all items."""
    items = Item.query.all()

    return items


def get_item_by_id(id):
    """For getting item by id."""
    try:
        item = Item.query.get(id)
    except:
        raise ItemNotFound

    return item


def update_item_data(item_dict):
    """For updating item data."""
    item = item_dict['item']
    try:
        if 'brand_id' in item_dict.keys():
            brand = get_brand_by_id(item_dict['brand_id'])
            item.brand = brand
            item_dict['action'] += 'brand'
            db.session.add(item)
        if 'category_id' in item_dict.keys():
            category = get_category_by_id(item_dict['category_id'])
            item.category = category
            item_dict['action'] += ', category'
            db.session.add(item)
        if 'name' in item_dict.keys():
            item.name = item_dict['name']
            item_dict['action'] += ', name'
            db.session.add(item)
        if 'product_code' in item_dict.keys():
            item.product_code = item_dict['product_code']
            item_dict['action'] += ', product_code'
            db.session.add(item)
        db.session.commit()
    except:
        raise InvalidItemParameters
    item_dict['action'] += 'of item' + item.name

    return item_dict


def delete_item_obj(item):
    """For deleting item object."""
    try:
        db.session.delete(item)
        db.session.commit()
    except:
        raise InvalidItemParameters

    return {'success': True}


def create_variant_object(variant_dict):
    """For creating variant object."""
    try:
        variant = Variant(
            item=variant_dict['item'],
            name=variant_dict['name'],
            selling_price=variant_dict['selling_price'],
            cost_price=variant_dict['cost_price'],
            quantity=variant_dict['quantity'])
        db.session.add(variant)
        db.session.commit()
    except:
        raise InvalidVariantParameters

    return variant


def filter_variants_by_item(item):
    """For filtering variants by item."""
    try:
        variants = Variant.query.filter_by(item=item)
    except:
        raise InvalidVariantParameters

    return variants


def get_variant_by_id(id):
    """For getting variant by id."""
    try:
        variant = Variant.query.get(id)
    except:
        raise VariantNotFound

    return variant


def update_variant_obj(variant_dict):
    """For updating variant data."""
    variant = variant_dict['variant']

    try:
        if 'name' in variant_dict.keys():
            variant.name = variant_dict['name']
            db.session.add(variant)
        if 'cost_price' in variant_dict.keys():
            variant.cost_price = variant_dict['cost_price']
            db.session.add(variant)
        if 'selling_price' in variant_dict.keys():
            variant.selling_price = variant_dict['selling_price']
            db.session.add(variant)
        if 'quantity' in variant_dict.keys():
            variant.quantity = variant_dict['quantity']
            db.session.add(variant)
        db.session.commit()
    except:
        raise InvalidVariantParameters

    return {'variant': variant}


def delete_variant_obj(variant):
    """For deleting variant object."""
    try:
        db.session.delete(variant)
        db.session.commit()
    except:
        raise InvalidVariantParameters

    return {'success': True}


def get_property_by_id(id):
    """For getting property by id."""
    try:
        property_obj = Property.query.get(id)
    except:
        raise PropertyNotFound

    return property_obj


def create_variant_property_object(variant_property_dict):
    """For creating variant property object."""
    try:
        variant_property = VariantProperty(
            variant=variant_property_dict['variant'],
            property=variant_property_dict['property'],
            property_value=variant_property_dict['property_value'])
        db.session.add(variant_property)
        db.session.commit()
    except:
        raise InvalidVariantPropertyParameters

    return variant_property


def filter_variant_properties_by_variant(variant):
    """For filtering variant properties by variant."""
    try:
        variant_properties = VariantProperty.query.filter_by(variant=variant)
    except:
        raise InvalidVariantPropertyParameters

    return variant_properties


def get_variant_property_by_id(id):
    """For getting variant property by id."""
    try:
        variant_property = VariantProperty.query.get(id)
    except:
        raise VariantPropertyNotFound

    return variant_property


def update_variant_property_data(variant_dict):
    """For updating variant property data."""
    variant_property = variant_dict['variant_property']

    try:
        if 'property_value' in variant_dict.keys():
            variant_property.property_value = variant_dict['property_value']
            db.session.add(variant_property)
        if 'property_id' in variant_dict.keys():
            property_obj = get_property_by_id(variant_dict['property_id'])
            variant_property.property = property_obj
            db.session.add(variant_property)
        db.session.commit()
    except:
        raise InvalidVariantPropertyParameters

    return {'variant_property': variant_property.id}


def delete_variant_property_obj(variant_property):
    """For deleting variant object."""
    try:
        db.session.delete(variant_property)
        db.session.commit()
    except:
        raise InvalidVariantPropertyParameters

    return {'success': True}


def filter_user_actions(user_dict):
    """For filtering user actions."""
    try:
        user_actions = Action.query.all()
    except:
        raise InvalidUserActionParameters

    return user_actions
