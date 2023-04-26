from rest_framework import serializers
from user.models import User


# FOR SHORTCUTS

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'employee_id', 'username', 'password', 'date_added', 'is_active', 
#               'date_deleted', 'is_locked', 'failed_login_attempts', 'old_password', 
#               'date_password_change', 'role', 'last_login', ]

ROLE_CHOICES = [
    (1, 'employee'),
    (2, 'hr_staff'),
    (3, 'hr_admin'),
    (4, 'hr_superadmin'),
    (5, 'developer')
]

# class EmployeeIDIntegerField(serializers.IntegerField):
#     def to_internal_value(self, data):
#         role = self.context.get('request').data.get('role')
#         if role == 5:
#             self.max_value = 9999
#         return super().to_internal_value(data)

class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    employee_id = serializers.IntegerField(max_value=9990)
    # employee_id = EmployeeIDIntegerField(max_value=9990)
    username = serializers.CharField(max_length=8)
    password = serializers.CharField()
    date_added = serializers.DateTimeField()
    
    is_active = serializers.BooleanField()
    date_deleted = serializers.DateTimeField(required=False, allow_null=True)
    is_locked = serializers. BooleanField()

    failed_login_attempts = serializers.IntegerField()

    old_password = serializers.CharField(required=False)
    date_password_change = serializers. DateTimeField(required=False, allow_null=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)
    last_login = serializers.DateTimeField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):

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
    
    # def validate_user_data(data):
    #     serializer = UserSerializer(data=data, context=self.context)
    #     serializer.is_valid(raise_exception=True)
    #     validated_data = serializer.validated_data
    #     return validated_data
    
    # def __init__(self, *args, **kwargs):
    #     role = kwargs.get('data', {}).get('role')
    #     if role == 5:
    #         self.fields['employee_id'].max_value = 9999

    #     super().__init__(*args, **kwargs)