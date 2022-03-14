# encoding:utf-8
from django.db import models



class Jugador(models.Model):
    nombre = models.TextField(unique=True)
    ranking = models.PositiveSmallIntegerField(default=0)
    puntos = models.PositiveIntegerField(default=0)
    compañero = models.TextField(null=True)
    posicion = models.TextField()
    lugarNac = models.TextField()
    fechaNac = models.DateField()
    altura = models.PositiveIntegerField(default=0)
    residencia = models.TextField()

    def __str__(self):
        return self.nombre

class Historico(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, default=0)
    partidosJ = models.PositiveIntegerField(default=0)
    partidosG = models.PositiveIntegerField(default=0)
    partidosP = models.PositiveIntegerField(default=0)
    efectividad = models.DecimalField(decimal_places= 2, max_digits = 4)
    victoriasConsec = models.PositiveIntegerField(default=0)    

    def __str__(self):
        return self.jugador

class Temporada(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, default=0)
    partidosJAnyo = models.PositiveIntegerField(default=0)
    partidosGAnyo = models.PositiveIntegerField(default=0)
    partidosPAnyo = models.PositiveIntegerField(default=0)
    efectividadAnyo = models.DecimalField(decimal_places= 2, max_digits = 4, default=0)
    campeon = models.PositiveIntegerField(default=0)
    finalista = models.PositiveIntegerField(default=0)
    semifinalista = models.PositiveIntegerField(default=0)      
    cuartos = models.PositiveIntegerField(default=0) 
    octavos = models.PositiveIntegerField(default=0)
    dieciseisavos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.jugador
