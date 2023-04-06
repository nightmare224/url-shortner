from flask import jsonify
from sqlalchemy.sql import func

from dbmodel import db, url_mapper, url_mapper_schema


def create_short_url(full_url) -> dict:
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
    BASE_URL_FOR_SHORT_URL = "https://snv.io"
    next_unique_id = query_next_unique_id()
    short_url_id = base62_encode(url_id=next_unique_id)
    new_url = url_mapper(
        url_id=next_unique_id,
        short_url_id=short_url_id,
        short_base_url=BASE_URL_FOR_SHORT_URL,
        full_url=full_url,
    )
    db.session.add(new_url)
    db.session.commit()
    return url_mapper_schema.dump(new_url)


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

def query_full_url(short_url_id) -> str:
    """
    To get the full URL from provided short url
    parameter:
        short_url_id : short ur id which is without the domain name [base url]
    returns:
        full url with http protocol as well.
    """
    url_id = base62_decode(short_url_id=short_url_id)
    url_map = url_mapper.query.get(url_id)
    if url_map is not None:
        result = url_mapper_schema.dump(url_map)
        baseUrl = result["short_base_url"]
        short_url_id = result["short_url_id"]
        short_url = baseUrl + "/" + short_url_id
        return short_url


def base62_encode(url_id) -> str:
    BASE_62_VALUES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_url_id = ""
    base = 62
    while url_id > 0:
        r = url_id % base
        short_url_id += BASE_62_VALUES[r]
        url_id //= base
    return short_url_id[len(short_url_id) :: -1]


def base62_decode(short_url_id) -> int:
    url_id = 0
    for letter in short_url_id:
        letter_val = ord(letter)
        if letter_val >= ord("a") and letter_val <= ord("z"):
            url_id = url_id * 62 + letter_val - ord("a")
        elif letter_val >= ord("A") and letter_val <= ord("Z"):
            url_id = url_id * 62 + letter_val - ord("A") + 26
        else:
            url_id = url_id * 62 + letter_val - ord("0") + 52
    return url_id


def is_full_url_not_found(full_url) -> bool:
    found = False
    count = (
        db.session.query(func.count(url_mapper.url_id))
        .filter(url_mapper.full_url == full_url)
        .scalar()
    )
    if count < 1:
        found = True
    return found


def query_url_mapping(full_url=None):
    if full_url:
        url_id = db.session.query("*").filter(url_mapper.full_url == full_url).scalar()
        url_map = url_mapper.query.get(url_id)
        result = url_mapper_schema.dump(url_map)
    else:
        #return all if not specify full_url
        result = []
        url_id_list = db.session.query(url_mapper.url_id).all()
        for url_id in url_id_list:
            url_map = url_mapper.query.get(url_id)
            result.append(url_mapper_schema.dump(url_map))

    return result


def query_next_unique_id() -> int:
    id = db.session.query(func.max(url_mapper.url_id)).scalar()
    return id + 1
