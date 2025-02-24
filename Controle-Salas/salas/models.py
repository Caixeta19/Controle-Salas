from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Sala(models.Model):
    nome = models.CharField(max_length=50)
    capacidade = models.IntegerField()

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    sala = models.ForeignKey('Sala', on_delete=models.CASCADE)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def clean(self):
        # Verifica conflitos de horário para a mesma sala
        conflitos = Agendamento.objects.filter(
            sala=self.sala,
            data=self.data,
        ).exclude(id=self.id)  # Exclui o próprio registro em edições

        for agendamento in conflitos:
            # Verifica se os horários se sobrepõem
            if (
                self.horario_inicio < agendamento.horario_fim
                and self.horario_fim > agendamento.horario_inicio
            ):
                raise ValidationError(
                    f"A sala '{self.sala.nome}' já está ocupada entre {agendamento.horario_inicio} e {agendamento.horario_fim}."
                )

    def save(self, *args, **kwargs):
        # Garante que a validação seja chamada antes de salvar
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sala.nome} - {self.data} ({self.horario_inicio} - {self.horario_fim})"
