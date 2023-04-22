from dbmodel import db, url_mapper
from uuid import uuid5, NAMESPACE_URL

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


def query_next_unique_id(full_url) -> int:
    def get_final_id(init_id, digit):
        init_id = str(init_id)
        final_id = ""
        while digit > 0:
            this_round_digit = len(init_id) if len(init_id) < digit else digit
            final_id += init_id[:this_round_digit]
            digit -= this_round_digit
        return int(final_id)
    
    digit = 1
    init_id = uuid5(NAMESPACE_URL, full_url).int
    final_id = get_final_id(init_id, digit)
    result = db.session.query(url_mapper.url_id).all()
    id_set = set([id[0] for id in result])
    while final_id in id_set:
        digit += 1
        final_id = get_final_id(init_id, digit)
    return final_id
