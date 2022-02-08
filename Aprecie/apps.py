from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.core.exceptions import ObjectDoesNotExist



class AprecieConfig(AppConfig):
    name = "Aprecie" 
    mensagem = " "

    def notificacao_do_colaborador(self, notificacao):
        AprecieConfig.mensagem = notificacao
    
    @staticmethod
    def obter_mensagem_notificacao():
        return AprecieConfig.mensagem

    def verifica_data_final_do_ciclo(self):
        from Reconhecimentos.models import Ciclo
        from Reconhecimentos.views import obter_ciclo_atual
        
        ciclo_atual = obter_ciclo_atual()
    
        if ciclo_atual.data_final == date.today():
            amanha = date.today() + timedelta(days=1)
            try:
                resposta = Ciclo.objects.get(data_inicial = amanha)
                #exibir mensagem que o novo ciclo comeca no dia seguinte para todo mundo ou só para os adm??
                self.notificacao_do_colaborador("Amanhã será iniciado um novo ciclo")
            except Ciclo.DoesNotExist:
                ciclo = Ciclo(data_inicial = amanha)
                ciclo.save()
                #exibir mensagem que o ciclo esta sem data final para todos os administradores
                self.notificacao_do_colaborador("O ciclo atual não possui data final")
           

        elif ciclo_atual.data_final != date.today():
            #verificar quantos dias faltam para terminar o ciclo atual
            dias_para_terminar_ciclo = ciclo_atual.data_final - date.today()
            #exibir mensagem a partir de 10 dias faltando para o fim
            if dias_para_terminar_ciclo < timedelta(days=10):
                mensagem = "Faltam " + str(dias_para_terminar_ciclo.days) + " dias para o fim do ciclo atual"
                self.notificacao_do_colaborador(mensagem)
        
        else:
            self.notificacao_do_colaborador("")
        

    def ready(self):
        cron = BackgroundScheduler()
        cron.add_job(self.verifica_data_final_do_ciclo, 'interval', seconds=5)
        cron.start()