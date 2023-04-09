import re
from marshmallow import (
    Schema,
    fields,
    post_load,
    validates_schema,
    ValidationError,
)
from model.url import FullURL, URL
from schema.shorturl import ShortURLSchema

class FullURLSchema(Schema):
    full_url = fields.String()
    # full_url = fields.Url() # do the URL validation

    @validates_schema
    def validate_url(self, data, **kwargs):
        full_url = data["full_url"]
        result = re.match(
            r"^([a-zA-Z]+)://([a-zA-Z0-9\-\.]+)(:\d+)?(/[^ \t\n\r\f\v?]*)*(\?\S*)?$", full_url
        )
        if result is None:
            raise ValidationError("Invalid URL")
        scheme = result.group(1)
        host = result.group(2)
        port = result.group(3)
        path = result.group(4)
        query = result.group(5)

        # scheme
        scheme_sanitize = scheme.lower()
        if scheme not in ["http", "https", "ftp"]:
            raise ValidationError("Invalid URL")

        # host
        host_sanitize = host.lower()
        labels = host_sanitize.split(".")
        for label in labels:
            if label:
                # not start and end with -
                if re.match("^([^\-].*[^\-])|([^\-])$", label) is None:
                    raise ValidationError("Invalid URL")
            else:
                raise ValidationError("Invalid URL")

        # port
        port_sanitize = port if port else ""

        # path
        path = path if path else ""
        path_sanitize = ""
        for i in path.split("/"):
            if i:
                path_sanitize += f"/{i}"

        # query
        # if "?" don't have following string, "?" would be clear
        query_sanitize = ""
        if query:
            if len(query) > 1:
                query_sanitize = query

        # full_url after sanitize
        data["full_url"] = f"{scheme_sanitize}://{host_sanitize}{port_sanitize}{path_sanitize}{query_sanitize}"

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return FullURL(**data)

class URLSchema(ShortURLSchema, FullURLSchema):

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return URL(**data)