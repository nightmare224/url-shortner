from dbmodel import db, url_mapper

def base62_encode(url_id) -> str:
    base62_values = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base = 62
    short_url_id = ""
    while url_id > 0:
        r = url_id % base
        short_url_id = base62_values[r] + short_url_id
        url_id //= base

    return short_url_id if short_url_id else base62_values[0]

def base62_decode(short_url_id) -> int:
    base62_values = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base = 62
    url_id = 0
    for i, letter in enumerate(short_url_id[::-1]):
        val = base62_values.index(letter)
        url_id = url_id + val * base**i

    return url_id


def query_next_unique_id() -> int:
    result = db.session.query(url_mapper.url_id).all()
    id_set = set([id[0] for id in result])
    id_next = 0
    for i in range(len(id_set)):
        if id_next not in id_set:
            break
        else:
            id_next += 1
    return id_next
