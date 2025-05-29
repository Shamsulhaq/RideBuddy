import datetime
from io import BytesIO
from PIL import Image
from rest_framework import serializers
from apps.utils.models import (
    TypeValue,
)
from apps.utils.choices import (
    TypeGroupName,
)
from apps.utils.serializers import (
    TypeValueSerializer,
)

def qs_for_admin_or_user(qs, user):
    if user.is_authenticated and user.is_admin:
        return qs.filter(is_deleted=False)
    else:
        return qs.filter(is_active=True, is_deleted=False)

def get_serialized_type_values_data(type_name, user):
    qs = TypeValue.objects.filter(group__name=type_name)
    qs = qs_for_admin_or_user(qs, user)
    return TypeValueSerializer(qs, many=True).data

def validate_type_value_field(pk, group_name):
    if isinstance(pk, TypeValue):
        pk = pk.pk
    if pk is not None:
        try:
            obj = TypeValue.objects.get(pk=pk, group__name=group_name)
            return (obj, obj.pk)
        except TypeValue.DoesNotExist:
            raise serializers.ValidationError(
                f"{group_name.replace('-', ' ').lower()} id: {pk} does not exist."
            )
    return (None, None)

def validate_type_value_group(value, group_name):
    validated_pk = []
    if value is not None and value != []:
        for pk in value:
            obj, obj_pk = validate_type_value_field(pk=pk, group_name=group_name)
            if obj is None:
                raise serializers.ValidationError(
                    f"{group_name.replace('-', ' ').lower()} id: {pk} does not exist."
                )
            validated_pk.append(obj_pk)
    return (value, validated_pk)

def validate_type_value_items_group(value, group_name):
    validated_data = []
    if value is not None and value != []:
        for pk in value:
            obj, obj_pk = validate_type_value_field(pk=pk, group_name=group_name)
            if obj is None:
                raise serializers.ValidationError(
                    f"{group_name.replace('-', ' ').lower()} id: {pk} does not exist."
                )
            validated_data.append(obj_pk)
    return validated_data



def validate_image(file, height=None, width=None, size_in_mb=None, file_format=[], hw_lookup="exact"):
    """
    Validates an image file against various parameters such as dimensions, size, and format.

    :param file: The image file to validate
    :param height: Minimum or exact height for the image (int)
    :param width: Minimum or exact width for the image (int)
    :param size_in_mb: Maximum size of the image in MB
    :param file_format: The required file format (e.g., 'JPEG', 'PNG')
    :param hw_lookup: How to compare height and width; one of 'exact', 'min', 'max'
    :return: The validated image file or raises ValidationError if validation fails
    """
    # Check if the file is a valid image
    try:
        image = Image.open(file)
        image.verify()  # Verifies that it's an actual image (no corrupt files)
    except Exception:
        raise serializers.ValidationError("The uploaded file is not a valid image.")

    # Check if the image has the correct format (if provided)
    if file_format != []:
        file_format = [f.lower() for f in file_format]
        if image.format.lower() not in file_format:
            raise serializers.ValidationError(f"The image must be in {file_format} format.")

    # Check the dimensions (height and width)
    img_width, img_height = image.size
    if height and hw_lookup == "exact" and img_height != height:
        raise serializers.ValidationError(f"The image height must be exactly {height} pixels.")
    elif width and hw_lookup == "exact" and img_width != width:
        raise serializers.ValidationError(f"The image width must be exactly {width} pixels.")
    elif height and hw_lookup == "min" and img_height < height:
        raise serializers.ValidationError(f"The image height must be at least {height} pixels.")
    elif width and hw_lookup == "min" and img_width < width:
        raise serializers.ValidationError(f"The image width must be at least {width} pixels.")
    elif height and hw_lookup == "max" and img_height > height:
        raise serializers.ValidationError(f"The image height must be no more than {height} pixels.")
    elif width and hw_lookup == "max" and img_width > width:
        raise serializers.ValidationError(f"The image width must be no more than {width} pixels.")

    # Check the file size (in MB)
    if size_in_mb:
        file.seek(0, os.SEEK_END)  # Move to the end of the file
        file_size = file.tell() / (1024 * 1024)  # File size in MB
        if file_size > size_in_mb:
            raise serializers.ValidationError(f"The image size must be no larger than {size_in_mb}MB.")

    return file


def add_error_in_dict(dict_obj, field_name, error_message, is_flat=False):
    if is_flat:
        dict_obj[field_name] = error_message
    else:
        if field_name in dict_obj:
            dict_obj[field_name].append(error_message)
        else:
            dict_obj[field_name] = [error_message]    


def get_missed__field_values_from_request(request,  field_name, data_dict_name):
    """
    utility function to get data from nested serializer fields;
    request: request object, 
    field_name: field name of what we need data, 
    data_dict_name: usually the nested serializer field name  > 
    
    returns list of field values
    """
    if not request:
        return []

    content_type = request.content_type
    remove_ids = []

    if content_type.startswith('application/json'):
        # JSON: nested structure
        remove_ids = request.data.get(data_dict_name, {}).get(field_name, [])

    elif content_type.startswith('multipart/form-data'):
        key = f'{data_dict_name}.{field_name}'
        if key in request.data:
            try:
                # getlist works if multiple keys sent: financial.remove_transaction_type=1, financial.remove_transaction_type=2
                remove_ids = request.data.getlist(key)
            except AttributeError:
                # fallback: possibly comma-separated or single value
                raw_value = request.data.get(key)
                if raw_value:
                    if isinstance(raw_value, str):
                        remove_ids = [v.strip() for v in raw_value.split(',')]
                    else:
                        remove_ids = [raw_value]

    # Final clean-up: convert to int, ignore invalid
    try:
        return [int(pk) for pk in remove_ids if pk]
    except (ValueError, TypeError):
        return []
