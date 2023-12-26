import os
import sys
import django

# Adicione o diretório do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma.settings')
django.setup()

from plataforma.models import RegistroAtividade
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def main():
    st.title("Dashboard Relatório de Atividades")

    # Obtenha dados do Django ORM
    registros = RegistroAtividade.objects.all().values(
        'nome__nome',
        'setor__setor',
        'municipio__municipio',
        'atividade__atividade',
        'descricao_atividade',
        'data_recepcao',
        'data_inicio',
        'data_fim', 
        'observacao',
        'status'
    )

    df = pd.DataFrame(registros)

    # Exiba os dados
    st.table(df)

    # Criar um gráfico de pizza usando Plotly
    fig = go.Figure(data=[go.Pie(labels=df['status'])])

    # Exiba os dados
    st.plotly_chart(fig)

    # Adicionar gráficos adicionais conforme necessário
    st.bar_chart(df['setor__setor'].value_counts())
    st.bar_chart(df['atividade__atividade'].value_counts())

if __name__ == '__main__':
    main()
