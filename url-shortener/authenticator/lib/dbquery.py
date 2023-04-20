from dbmodel import db, user_info


def is_user_exist(username) -> bool:
    result = db.session.query(user_info).filter_by(username=username).scalar()

    return False if result is None else True


def add_user(username, password) -> str:
    user = user_info(username=username, password=password)
    db.session.add(user)
    db.session.commit()


def authenticate_user(username, password) -> bool:
    result = (
        db.session.query(user_info)
        .filter_by(username=username, password=password)
        .scalar()
    )

    return False if result is None else True