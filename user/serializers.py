from rest_framework import serializers
from user.models import User, EMPLOYEE_ID_MAX, USERNAME_LENGTH_MAX

ROLE_CHOICES = [
    (1, 'employee'),
    (2, 'hr_staff'),
    (3, 'hr_admin'),
    (4, 'hr_superadmin'),
    (5, 'developer')
]

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    employee_id = serializers.IntegerField(max_value=EMPLOYEE_ID_MAX)
    username = serializers.CharField(max_length=USERNAME_LENGTH_MAX)
    password = serializers.CharField()
    date_added = serializers.DateTimeField()
    
    is_active = serializers.BooleanField()
    date_deleted = serializers.DateTimeField(required=False, allow_null=True)
    is_locked = serializers. BooleanField()

    failed_login_attempts = serializers.IntegerField()

    old_password = serializers.CharField(required=False, allow_null=True)
    date_password_change = serializers. DateTimeField(required=False, allow_null=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default=1)
    last_login = serializers.DateTimeField()

    

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)

        instance.employee_id = validated_data.get("employee_id", instance.employee_id)
        instance.username = validated_data.get("username", instance.username)
        instance.password = validated_data.get("password", instance.password)
        instance.date_added = validated_data.get("date_added", instance.date_added)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.date_deleted = validated_data.get("date_deleted", instance.date_deleted)
        instance.is_locked = validated_data.get("is_locked", instance.is_locked)
        instance.failed_login_attempts = validated_data.get("failed_login_attempts", instance.failed_login_attempts)
        instance.old_password = validated_data.get("old_password", instance.old_password)
        instance.dat0e_password_change = validated_data.get("date_password_change", instance.date_password_change)
        instance.role = validated_data.get("role", instance.role)

        instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        role = kwargs.get('data', {}).get('role')
        if role == 5:
            self.fields['employee_id'].max_value = 9999

        super().__init__(*args, **kwargs)