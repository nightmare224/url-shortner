class BadRequest(Exception):
    status_code = 400
    def __init__(self, message=None):
        super().__init__()
        self.payload = {
            "error": str(message) if message else "400 Bad Request."
        }

class NotFound(Exception):
    status_code = 404
    def __init__(self, message=None):
        super().__init__()
        self.payload = {
            "error": str(message) if message else "404 Not Found."
        }

class InternalServer(Exception):
    status_code = 500
    def __init__(self, message=None):
        super().__init__()
        self.payload = {
            "error": str(message) if message else "500 Interal Server Error."
        }