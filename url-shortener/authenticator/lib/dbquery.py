from dbmodel import db, user_info, UserInfoSchema


def is_user_exist(username) -> bool:
    result = db.session.query(user_info).filter_by(username=username).scalar()

    return False if result is None else True


def add_user(username, password) -> str:
    user = user_info(username=username, password=password)
    db.session.add(user)
    db.session.commit()

def update_user_password(username, new_password) -> str:
    db.session.query(user_info).filter_by(username=username).update(
        {
            "password": new_password
        }
    )
    db.session.commit()

def query_user_info(username):
    user_id = db.session.query(user_info.user_id).filter_by(username=username).scalar()
    if user_id is None:
        return None

    data = user_info.query.get(user_id)
    
    return UserInfoSchema().dump(data)


def authenticate_user(username, password) -> bool:
    result = (
        db.session.query(user_info)
        .filter_by(username=username, password=password)
        .scalar()
    )

    return False if result is None else True
