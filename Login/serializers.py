from Login.models import Colaborador, LOG_Administrador
from rest_framework import serializers

class ColaboradorSerializer(serializers.Serializer):
    class Meta:
        model = Colaborador
        fields = ['id', 'cpf', 'nome', 'data_de_nascimento', 'foto', 'usuario_id_do_chat', 'administrador', 'data_ultimo_reconhecimento']