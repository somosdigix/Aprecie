from zoneinfo import available_timezones
from rolepermissions.roles import AbstractUserRole

class administrador(AbstractUserRole):
    available_permissions = {
        'adicionar_administrador' : True,
        'remover_administrador'  : True
    }

class recursos_humanos(AbstractUserRole):
    available_permissions = {
        'cadastrar_colaborador' : True,
        'ativar_colaborador' : True,
        'desativar_colaborador' : True
    }