from infographs.models import AspectRatio, Resolution
from marshmallow import Schema, fields, validate


class InfographCreateSchema(Schema):
    prompt = fields.Str(required=True)
    blog_url = fields.URL(required=False, allow_none=True, validate=validate.URL())
    aspect_ratio = fields.Str(required=True, validate=validate.OneOf([choice[0] for choice in AspectRatio.choices]))
    resolution = fields.Str(required=True, validate=validate.OneOf([choice[0] for choice in Resolution.choices]))
    number_of_infographs = fields.Int(required=True)

    class Meta:
        fields = ['prompt', 'blog_url', 'aspect_ratio', 'resolution', 'number_of_infographs']