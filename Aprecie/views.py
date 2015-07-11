from django.shortcuts import render

def index(requisicao):
	return render(requisicao, "index.html")