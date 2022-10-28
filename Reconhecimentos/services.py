from discord import SyncWebhook

from Aprecie import settings

class Notificacoes():
	@staticmethod
	def notificar_no_chat(reconhecedor, reconhecido, pilar):
		if not settings.CHAT_WEBHOOK_URL \
			or not reconhecido.usuario_id_do_chat \
			or not reconhecedor.usuario_id_do_chat:
			return

		mensagem = '**<@{0}>** acabou de ser reconhecido(a) em **{1}** por **<@{2}>**. Olha lá: http://aprecie.digix.com.br' \
			.format(reconhecido.usuario_id_do_chat, pilar.nome, reconhecedor.usuario_id_do_chat)

		webhook = SyncWebhook.from_url(settings.CHAT_WEBHOOK_URL)
		webhook.send(content=mensagem)
