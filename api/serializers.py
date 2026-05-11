from rest_framework import serializers # type: ignore
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UPISerializer(serializers.ModelSerializer):
    class Meta:
        model = UPIInfo
        fields = '__all__'



from .models import Submission, Product

class SubmissionSerializer(serializers.ModelSerializer):
    selected_product_name = serializers.CharField(
        source='selected_product.name',
        read_only=True
    )

    batch_number = serializers.IntegerField(
        source='batch.batch_number',
        read_only=True
    )

    # 👇 accept frontend field
    selected_product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        extra_kwargs = {
            "selected_product": {"required": False}  # 👈 IMPORTANT FIX
        }

    def create(self, validated_data):
        product_id = validated_data.pop('selected_product_id')

        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise serializers.ValidationError({
                "selected_product_id": "Invalid product ID"
            })

        validated_data['selected_product'] = product
        return Submission.objects.create(**validated_data)

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'