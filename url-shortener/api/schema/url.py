from re import match
from marshmallow import (
    Schema,
    fields,
    post_load,
    validates_schema,
    ValidationError,
)
from model.url import FullURL, URL
from schema.shorturl import ShortURLSchema
from urllib.parse import urlparse, urlunparse

class FullURLSchema(Schema):
    full_url = fields.String()
    # full_url = fields.Url() # do the URL validation

    @validates_schema
    def validate_url(self, data, **kwargs):
        try:
            uni_url = urlparse(data["full_url"])
            uni_scheme = uni_url.scheme
            uni_host = uni_url.hostname
            uni_port = uni_url.port
            uni_path = uni_url.path
            uni_query = uni_url.query
            uni_fragment = uni_url.fragment
            
            ascii_url = urlparse(data["full_url"])
            ascii_url = ascii_url._replace(netloc=ascii_url.netloc.encode('idna').decode('ascii'))
            ascii_url = urlunparse(ascii_url)
        except UnicodeError:
            raise ValidationError("Invalid URL")
        
        result = match(
            r"^([a-zA-Z][a-zA-Z\d\+\-\.]*)://([a-zA-Z0-9\-\.]+)(:\d+)?(/[^\s\?#]*)*(\?[^\s#]*)*?(#\S*)*$",
            ascii_url
        )
        if result is None:
            raise ValidationError("Invalid URL")
        ascii_scheme = result.group(1)
        ascii_host = result.group(2)
        ascii_port = result.group(3)
        ascii_path = result.group(4)
        ascii_query = result.group(5)
        ascii_fragment = result.group(6)

        # scheme
        scheme_sanitize = uni_scheme.lower()
        if ascii_scheme.lower() not in ["http", "https", "ftp"]:
            raise ValidationError("Invalid URL")

        # host
        host_sanitize = uni_host.lower()
        labels = ascii_host.lower().split(".")
        for label in labels:
            if label:
                # not start and end with -
                if match("^([^\-].*[^\-])|([^\-])$", label) is None:
                    raise ValidationError("Invalid URL")
            else:
                raise ValidationError("Invalid URL")

        # port
        port_sanitize = f":{uni_port}" if ascii_port else ""

        # path
        path = uni_path if ascii_path else ""
        path_sanitize = ""
        for i in path.split("/"):
            if i:
                path_sanitize += f"/{i}"  

        # query
        # if "?" don't have following string, "?" would be clear
        query_sanitize = ""
        if ascii_query:
            if len(ascii_query) > 1:
                query_sanitize = f"?{uni_query}"

        fragment_santize = ""
        if ascii_fragment:
            if len(ascii_fragment) > 1:
                fragment_santize = f"#{uni_fragment}"
        
        # full_url after sanitize
        data["full_url"] = f"{scheme_sanitize}://{host_sanitize}{port_sanitize}{path_sanitize}{query_sanitize}{fragment_santize}"
    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return FullURL(**data)

class URLSchema(ShortURLSchema, FullURLSchema):

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return URL(**data)