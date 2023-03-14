from discord import SyncWebhook
import pymsteams
import logging

from Aprecie import settings
logger = logging.getLogger(__name__)

class Notificacoes():

    @staticmethod
    def notificar_no_chat_discord(reconhecedor, reconhecido, pilar):
        if not settings.CHAT_WEBHOOK_URL \
            or not reconhecido.usuario_id_do_chat \
            or not reconhecedor.usuario_id_do_chat:
            return

        mensagem = '**<@{0}>** acabou de ser reconhecido(a) em **{1}** por **<@{2}>**. Olha lá: http://aprecie.digix.com.br' \
            .format(reconhecido.usuario_id_do_chat, pilar.nome, reconhecedor.usuario_id_do_chat)

        webhook = SyncWebhook.from_url(settings.CHAT_WEBHOOK_URL)
        webhook.send(content=mensagem)

    @staticmethod
    def notificar_no_chat_msteams(reconhecedor, reconhecido, pilar):
        arroba = '@'
        logger.warning('entrou na notificação')
        mensagem = '{0} acabou de ser reconhecido(a) em {1} por {2}. Olha lá: http://aprecie.digix.com.br'.format(reconhecido.nome, pilar.nome, reconhecedor.nome)
        myTeamsMessage = pymsteams.connectorcard(settings.CHAT_WEBHOOK_URL)
        myTeamsMessage.text(mensagem)
        myTeamsMessage.payload = {
            "type": "message",
            "attachments": [
                {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                        "type": "TextBlock",
                        "text": mensagem
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0",
                    "msteams": {
                        "entities": [
                            {
                                "type": "mention",
                                "text": reconhecedor.nome,
                                "mentioned": {
                                    "id": 'ff8eb29b-e634-4db9-8d37-b7cf4f4c00d0',
                                    "name": reconhecedor.nome,
                                }
                            }
                        ]
                    }
                }
            }]
        }

        # message_payload = {
        #     "@type": "MessageCard",
        #     "@context": "http://schema.org/extensions",
        #             "text": mensagem,
        #     "mentions": [
        #         {
        #             "mri": f"mention:ff8eb29b-e634-4db9-8d37-b7cf4f4c00d0",
        #             "text": reconhecido.nome,
        #             "id": "ff8eb29b-e634-4db9-8d37-b7cf4f4c00d0"
        #                 }
        #     ]
        # }
        # myTeamsMessage.payload = message_payload
        myTeamsMessage.send()
        logger.warning('enviou a notificação')
        logger.warning(reconhecido)
        logger.warning(reconhecedor)