import os
from sqlalchemy.sql import func
from dbmodel import db, url_mapper, url_mapper_schema, url_user_mapper
from sqlalchemy.orm.exc import UnmappedInstanceError
from model.error import InternalServer
from lib.shortener import base62_encode, base62_decode, query_next_unique_id


def create_short_url(full_url, user_id) -> dict:
    """
    Function to create a new record in database for any new URL

    parameters:
        full_url: complete url including http or https as well

    returns:
        json response with following details:
        url_id : unique primary key [highest int]
        short_url_id : new generated short url [without domain]
        short_base_url : Base url [domain name] for short url
        full_url : full url which was passed as input
    """
    short_base_url = os.environ.get("BASE_URL_FOR_SHORT_URL")
    next_unique_id = query_next_unique_id(full_url)
    short_url_id = base62_encode(url_id=next_unique_id)
    # add url mapping
    new_url = url_mapper(
        url_id=next_unique_id,
        short_url_id=short_url_id,
        short_base_url=short_base_url,
        full_url=full_url,
    )
    db.session.add(new_url)
    # add user and url mapping
    new_url_user = url_user_mapper(url_id=next_unique_id, user_id=user_id)
    db.session.add(new_url_user)
    db.session.commit()

    return url_mapper_schema.dump(new_url)


def update_full_url(short_url_id, full_url):
    url_map = url_mapper.query.filter_by(short_url_id=short_url_id).first()
    if url_map is None:
        raise UnmappedInstanceError(f"No row found with short_url_id={short_url_id}")
    url_map.full_url = full_url
    db.session.commit()
    return short_url_id


def delete_short_url(short_url_id) -> str:
    """
    To delete the mapping of short url
    parameter:
        short_url_id : short ur id which is without the domain name [base url]
    returns:
        short url id
    """
    url_id = base62_decode(short_url_id=short_url_id)
    to_delete = url_mapper.query.get(url_id)
    db.session.delete(to_delete)
    db.session.commit()
    return short_url_id


def is_full_url_not_found(full_url, user_id) -> bool:
    not_found = False
    count = (
        db.session.query(func.count(url_user_mapper.url_id))
        .filter_by(user_id=user_id)
        .join(url_mapper, url_user_mapper.url_id == url_mapper.url_id)
        .filter(url_mapper.full_url == full_url)
        .scalar()
    )
    if count < 1:
        not_found = True
    return not_found


def is_short_url_id_not_found(short_url_id, user_id) -> bool:
    not_found = False
    count = (
        db.session.query(func.count(url_user_mapper.url_id))
        .filter_by(user_id=user_id)
        .join(url_mapper, url_user_mapper.url_id == url_mapper.url_id)
        .filter(url_mapper.short_url_id == short_url_id)
        .scalar()
    )
    if count < 1:
        not_found = True
    return not_found


def query_url_mapping(*args, short_url_id=None, full_url=None, user_id=None):
    statement = db.session.query(url_mapper.url_id)
    if user_id is not None:
        statement = (
            db.session.query(url_user_mapper.url_id)
            .filter_by(user_id=user_id)
            .join(url_mapper, url_user_mapper.url_id == url_mapper.url_id)
        )

    url_id = None
    if args:
        raise InternalServer("Provide short_url_id or full_url to get url_mapping")
    elif short_url_id:
        url_id = statement.filter(url_mapper.short_url_id == short_url_id).scalar()
        if url_id is None:
            return None
            # raise InternalServer("short_url_id not found in database.")
    elif full_url:
        url_id = statement.filter(url_mapper.full_url == full_url).scalar()
        if url_id is None:
            return None
            # raise InternalServer("short_url_id not found in database.")

    if url_id is not None:
        url_map = url_mapper.query.get(url_id)
        result = url_mapper_schema.dump(url_map)
    # get all result if not provide variable
    else:
        result = []
        url_id_list = statement.all()
        for url_id in url_id_list:
            url_map = url_mapper.query.get(url_id)
            result.append(url_mapper_schema.dump(url_map))

    return result
