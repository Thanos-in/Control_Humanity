from rest_framework import serializers
from .models import Rating
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RatingSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    to_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='employee'),
        source='to_user',
        write_only=True
    )

    class Meta:
        model = Rating
        fields = ('id', 'from_user', 'to_user', 'to_user_id', 'score', 'comment', 'created_at')
        read_only_fields = ('from_user', 'created_at')

    def create(self, validated_data):
        validated_data['from_user'] = self.context['request'].user
        return super().create(validated_data)
