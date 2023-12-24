import re
import pandas as pd
from unidecode import unidecode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.http import require_POST
from weasyprint import HTML
from .models import RegistroAtividade, Nome, Setor, Municipio, Atividade, Status

import os
import csv
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/auth/login')
def home(request):
    registros = RegistroAtividade.objects.all()
    return render(request, 'home.html', {'registros': registros})

def adicionar_nome(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        Nome.objects.create(nome=nome)
        return redirect('home')
    
    return render(request, 'adicionar_nome.html')

def adicionar_setor(request):
    if request.method == 'POST':
        setor = request.POST.get('setor')
        Setor.objects.create(setor=setor)
        return redirect('home')
    
    return render(request, 'adicionar_setor.html')

def adicionar_municipio(request):
    if request.method == 'POST':
        municipio = request.POST.get('municipio')
        Municipio.objects.create(municipio=municipio)
        return redirect('home')
    
    return render(request, 'adicionar_municipio.html')

def adicionar_atividade(request):
    if request.method == 'POST':
        atividade = request.POST.get('atividade')
        Atividade.objects.create(atividade=atividade)
        return redirect('home')
    
    return render(request, 'adicionar_atividade.html')

def adicionar_registro(request):
    registros = RegistroAtividade.objects.all()
    
    if request.method == 'POST':
        nome = Nome.objects.get(id=request.POST.get('nome'))
        setor = Setor.objects.get(id=request.POST.get('setor'))
        municipio = Municipio.objects.get(id=request.POST.get('municipio'))
        atividade = Atividade.objects.get(id=request.POST.get('atividade'))
        descricao_atividade = request.POST.get('descricao_atividade')
        data_recepcao = request.POST.get('data_recepcao')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        observacao = request.POST.get('observacao')
        
        status_str = request.POST.get('status')  # Obtenha o valor do campo 'status'

        # Remova a acentuação e converta para maiúsculas
        status_str_clean = unidecode(status_str).upper()

        # Use expressão regular para remover caracteres não alfanuméricos
        status_str_clean = re.sub(r'[^a-zA-Z0-9]', '', status_str_clean)

        # Mapeie variações possíveis para os valores padrão da enumeração Status
        status_mapping = {
            'NAOINICIADONAOINICIADO': 'Não Iniciado',
            'EMANALISEEMANALISE': 'Em Análise',
            'PENDENTEPENDENTE': 'Pendente',
            'CONCLUIDOCONCLUIDO': 'Concluído',
            'SUSPENSOSUSPENSO': 'Suspenso',
        }

        # Obtenha o valor correspondente ou 'Desconhecido' se não houver correspondência
        status = status_mapping.get(status_str_clean, 'Desconhecido')

        registro = RegistroAtividade(
            nome=nome, 
            setor=setor, 
            municipio=municipio, 
            atividade=atividade, 
            descricao_atividade=descricao_atividade, 
            data_recepcao=data_recepcao, 
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            observacao=observacao, 
            status=status
        )
        registro.save()

    return render(request, 'adicionar_registro.html', {'status_choices': Status.choices, 'nomes': Nome.objects.all(), 'setores': Setor.objects.all(), 'municipios': Municipio.objects.all(), 'atividades': Atividade.objects.all(), 'registros': registros})

def visualizar_tabela(request):
    registros = RegistroAtividade.objects.all()
    
    return render(request, 'visualizar_tabela.html', {'registros': registros})

def gerar_relatorio_pdf(request):
    registros = RegistroAtividade.objects.all()
    
    # Renderiza o template
    template = get_template('visualizar_tabela.html')
    html_content = template.render({'registros': registros})

    # Configuração do PDF usando weasyprint e estilos externos
    views_dir = os.path.dirname(os.path.abspath(__file__))
    stylesheets = [os.path.join(views_dir, 'static/plataforma/css/styles.css')]
    pdf_files = HTML(string=html_content).write_pdf(stylesheets=stylesheets, page_size=('A4', 'landspace'))

    # Resposta HTTP com o PDF gerado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="relatorio.pdf"'
    response.write(pdf_files)

    return response

def exportar_csv(request):
    # Dados da tabela
    dados = [
        {'NOME': 'Alex Pereira', 'SETOR': 'FNDE', 'MUNICÍPIO': 'Pedro Avelino', 'ATIVIDADE': 'Prestação de Contas', 'DESCRIÇÃO DA ATIVIDADE': 'PPDE 2022 das escolas do município', 'DATA DE RECEPÇÃO': '16/03/2023', 'DATA DE INICIO': '06/07/2023', 'DATA DO FIM': '28/11/2023', 'DURAÇÃO DE DIAS': 104, 'OBSERVAÇÃO': '', 'STATUS': 'Concluído'},
        {'NOME': 'Anaise', 'SETOR': 'FNDE', 'MUNICÍPIO': 'Touros', 'ATIVIDADE': 'Prestação de Contas', 'DESCRIÇÃO DA ATIVIDADE': 'PNAE 2022', 'DATA DE RECEPÇÃO': '28/04/2023', 'DATA DE INICIO': '28/04/2023', 'DATA DO FIM': '', 'DURAÇÃO DE DIAS': '', 'OBSERVAÇÃO': 'Está sendo lançado o mês de dezembro de 2022 no sistema', 'STATUS': 'Pendente'},
        {'NOME': 'Maryllia', 'SETOR': 'Receita Federal', 'MUNICÍPIO': 'Rio do Fogo', 'ATIVIDADE': 'RFB - Parcelamento', 'DESCRIÇÃO DA ATIVIDADE': 'Formalização do parcelamento', 'DATA DE RECEPÇÃO': '', 'DATA DE INICIO': '', 'DATA DO FIM': '', 'DURAÇÃO DE DIAS': '', 'OBSERVAÇÃO': 'Ordem Cronologica', 'STATUS': 'Não iniciado'},
        {'NOME': 'Marta', 'SETOR': 'FTGS', 'MUNICÍPIO': 'Tibau do Sul', 'ATIVIDADE': 'Individualizar', 'DESCRIÇÃO DA ATIVIDADE': '', 'DATA DE RECEPÇÃO': '01/06/2023', 'DATA DE INICIO': '01/06/2023', 'DATA DO FIM': '', 'DURAÇÃO DE DIAS': '', 'OBSERVAÇÃO': 'Aguardando documentos. Só veio extrato', 'STATUS': 'Pendente'},
        {'NOME': 'Cinthia', 'SETOR': 'CAIXA', 'MUNICÍPIO': 'São Miguel do Gostoso', 'ATIVIDADE': 'Prestação de Contas', 'DESCRIÇÃO DA ATIVIDADE': 'SICONV', 'DATA DE RECEPÇÃO': '27/10/2023', 'DATA DE INICIO': '30/10/2023', 'DATA DO FIM': '05/11/2023', 'DURAÇÃO DE DIAS': '5', 'OBSERVAÇÃO': 'Enviar ao BJPREV', 'STATUS': 'Concluído'},
        {'NOME': 'Daniel Molick', 'SETOR': 'CAIXA', 'MUNICÍPIO': 'Extremoz', 'ATIVIDADE': 'Prestação de Contas', 'DESCRIÇÃO DA ATIVIDADE': 'SICONV', 'DATA DE RECEPÇÃO': '27/10/2023', 'DATA DE INICIO': '05/11/2023', 'DATA DO FIM': '', 'DURAÇÃO DE DIAS': '', 'OBSERVAÇÃO': '', 'STATUS': 'Em Analise'},
        {'NOME': 'Fátima', 'SETOR': 'Contabilidade', 'MUNICÍPIO': 'Goianinha', 'ATIVIDADE': 'Auditoria', 'DESCRIÇÃO DA ATIVIDADE': 'Contabilidade dos centro de custos', 'DATA DE RECEPÇÃO': '28/10/2023', 'DATA DE INICIO': '10/11/2023', 'DATA DO FIM': '', 'DURAÇÃO DE DIAS': '', 'OBSERVAÇÃO': '', 'STATUS': 'Em Analise'},
        {'NOME': 'Ingrid', 'SETOR': 'SIMEC', 'MUNICÍPIO': 'Lagoa Salgada', 'ATIVIDADE': 'Envio de documento', 'DESCRIÇÃO DA ATIVIDADE': 'Documento para celebração', 'DATA DE RECEPÇÃO': '30/10/2023', 'DATA DE INICIO': '15/12/2023', 'DATA DO FIM': '15/12/2023', 'DURAÇÃO DE DIAS': '1', 'OBSERVAÇÃO': '', 'STATUS': 'Concluído'},
    ]

    # Configuração do response para um arquivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    # Cria um objeto CSVWriter
    writer = csv.writer(response)

    # Escreve os cabeçalhos
    writer.writerow(['NOME', 'SETOR', 'MUNICÍPIO', 'ATIVIDADE', 'DESCRIÇÃO DA ATIVIDADE', 'DATA DE RECEPÇÃO', 'DATA DE INICIO', 'DATA DO FIM', 'DURAÇÃO DE DIAS', 'OBSERVAÇÃO', 'STATUS'])

    # Escreve os dados
    for dado in dados:
        writer.writerow([dado['NOME'], dado['SETOR'], dado['MUNICÍPIO'], dado['ATIVIDADE'], dado['DESCRIÇÃO DA ATIVIDADE'], dado['DATA DE RECEPÇÃO'], dado['DATA DE INICIO'], dado['DATA DO FIM'], dado['DURAÇÃO DE DIAS'], dado['OBSERVAÇÃO'], dado['STATUS']])

    return response