import pymsteams

from Aprecie import settings

class Notificacoes():

    @staticmethod
    def notificar_no_chat_msteams(reconhecedor, reconhecido, pilar, descritivo):
        if not settings.CHAT_WEBHOOK_URL_TEAMS:
            return

        myTeamsMessage = pymsteams.connectorcard(settings.CHAT_WEBHOOK_URL_TEAMS)
        # create the section
        myMessageSection = pymsteams.cardsection()
        # Section Title
        myMessageSection.title(f"{pilar.nome}")
        # Activity Elements
        myMessageSection.activityTitle(reconhecido.nome)
        
        # myMessageSection.activityImage(reconhecido.foto)

        # Facts are key value pairs displayed in a list.
        myMessageSection.addFact("feito por", reconhecedor.nome)
        # Section Text
        myMessageSection.text(descritivo)
        # Add your section to the connector card object before sending
        myTeamsMessage.addSection(myMessageSection)
        myTeamsMessage.summary("Resumo")
        myTeamsMessage.send()