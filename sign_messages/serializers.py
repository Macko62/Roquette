from rest_framework.serializers import ModelSerializer
from .models import mdlSignMessages

class smSerializer(ModelSerializer):
    class Meta:
        model=mdlSignMessages
        fields=[
            'msgNum',
            'tuNumExt',
            'door',
            'userOverride'
        ]