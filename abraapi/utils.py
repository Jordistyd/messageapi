import json
from .constants import General, Keys
from django.core.serializers import serialize


def serialize_message(message):
    display_message = serialize(General.JSON, list(message), fields=(Keys.SENDER, Keys.RECEIVER, Keys.SUBJECT,
                                                                     Keys.MESSAGE, Keys.CREATION_DATE,
                                                                     Keys.IS_READ))
    json_message = json.loads(display_message)
    return json_message
