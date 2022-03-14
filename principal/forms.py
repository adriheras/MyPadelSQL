#encoding:utf-8
from django import forms
   
class JugadorNombreForm(forms.Form):
    nombre = forms.CharField(label="Nombre del jugador", widget=forms.TextInput, required=True)

class JugadorPosicionForm(forms.Form):
    posicion = forms.CharField(label="Posición del jugador", widget=forms.Select(choices=[('Drive','Drive'),
             ('Revés','Revés')]), required=True)

class JugadorCiudadForm(forms.Form):
    ciudad = forms.CharField(label="Ciudad del jugador", widget=forms.TextInput, required=True)

class JugadorEdadForm(forms.Form):
    inicio = forms.CharField(label="Fecha inicio", widget=forms.TextInput, required=True)
    fin = forms.CharField(label="Fecha fin", widget=forms.TextInput, required=True)

class EstadisticasForm(forms.Form):
    estadisticas = forms.CharField(label="Posición del jugador", widget=forms.Select(choices=[('Temporada','Temporada'),
             ('Historico','Historico')]), required=True)
