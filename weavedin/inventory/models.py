"""Models for inventory app."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# from .constants import USER_ACTION_STATUS_CHOICES

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://weavedinadmin:admin@weavedin@localhost/weavedin'
db = SQLAlchemy(app)


class Customuser(db.Model):
    """Class for storing user data."""

    # __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    access_token = db.Column(db.String(100))


class Action(db.Model):
    """Class for storing user variant log."""

    id = db.Column(db.Integer, primary_key=True)
    actor = db.Column(db.String(20))
    action = db.Column(db.String(500))
    status = db.Column(db.String(20))
    edited_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # def __repr__(self):
    #     """For representing the object."""
    #     return "<User(fullname='%s', password='%s')>" % (
    #         self.first_name, self.password)


class Brand(db.Model):
    """Class representing for storing brand data."""

    # __tablename__ = "brand"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Category(db.Model):
    """Class for storing item category."""

    # __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Item(db.Model):
    """Class representing data in item."""

    # __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False)
    product_code = db.Column(db.String(100))

    brand = db.relationship('Brand')
    category = db.relationship('Category')


class Property(db.Model):
    """Class for storing properties."""

    # __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Variant(db.Model):
    """Class for storing variant data."""

    # __tablename__ = "variant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    item_id = db.Column(
        db.Integer, db.ForeignKey("item.id", ondelete='CASCADE'),
        nullable=False)
    selling_price = db.Column(db.String(20))
    cost_price = db.Column(db.String(20))
    quantity = db.Column(db.String(20))

    item = db.relationship('Item')


class VariantProperty(db.Model):
    """Class representing for storing data of variant properties."""

    # __tablename__ = "variantproperty"

    id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(
        db.Integer, db.ForeignKey("variant.id"), nullable=False)
    property_id = db.Column(
        db.Integer, db.ForeignKey("property.id"), nullable=False)
    property_value = db.Column(db.String(20))

    variant = db.relationship('Variant')
    property = db.relationship('Property')
