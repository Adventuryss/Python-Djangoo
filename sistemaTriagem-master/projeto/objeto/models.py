from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Objeto(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    

    nome = models.CharField(_('Nome do paciente'), max_length=20, null=True, blank=True)
    idade = models.CharField(_('Idade do paciente'), max_length=20, null=True, blank=True)
    altura = models.CharField(_('Altura do paciente'), max_length=20, null=True, blank=True)
    peso = models.CharField(_('Peso do paciente'), max_length=20, null=True, blank=True)

    febre = models.CharField(_('O paciente possui febre? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    cabeca = models.CharField(_('O paciente possui dor de cabeca??? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)

    nasal = models.CharField(_('O paciente tem secrecao nasal ou espirros? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    garganta = models.CharField(_('O paciente possui dor de garganta? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    tosse = models.CharField(_('O paciente possui tosse seca? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    dificuldadeResp = models.CharField(_('O paciente possui dificuldade respiratoria? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    dorCorpo = models.CharField(_('O paciente possui dor no corpo? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    diarreia = models.CharField(_('O paciente possui diarreia? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    viajou = models.CharField(_('O paciente viajou recentemente para alguma local com casos de Covid? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    contato = models.CharField(_('O paciente teve contato com alguemm que teve um caso de Covid? (RESPONDER COM SIM OU NAO)'), max_length=20, null=True, blank=True)
    resultado = models.CharField(_('Resultado do Diagnostico (O RESULTADO IRA SAIR APOS O CADASTRO)'), max_length=20, null=True, blank=True)

    imc = models.CharField(_('IMC (Será preenchido automaticamente apos o cadastro)'), max_length=20, null=True, blank=True)
    data = models.CharField(_('Data da triagem (usar formato DD/MM/AAAA)'), max_length=20, null=True, blank=True)
    hora = models.CharField(_('Hora da triagem (usar formato MM:HH)'), max_length=20, null=True, blank=True)
    slug = models.SlugField('Hash', max_length= 200, null=True, blank=True)


    objects = models.Manager()
    
    class Meta:
        ordering            =   ['data','hora']
        verbose_name        =   ('objeto')
        verbose_name_plural =   ('objetos')

    def save(self, *args, **kwargs):
        #calculo do imc
        a = float(self.peso)
        b = float(self.altura)

        imc = a / b ** 2
        imc2 = imc * 10000

        # calculo triagem
        resul = 0
        resul2 = ""

        if(self.febre == "Sim"):
            resul += 5

        if(self.cabeca == "Sim"):
            resul += 1

        if(self.nasal == "Sim"):
            resul += 1

        if(self.garganta == "Sim"):
            resul += 1

        if(self.tosse == "Sim"):
            resul += 3

        if(self.dificuldadeResp == "Sim"):
            resul += 10

        if (self.dorCorpo == "Sim"):
            resul += 1

        if (self.diarreia == "Sim"):
            resul += 1

        if (self.viajou == "Sim"):
            resul += 3

        if (self.contato == "Sim"):
            resul += 10


        if(resul >= 1 and resul <= 9):
            resul2 = "RISCO BAIXO!"
        elif(resul >= 10 and resul <= 19):
            resul2 = "RISCO MEDIO!"
        elif(resul >= 20 and resul <= 36):
            resul2 = "RISCO ALTO!"


        if not self.slug:
            self.slug = gerar_hash()

        self.data = self.data.upper()
        self.hora = self.hora.upper()
        self.imc = imc2
        self.resultado = resul2
        self.peso = self.peso.upper()

        self.febre = self.febre.upper()
        self.cabeca = self.cabeca.upper()

        self.altura = self.altura.upper()
        self.idade = self.idade.upper()
        self.nome = self.nome.upper()
        super(Objeto, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('objeto_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('objeto_delete', args=[str(self.id)])

