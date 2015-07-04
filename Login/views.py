from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def login_de_funcionario(requisicao):
	return render(requisicao, "login.html")

def logar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST["data_de_nascimento"], "%d/%m/%Y")
	usuario = authenticate(cpf=cpf, data_de_nascimento=data_de_nascimento)
	login(requisicao, usuario)
	return redirect(index)

@login_required(login_url="/login/")
def index(requisicao):
	return render(requisicao, "index.html", {"mensagem": "Logou"})

