from flask import jsonify
from sqlalchemy.sql import func

from dbmodel import db, url_mapper, url_mapper_schema


def createShortURL(fullUrl):
    """
    Function to create a new record in database for any new URL

    parameters:
        fullUrl: complete url including http or https as well

    returns:
        json response with following details:
        url_id : unique primary key [highest int]
        short_url_id : new generated short url [without domain]
        short_base_url : Base url [domain name] for short url
        full_url : full url which was passed as input

    """
    if isFullUrlNotFound(fullUrl):
        baseUrlForShortUrl = "https://snv.io"
        nextUniqueId = getNextuniqueId()
        short_url_id = generateShortId(nextUniqueId)
        newUrl = url_mapper(
            url_id=nextUniqueId,
            short_url_id=short_url_id,
            short_base_url=baseUrlForShortUrl,
            full_url=fullUrl,
        )
        db.session.add(newUrl)
        db.session.commit()
        return url_mapper_schema.jsonify(newUrl)
    else:
        result = getUrlMappingForFullUrl(fullUrl)
        return jsonify(result)


def getFullUrlFromShortUrl(ShortUrlId):
    """
    To get the full URL from provided short url
    parameter:
        ShortUrlId : short ur id which is without the domain name [base url]
    returns:
        full url with http protocol as well.
    """
    UrlId = getShortUrlIdToUrlId(ShortUrlId)
    urlMap = url_mapper.query.get(UrlId)
    if urlMap is not None:
        result = url_mapper_schema.dump(urlMap)
        baseUrl = result["short_base_url"]
        short_url_id = result["short_url_id"]
        short_url = baseUrl + "/" + short_url_id
        return short_url


def deleteShortUrl(ShortUrlId):
    """
    To delete the mapping of short url
    parameter:
        ShortUrlId : short ur id which is without the domain name [base url]
    returns:
        short url id
    """
    UrlId = getShortUrlIdToUrlId(ShortUrlId)
    toDelete = url_mapper.query.get(UrlId)
    db.session.delete(toDelete)
    db.session.commit()
    return ShortUrlId


def generateShortId(UrlId):
    BASE_62_VALUES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortUrlId = ""
    base = 62
    while UrlId > 0:
        r = UrlId % base
        shortUrlId += BASE_62_VALUES[r]
        UrlId //= base
    return shortUrlId[len(shortUrlId) :: -1]


def getShortUrlIdToUrlId(ShortUrlId):
    UrlId = 0
    for letter in ShortUrlId:
        letter_val = ord(letter)
        if letter_val >= ord("a") and letter_val <= ord("z"):
            UrlId = UrlId * 62 + letter_val - ord("a")
        elif letter_val >= ord("A") and letter_val <= ord("Z"):
            UrlId = UrlId * 62 + letter_val - ord("A") + 26
        else:
            UrlId = UrlId * 62 + letter_val - ord("0") + 52
    return UrlId


def isFullUrlNotFound(full_url):
    found = False
    count = (
        db.session.query(func.count(url_mapper.url_id))
        .filter(url_mapper.full_url == full_url)
        .scalar()
    )
    if count < 1:
        found = True
    return found


def getUrlMappingForFullUrl(full_url):
    UrlId = db.session.query("*").filter(url_mapper.full_url == full_url).scalar()
    print(UrlId)
    urlMap = url_mapper.query.get(UrlId)
    result = url_mapper_schema.dump(urlMap)
    return result


def getNextuniqueId():
    id = db.session.query(func.max(url_mapper.url_id)).scalar()
    print(id)
    return id + 1
