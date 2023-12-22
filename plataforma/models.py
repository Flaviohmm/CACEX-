from django.db import models

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
    NAO_INICIADO = "Não iniciado", "Não iniciado"
    EM_ANALISE = "Em análise", "Em análise"
    PENDENTE = "Pendente", "Pendente"
    CONCLUIDO = "Concluído", "Concluído"
    SUSPENSO = "Suspenso", "Suspenso"

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
    def duracao_dias(self):
        return (self.data_fim - self.data_inicio).days
    
    def __str__(self):
        return f"{self.nome} | {self.setor} | {self.municipio} | {self.atividade} | {self.descricao_atividade} | {self.data_recepcao} | {self.data_inicio} | {self.data_fim} | {self.duracao_dias} | {self.observacao} | {self.status}"
    
    
    
    
    