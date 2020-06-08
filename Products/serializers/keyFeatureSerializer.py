from rest_framework import serializers

from Products.models.keyFeature import KeyFeature


class KeyFeatureListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        ret = []

        for data in validated_data:
            ret.append(KeyFeature(**data))

        return KeyFeature.objects.bulk_create(ret)

    def update(self, instance, validated_data):
        data_for_deletion = []

        for i, data in enumerate(validated_data):
            if 'delete' in data and data['delete']:
                data_for_deletion.append(validated_data.pop(i))
                
        data_mapping = {data.get('id', None): data for data in validated_data}
        features_mapping = {feature.id: feature for feature in instance}

        ret = []

        # creation and updating operation #

        for feature_id, data in data_mapping.items():
            key_feature_obj = features_mapping.get(feature_id, None)
            if key_feature_obj is None:
                ret.append(self.child.create(data))
            else:
                del data['id']
                ret.append(self.child.update(key_feature_obj, data))

        # deletion operation #
        
        for data in data_for_deletion:
            instance = features_mapping.get(data.get('id'))
            instance.delete()

        return ret


class KeyFeatureSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False)

    class Meta:
        model = KeyFeature
        exclude = ('added_at', 'updated_at')
        list_serializer_class = KeyFeatureListSerializer
        validators = []

    def to_representation(self, instance):
        if 'delete' in self.fields:
            self.fields.pop('delete')

        return super().to_representation(instance)
