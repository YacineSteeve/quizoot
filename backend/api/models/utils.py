import uuid
from typing import Any, Union

from django.core.exceptions import ValidationError

ID_LENGTH = 12


def generate_id() -> str:
    default_uuid_length = 32
    n_drop = (default_uuid_length - ID_LENGTH) // 2

    return uuid.uuid4().hex[n_drop : (n_drop + ID_LENGTH)]


def validate_id(
    id_value: Any, existing_ids: list, object_type: str
) -> Union[None, ValidationError]:
    if id_value == "" or id_value not in [None, *existing_ids]:
        raise ValidationError(
            f"Invalid {object_type.title()} Id. "
            f"Make sure an object {object_type.title()} with '{id_value}' as Id exists."
        )
    else:
        return
