from flask import jsonify
from sqlalchemy.sql import func

from dbmodel import db, URL_MAPPER, UrlMapperSchema


def createShortURL(fullUrl):
    nextUniqueId = getNextuniqueId()
    Short_url_id = generateShortId(nextUniqueId)
    newUrl = URL_MAPPER(
        URL_ID=nextUniqueId, SHORT_URL_ID=Short_url_id, FULL_URL=fullUrl
    )
    db.session.add(newUrl)
    db.session.commit()
    return UrlMapperSchema.jsonify(newUrl)


def getNextuniqueId():
    id = URL_MAPPER.query(func.max(URL_MAPPER.URL_ID)).all()
    return id + 1


def generateShortId(UrlId):
    BASE_62_VALUES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortUrlId = ""
    base = 62
    while UrlId > 0:
        r = UrlId % base
        shortUrlId += BASE_62_VALUES[r]
        UrlId //= base
    return shortUrlId[len(shortUrlId) :: -1]


def getUrlFromId(ShortUrlId):
    UrlId = getShortUrlIdToUrlId(ShortUrlId)
    urlMap = URL_MAPPER.query.get(UrlId)
    result = UrlMapperSchema.dump(urlMap)
    return jsonify(result)


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
