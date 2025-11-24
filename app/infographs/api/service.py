from typing import Optional

from infographs.api.schema import InfographCreateSchema
from infographs.infographs import service as infographs_service
from infographs.infographs.exceptions import NotEnoughCreditsException
from marshmallow import ValidationError

from account.models import Account


def create_infograph(account: Account, prompt: str, blog_url: Optional[str], aspect_ratio: str, resolution: str, number_of_infographs: int, type: str = 'infograph'):
    try:
        validated_data = InfographCreateSchema().load({
            "prompt": prompt,
            "blog_url": blog_url,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "number_of_infographs": number_of_infographs,
            "type": type,
        })

        
        infograph = infographs_service.create_infograph(
            account=account,
            prompt=validated_data["prompt"],
            blog_url=validated_data["blog_url"],
            aspect_ratio=validated_data["aspect_ratio"],
            resolution=validated_data["resolution"],
            number_of_infographs=validated_data["number_of_infographs"],
            type=validated_data["type"],
        )

        return {"message": "Infograph created successfully", "infograph": infograph}
    except NotEnoughCreditsException as e:
        raise ValidationError({"message": "Not enough credits"})
    except ValidationError as e:
        raise ValidationError(e.messages)