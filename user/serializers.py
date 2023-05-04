from rest_framework import serializers
from user.models import User, Employee, AuditTrail, DTR, DTRSummary, Holiday, OBT, Province, CityMunicipality, OvertimeEntry

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

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"

class OBTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OBT
        fields = "__all__"

class CityMunicipalitySerializer(serializers.ModelSerializer):
    # Include the code below to access the fields you want to add in your API
    # province_name = serializers.CharField(source="province.name", read_only=True)
    data = serializers.SerializerMethodField()
    
    class Meta:
        model = CityMunicipality
        fields = ["id", "name", "province", "data"]

    def get_data(self, obj):
        return {'province': obj.province.id, "province_name":obj.province.name}

class ProvinceSerializer(serializers.ModelSerializer):
    # Include code below if you want to enable the parent model to access the data on the child model
    citymunicipality_set = CityMunicipalitySerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ("id", "name", "citymunicipality_set")

class OvertimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimeEntry
        fields = "__all__"
