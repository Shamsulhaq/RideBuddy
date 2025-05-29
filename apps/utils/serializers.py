from django.utils import timezone
from rest_framework import serializers
from utils.serializers import CommonFieldSerializer

from .models import Country, Region, City, TypeGroup, TypeValue, License


class CountrySerializer(CommonFieldSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code', 'phone_number_code', 'vat_rate', 'currency') + CommonFieldSerializer.Meta.fields

class CountryShortSerializer(CommonFieldSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code', 'phone_number_code', 'vat_rate', 'currency')
    

class RegionSerializer(CommonFieldSerializer):

    class Meta:
        model = Region
        fields = ('id', 'country', 'name', 'housing_fees') + CommonFieldSerializer.Meta.fields
        # extra_kwargs ={
        #     'country': {'read_only':True}
        # }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["country"] = CountryShortSerializer(instance.country).data
        return ret


class RegionShortSerializer(serializers.ModelSerializer):
    country = CountryShortSerializer(instance=Country.objects.all(), read_only=True)

    class Meta:
        model = Region
        fields = ('id', 'country', 'name', 'housing_fees')


class CitySerializer(CommonFieldSerializer):
    class Meta:
        model = City
        fields = ('id', 'region', 'name') + CommonFieldSerializer.Meta.fields

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["region"] = RegionShortSerializer(instance.region).data
        return ret


class TypeGroupSerializer(CommonFieldSerializer):
    class Meta:
        model = TypeGroup
        fields = ('id', 'name', 'required_field') + CommonFieldSerializer.Meta.fields

    
class TypeGroupShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeGroup
        fields = ('id', 'name', 'required_field')


class TypeValueSerializer(CommonFieldSerializer):
    class Meta:
        model = TypeValue
        fields = ('id', 'name', 'icon', 'percentage', 'group') + CommonFieldSerializer.Meta.fields

    def validate(self, attrs):
        group = attrs.get('group', None)
        icon  = attrs.pop('icon', None)
        percentage = attrs.pop('percentage', None)
        if self.instance is None:
            if group.required_field is not None:
                if group.required_field == 'icon':
                    if icon is None:
                        raise serializers.ValidationError({"required_field": "'icon' is required"})
                    attrs['icon'] = icon
                elif group.required_field == 'percentage':
                    if percentage is None:
                        raise serializers.ValidationError({"required_field": "'percentaged' is required"})
                    attrs['percentage'] = percentage
        else:
            group = group if group is not None else self.instance.group
            icon = icon if icon is not None else self.instance.icon 
            percentage = percentage if percentage is not None else self.instance.percentage
            if group.required_field is not None:
                if group.required_field == 'icon':
                    if icon is None:
                        raise serializers.ValidationError({"required_field": "'icon' is required"})
                    attrs['icon'] = icon
                elif group.required_field == 'percentage':
                    if percentage is None:
                        raise serializers.ValidationError({"required_field": "'percentaged' is required"})
                    attrs['percentage'] = percentage
                
        return super().validate(attrs)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["group"] = TypeGroupShortSerializer(instance.group).data
        return ret


class LicenseSerializer(CommonFieldSerializer):
    class Meta:
        model = License
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["country"] = CountryShortSerializer(instance.country).data
        ret["region"] = RegionShortSerializer(instance.region).data
        ret["license_type"] = TypeValueSerializer(instance.license_type).data
        return ret

class LicenseAsChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ('id', 'name')

