from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, Ad, User
from schema import CreateUser, UpdateUser, CreateAd, UpdateAd

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def validate_json(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def get_ad_by_id(ad_id: int):
    ad = request.session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, "adv not found")
    return ad


def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    print('jgggg')
    if user is None:
        raise HttpError(404, "User not found")
    return user


def add_ad(ad: Ad):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "Error of date")


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "User already exists")


class UserView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, user_id):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate_json(CreateUser, request.json)
        user = User(**json_data)
        add_user(user)
        return jsonify({"id": user.id})

    def patch(self, user_id):
        json_data = validate_json(UpdateUser, request.json)
        user = get_user_by_id(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id):
        user = get_user_by_id(user_id)
        #удалить все объявления пользователя
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "deleted"})


user_view = UserView.as_view("user_view")

app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/user/<int:user_id>/", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)


class AdView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, ad_id):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)

    def post(self):
        json_data = validate_json(CreateAd, request.json)
        ad = Ad(**json_data)
        add_ad(ad)
        return jsonify({"id": ad.id})

    def patch(self, ad_id):
        json_data = validate_json(UpdateAd, request.json)
        ad = get_ad_by_id(ad_id)
        for field, value in json_data.items():
            setattr(ad, field, value)
        add_ad(ad)
        return jsonify(ad.dict)

    def delete(self, ad_id):
        ad = get_ad_by_id(ad_id)
        self.session.delete(ad)
        self.session.commit()
        return jsonify({"status": "deleted"})


ad_view = AdView.as_view("ad_view")

app.add_url_rule("/ad/", view_func=ad_view, methods=["POST"])
app.add_url_rule(
    "/ads/<int:ad_id>/", view_func=ad_view, methods=["GET", "PATCH", "DELETE"]
)


if __name__ == "__main__":
    app.run()
