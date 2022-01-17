from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
import os
from os.path import join
from Aprecie.settings import BASE_DIR


class AprecieConfig(AppConfig):
    name = "Aprecie"
   

    def verifica_data_final_do_ciclo(self):
        from Reconhecimentos.models import Ciclo
        from Reconhecimentos.views import obter_ciclo_atual
        
        ciclo_atual = obter_ciclo_atual()
    
        if ciclo_atual.data_final == date.today():
            amanha = date.today() + timedelta(days=1)
            reposta = Ciclo.object.get(data_inicial = amanha)
            if resposta == None:
                ciclo = Ciclo(data_inicial = amanha)
                ciclo.save()
            #exibir mensagem que o ciclo esta sem data final para todos os administradores
            #else:
            #exibir mensagem que o novo ciclo comeca no dia seguinte para todo mundo ou só para os adm??

        elif ciclo_atual.data_final != date.today():
            #verificar quantos dias faltam para terminar o ciclo atual
            ciclo_atual = obter_ciclo_atual()
            dias_para_terminar_ciclo = ciclo_atual.data_final - date.today()
            #exibir mensagem a partir de 10 dias faltando para o fim


    def ready(self):
        cron = BackgroundScheduler()
        cron.add_job(self.verifica_data_final_do_ciclo, 'interval', seconds=5)
        cron.start()