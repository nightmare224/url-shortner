from dbmodel import db, UserInfo, UserInfoSchema


def is_user_exist(username) -> bool:
    result = db.session.query(UserInfo).filter_by(username=username).scalar()

    return False if result is None else True


def add_user(username, password) -> str:
    user = UserInfo(username=username, password=password)
    db.session.add(user)
    db.session.commit()

def update_user_password(username, new_password) -> str:
    db.session.query(UserInfo).filter_by(username=username).update(
        {
            "password": new_password
        }
    )
    db.session.commit()

def query_user_info(username):
    user_id = db.session.query(UserInfo.user_id).filter_by(username=username).scalar()
    if user_id is None:
        return None

    data = UserInfo.query.get(user_id)
    
    return UserInfoSchema().dump(data)


def authenticate_user(username, password) -> bool:
    result = (
        db.session.query(UserInfo)
        .filter_by(username=username, password=password)
        .scalar()
    )

    return False if result is None else True
