from rest_framework import serializers
from info.models import CompanyInfoModel, WasteInfoModel


class WasteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteInfoModel
        # exclude = ['company']
        fields = ['id', 'image', 'type', 'amount', 'price']

class CompanyInfoSerializer(serializers.ModelSerializer):
    waste_infos = WasteInfoSerializer(many=True)

    class Meta:
        model = CompanyInfoModel
        fields = ['proposal_id', 'name', 'profile', 'address', 'rating', 'waste_infos']
    
    def create(self, validated_data):
        waste_infos_data = validated_data.pop('waste_infos')
        company = CompanyInfoModel.objects.create(**validated_data)
        
        for waste_info in waste_infos_data:
            WasteInfoModel.objects.create(proposal_id_id=company.proposal_id, **waste_info)
        return company
    
    # def update(self, instance, validated_data):
    #     waste_infos_data = validated_data.pop('waste_infos',)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.save()

    #     if waste_infos_data:
    #         instance.waste_infos.all().delete()
    #         for waste_info in waste_infos_data:
    #             WasteInfoModel.objects.create(company=instance, **waste_info)
    #     return instance
