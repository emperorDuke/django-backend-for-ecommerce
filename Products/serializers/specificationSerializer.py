from rest_framework import serializers

from Products.models.specification import Specification


class SpecificationListSerializer(serializers.ListSerializer):
 
    def create(self, validated_data):
        ret = []

        for data in validated_data:
            ret.append(Specification(**data))

        return Specification.objects.bulk_create(ret)

    def update(self, instance, validated_data):
        
        # collect data to be deleted

        data_for_deletion = []

        for i, data in enumerate(validated_data):
            if 'delete' in data and data['delete']:
                data_for_deletion.append(validated_data.pop(i))

        data_mapping = {data.get('id', None): data for data in validated_data}
        spec_mapping = {spec_obj.id: spec_obj for spec_obj in instance}

        ret = []

        # creation and updating operation #

        for spec_id, data in data_mapping.items():
            spec_obj = spec_mapping.get(spec_id, None)
            if spec_obj is None:
                ret.append(self.child.create(data))
            else:
                del data['id']
                ret.append(self.child.update(spec_obj, data))

        # deletion operation #

        for data in data_for_deletion:
            instance = spec_mapping.get(data.get('id'))
            instance.delete()

        return ret


class SpecificationSerializer (serializers.ModelSerializer):
    
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False)

    class Meta:
        model = Specification
        exclude = ('added_at', 'updated_at')
        list_serializer_class = SpecificationListSerializer
        validators = []

    
    def to_representation(self, instance):
        if 'delete' in self.fields:
            self.fields.pop('delete')

        return super().to_representation(instance)
