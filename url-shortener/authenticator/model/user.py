from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str

@dataclass
class UserPwd(User):
    new_password: str