from discord import Webhook, RequestsWebhookAdapter

from Aprecie import settings

class Notificacoes():
	@staticmethod
	def notificar_no_chat(reconhecedor, reconhecido, pilar):
		if not settings.CHAT_WEBHOOK_URL:
			return

		mensagem = '**<@{0}>** acabou de ser reconhecido(a) em **{1}** por **<@{2}>**' \
			.format(reconhecido.usuario_id_do_chat, pilar.nome, reconhecedor.usuario_id_do_chat)

		webhook = Webhook.from_url(settings.CHAT_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
		webhook.send(mensagem)
