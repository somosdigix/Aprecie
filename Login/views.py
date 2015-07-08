# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from models import Funcionario
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def login_de_funcionario(requisicao):
	return render(requisicao, 'login.html')

@csrf_exempt
def entrar(requisicao):
	cpf = requisicao.POST['cpf']
	data_de_nascimento = datetime.strptime(requisicao.POST['data_de_nascimento'], '%d/%m/%Y')

	funcionario_autenticado = authenticate(cpf=cpf, data_de_nascimento=data_de_nascimento)

	if funcionario_autenticado:
		return JsonResponse({ 'autenticado': True })

	return JsonResponse({ 'autenticado': False, 'mensagem': 'Colaborador não encontrado, confirme seus dados tente novamente' })

@csrf_exempt
def obter_funcionarios(requisicao):
	termo = requisicao.GET['term']
	funcionarios = Funcionario.objects.filter(nome__icontains=termo)
	funcionarios = map(lambda funcionario: { 'cpf': funcionario.cpf, 'nome': funcionario.nome }, funcionarios)
	
	return JsonResponse(funcionarios, safe=False)

@login_required
def sair(requisicao):
	logout(requisicao)
	return redirect(login_de_funcionario)	

@login_required
def index(requisicao):
	return render(requisicao, 'index.html', {'mensagem': 'Logou'})