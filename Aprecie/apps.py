from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig

class AprecieConfig(AppConfig):
    name = "Aprecie" 
    mensagem = " "

    @staticmethod
    def notificacao_do_colaborador(notificacao):
        AprecieConfig.mensagem = notificacao
    
    @staticmethod
    def obter_mensagem_notificacao():
        return AprecieConfig.mensagem

    def verifica_data_final_do_ciclo(self):
        from Reconhecimentos.models import Ciclo, LOG_Ciclo
        from Reconhecimentos.views import obter_ciclo_atual
        
        try:
            ciclo_atual = obter_ciclo_atual()
        
            if ciclo_atual.data_final == date.today():
                amanha = date.today() + timedelta(days=1)
                try:
                    resposta = Ciclo.objects.get(data_inicial = amanha)
                except Ciclo.DoesNotExist:
                    ciclo = Ciclo(data_inicial = amanha)
                    ciclo.save()
                    log_Ciclo = LOG_Ciclo.adicionar_automatico(ciclo)
                    log_Ciclo.save()
                AprecieConfig.notificacao_do_colaborador("Amanhã será iniciado um novo ciclo")

            elif ciclo_atual.data_final == None:
                AprecieConfig.notificacao_do_colaborador("O ciclo atual não possui data final")

            elif ciclo_atual.data_final != date.today():
                dias_para_terminar_ciclo = ciclo_atual.data_final - date.today()
                if dias_para_terminar_ciclo < timedelta(days=10):
                    mensagem = "Faltam " + str(dias_para_terminar_ciclo.days) + " dias para o fim do ciclo atual"
                    AprecieConfig.notificacao_do_colaborador(mensagem)
            
            else:
                AprecieConfig.notificacao_do_colaborador("")
    
        except  Ciclo.DoesNotExist:
            ciclo_atual = Ciclo(data_inicial = date.today())
            ciclo_atual.save()
            log_Ciclo = LOG_Ciclo.adicionar_automatico(ciclo_atual)
            log_Ciclo.save()
            AprecieConfig.notificacao_do_colaborador("O ciclo atual não possui data final")
    

    def ready(self):
        cron = BackgroundScheduler(timezone="America/Campo_Grande")
        cron.add_job(self.verifica_data_final_do_ciclo, 'interval', seconds=5)
        #cron.add_job(self.verifica_data_final_do_ciclo, 'cron', hour=6)
        cron.start()