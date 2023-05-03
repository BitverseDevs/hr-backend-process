from rest_framework import serializers
from user.models import User, Employee, AuditTrail, DTR, DTRSummary, CityMunicipality

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        # prevent password from returning on json file
        extra_kwargs = {
            "password": {"write_only":True}
        }

    # def create(self, validated_data):
    #     password = validated_data.pop("password", None)
    #     instance = self.Meta.model(**validated_data)

    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()

    #     return instance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = "__all__"
        
class DTRSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTR
        fields = "__all__"

class DTRSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DTRSummary
        fields = "__all__"

class CityMunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityMunicipality
        fields = "__all__"