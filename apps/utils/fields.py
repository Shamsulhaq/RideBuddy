import json
from rest_framework import serializers

from apps.utils.models import (
    TypeValue,
)


class TypeValueItemField(serializers.Field):    
    def to_internal_value(self, data):
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            raise serializers.ValidationError(
                "Invalid JSON format"
            )
        if 'type_value_id' not in json_data or 'items' not in json_data:
            raise serializers.ValidationError(
                "Both 'type_value_id' and 'items' keys are required"
            )
        try:
            type_value_id = int(json_data['type_value_id'])
        except ValueError:
            raise serializers.ValidationError(
                "type_value_id is not valid id"
            )
        try:
            type_value_obj = TypeValue.objects.get(pk=type_value_id)
        except TypeValue.DoesNotExist:
            raise serializers.ValidationError(
                f"Type Value object with id '{type_value_id}' does not exist."
            )
        except Exception as e:
            raise serializers.ValidationError(
                str(e)
            )
        try:
            items = int(json_data["items"])
        except ValueError:
            raise serializers.ValidationError(
                "items is not a valid data"
            )
        if items < 0:
            raise serializers.ValidationError(
                f"items of id: {type_value_id} is less than 0"
            )
        json_data["type_value_id"] = type_value_id
        json_data["items"] = items
        return json_data    

    def to_representation(self, value):
        return json.dumps(value)