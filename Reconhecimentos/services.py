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
		# if not settings.CHAT_WEBHOOK_URL \
		# 	or not reconhecido.email_do_reconhecido \
		# 	or not reconhecedor.email_do_reconhecedor:
		# 	return
		logger.warning('entrou na notificação')
		mensagem = '**<@{0}>** acabou de ser reconhecido(a) em **{1}** por **<@{2}>**. Olha lá: http://aprecie.digix.com.br' \
			.format(reconhecido.email, pilar.nome, reconhecedor.email)
		myTeamsMessage = pymsteams.connectorcard('https://somosdigix.webhook.office.com/webhookb2/da1ea293-f7a3-4eb0-bb87-0b31a31d0f64@0b7d0763-4b89-40fa-9dec-6eed7d82aad4/IncomingWebhook/ac427f9971de451fbd26cb672563c32f/ff8eb29b-e634-4db9-8d37-b7cf4f4c00d0')
		myTeamsMessage.text(mensagem)
		myTeamsMessage.send()