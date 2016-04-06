import slackweb
from Aprecie import settings

class Notificacoes():
	@staticmethod
	def notificar_no_slack(reconhecedor, reconhecido, valor):
		if not settings.ON_OPENSHIFT or not reconhecedor.usuario_no_slack or not reconhecido.usuario_no_slack:
			return

		mensagem = '*@{0}* acabou de ser reconhecido em *{1}* por *@{2}*'.format(reconhecido.usuario_no_slack, valor.nome, reconhecedor.usuario_no_slack)
		
		slack = slackweb.Slack(url='https://hooks.slack.com/services/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')
		slack.notify(text=mensagem, channel='#geral', username='Aprecie.me', link_names=1)