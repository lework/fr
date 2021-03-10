# Django Rest Framework
from rest_framework import serializers


class APIVersionHyperlinkedField(serializers.HyperlinkedIdentityField):
    """
    重写HyperlinkedIdentityField，增加verison字段
    """

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value, 'version': 'v1'}
        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)


class WritableSerializerMethodField(serializers.SerializerMethodField):
    """可写的SerializerMethodField"""

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        self.setter_method_name = kwargs.pop('setter_method_name', None)

        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def bind(self, field_name, parent):
        retval = super().bind(field_name, parent)
        if not self.setter_method_name:
            self.setter_method_name = f'set_{field_name}'

        return retval

    def to_internal_value(self, data):
        # value = self.deserializer_field.to_internal_value(data)
        method = getattr(self.parent, self.setter_method_name)
        method(data)
        return {}
