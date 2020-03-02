from marshmallow import fields, EXCLUDE
from flask_marshmallow import Marshmallow
from .models import Movie


ma = Marshmallow()


def configure(app):
    ma.init_app(app)


class MovieSchema(ma.ModelSchema):
    class Meta:
        model = Movie
        unknow = EXCLUDE

    title = fields.Str(required=True)
