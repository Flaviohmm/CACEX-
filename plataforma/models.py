from django.db import models
from datetime import datetime, timedelta

# Função para calcular a diferença em dias úteis
def dias_uteis(start_date, end_date):
    count = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Verificar se o dia da semana não é sabado (5) ou domigo (6)
        if current_date.weekday() < 5:
            count += 1
            
        # Avançar para o próximo dia
        current_date += timedelta(days=1)
        
    return count

class Nome(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Setor(models.Model):
    setor = models.CharField(max_length=100)

    def __str__(self):
        return self.setor
    
class Municipio(models.Model):
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return self.municipio
    
class Atividade(models.Model):
    atividade = models.CharField(max_length=100)

    def __str__(self):
        return self.atividade
    
class Status(models.TextChoices):
    NAO_INICIADO = "Não Iniciado"
    EM_ANALISE = "Em Análise"
    PENDENTE = "Pendente"
    CONCLUIDO = "Concluído"
    SUSPENSO = "Suspenso"

class RegistroAtividade(models.Model):
    nome = models.ForeignKey(Nome, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    descricao_atividade = models.TextField()
    data_recepcao = models.DateField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    observacao = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices)

    @property
    def duracao_dias_uteis(self):
        start_date = self.data_inicio
        end_date = self.data_fim
        
        # Calcular a diferença em dias úteis
        business_days = dias_uteis(start_date, end_date)
        
        return business_days
    
    def __str__(self):
        return f"{self.nome.nome} | {self.setor.setor} | {self.municipio.municipio} | {self.atividade.atividade} | {self.descricao_atividade} | {self.data_recepcao} | {self.data_inicio} | {self.data_fim} | {self.duracao_dias_uteis} | {self.observacao} | {self.status}"
    
    
    
    
    