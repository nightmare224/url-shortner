import re
from marshmallow import (
    Schema,
    fields,
    pre_load,
    post_load,
    validates_schema,
    ValidationError,
)
from model.url import URL

class URLSchema(Schema):
    url = fields.String()
    # url = fields.Url() # do the URL validation

    @validates_schema
    def validate_url(self, data, **kwargs):
        url = data["url"]
        result = re.match(
            r"^([a-z]+)://([a-z0-9\-\.]+)(:\d+)?(/[^ \t\n\r\f\v?]*)*(\?\S*)?$", url
        )
        if result is None:
            raise ValidationError("Invalid URL")
        scheme = result.group(1)
        host = result.group(2)
        port = result.group(3)
        path = result.group(4)
        query = result.group(5)

        # scheme
        if scheme not in ["http", "https", "ftp"]:
            raise ValidationError("Invalid URL")

        # host
        labels = host.split(".")
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

        # url after sanitize
        data["url"] = f"{scheme}://{host}{port_sanitize}{path_sanitize}{query_sanitize}"

    @pre_load
    def uncapital_url(self, data, **kwargs):
        data["url"] = data["url"].lower()
        return data

    # deserialization
    @post_load
    def __post_load__(self, data, **kwargs):
        return URL(**data)
