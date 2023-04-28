from rest_framework import serializers
from user.models import User, Employee, AuditTrail, DTR, CityMunicipality

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

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

class CityMunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityMunicipality
        fields = "__all__"