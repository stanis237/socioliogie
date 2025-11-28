from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, UserProfile, UserSettings, UserActivityLog

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})

        # Set username to email since email is the USERNAME_FIELD
        attrs['username'] = attrs['email']

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        # Créer UserProfile et UserSettings uniquement si non existants
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)
        if not UserSettings.objects.filter(user=user).exists():
            UserSettings.objects.create(user=user)
        return user


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['theme', 'language', 'font_size', 'auto_play_videos', 'subtitles_enabled',
                 'notifications_email', 'notifications_push', 'notifications_sms', 'allow_analytics']
        read_only_fields = ['created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user_email', 'user_username', 'total_learning_minutes', 'exercises_completed',
                 'average_score', 'streaks_days', 'badges']
        read_only_fields = ['total_learning_minutes', 'exercises_completed', 'average_score', 
                           'streaks_days', 'badges']


class CustomUserSerializer(serializers.ModelSerializer):
    detailed_profile = UserProfileSerializer(read_only=True)
    settings = UserSettingsSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture',
                 'bio', 'learning_style', 'proficiency_level', 'interests', 'goals',
                 'daily_goal_minutes', 'timezone', 'notification_enabled', 'emotion_tracking_enabled',
                 'webcam_consent', 'privacy_accepted', 'last_activity', 'is_active_learner',
                 'detailed_profile', 'settings']
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_activity']


class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = ['id', 'activity_type', 'description', 'metadata', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_picture', 'bio', 'learning_style',
                 'proficiency_level', 'interests', 'goals', 'daily_goal_minutes', 'timezone',
                 'notification_enabled', 'emotion_tracking_enabled', 'webcam_consent']
