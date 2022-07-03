from rest_framework import serializers
from .models import Product
from .validator import validate_title


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_link = serializers.HyperlinkedIdentityField(view_name='rud-view', lookup_field='pk')
    # title = serializers.CharField(validators=[validate_title])
    # email = serializers.EmailField(write_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_data = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)

    def get_my_discount(self, obj):
        return obj.get_dicount()

    def get_user_data(self, obj):
        user_data = {
            'user_id': obj.user_id,
            'username': obj.user. username,
        }
        return user_data

    class Meta:
        model = Product
        fields = ('id', 'user', 'user_data', 'user_username', 'edit_link', 'title', 'content', 'price', 'self_price', 'my_discount')


    def validate_title(self, value):
        qs = Product.objects.filter(title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('Already in use')
        return value

    def create(self, validated_data):
        email = self.validated_data.pop('email')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        return super().update(instance, validated_data)