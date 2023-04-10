import os
from sqlalchemy.sql import func
from dbmodel import db, url_mapper, url_mapper_schema
from sqlalchemy.orm.exc import UnmappedInstanceError
from model.error import InternalServer

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
    short_base_url = os.environ.get("BASE_URL_FOR_SHORT_URL")
    next_unique_id = query_next_unique_id()
    short_url_id = base62_encode(url_id=next_unique_id)
    new_url = url_mapper(
        url_id=next_unique_id,
        short_url_id=short_url_id,
        short_base_url=short_base_url,
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


# def query_full_url(short_url_id) -> str:
#     """
#     To get the full URL from provided short url
#     parameter:
#         short_url_id : short ur id which is without the domain name [base url]
#     returns:
#         full url with http protocol as well.
#     """
#     url_id = base62_decode(short_url_id=short_url_id)
#     url_map = url_mapper.query.get(url_id)
#     if url_map is not None:
#         result = url_mapper_schema.dump(url_map)
#         short_url = get_short_url(result)
#         full_url = result["full_url"]
#         # TODO : return both short and full url
#         return full_url


def base62_encode(url_id) -> str:
    base62_values = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_url_id = ""
    base = 62
    while url_id > 0:
        r = url_id % base
        short_url_id += base62_values[r]
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

def is_short_url_id_not_found(short_url_id) -> bool:
    not_found = False
    count = (
        db.session.query(func.count(url_mapper.url_id))
        .filter(url_mapper.short_url_id == short_url_id)
        .scalar()
    )
    if count < 1:
        not_found = True
    return not_found

# def query_url_mapping(full_url=None):
#     if full_url:
#         url_id = db.session.query("*").filter(url_mapper.full_url == full_url).scalar()
#         url_map = url_mapper.query.get(url_id)
#         result = url_mapper_schema.dump(url_map)
#     else:
#         # return all if not specify full_url
#         result = []
#         url_id_list = db.session.query(url_mapper.url_id).all()
#         for url_id in url_id_list:
#             url_map = url_mapper.query.get(url_id)
#             result.append(url_mapper_schema.dump(url_map))
#     return result

def query_url_mapping(*args, short_url_id=None, full_url=None):
    url_id = None
    if args:
        raise InternalServer("Provide short_url_id or full_url to get url_mapping")
    elif short_url_id:
        url_id = db.session.query(url_mapper.url_id).filter(url_mapper.short_url_id == short_url_id).scalar()
        if url_id is None:
            raise InternalServer("short_url_id not found in database.")
    elif full_url:
        url_id = db.session.query(url_mapper.url_id).filter(url_mapper.full_url == full_url).scalar()
        if url_id is None:
            raise InternalServer("short_url_id not found in database.")
        
    if url_id:
        url_map = url_mapper.query.get(url_id)
        result = url_mapper_schema.dump(url_map)
    # get all result if not provide variable
    else:
        result = []
        url_id_list = db.session.query(url_mapper.url_id).all()
        for url_id in url_id_list:
            url_map = url_mapper.query.get(url_id)
            result.append(url_mapper_schema.dump(url_map))

    return result


def query_next_unique_id() -> int:
    result = db.session.query(url_mapper.url_id).all()
    id_set = set([id[0] for id in result])
    id_next = 1
    for i in range(len(id_set)):
        if id_next not in id_set:
            break
        else:
            id_next += 1
    return id_next


def update_full_url(short_url_id, full_url):
    url_map = url_mapper.query.filter_by(short_url_id=short_url_id).first()
    if url_map is None:
        raise UnmappedInstanceError(f"No row found with short_url_id={short_url_id}")
    url_map.full_url = full_url
    db.session.commit()
    return short_url_id


def get_short_url(url_mapper_dump) -> str:
    baseUrl = url_mapper_dump["short_base_url"]
    baseUrl = clean_base_url(baseUrl)
    short_url_id = url_mapper_dump["short_url_id"]
    short_url = baseUrl + "/" + short_url_id
    return short_url


def clean_base_url(base_url) -> str:
    base_url.strip("/")
    base_url.strip(".")
    return base_url
