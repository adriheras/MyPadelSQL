# encoding:utf-8
from principal.models import *
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings
from principal import populateDB
from django.db.models import Max
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.index import create_in, open_dir
from principal.forms import JugadorNombreForm, JugadorPosicionForm
from principal.forms import JugadorCiudadForm
from principal.forms import JugadorEdadForm
from principal.forms import EstadisticasForm


def cargar(request):
    if populateDB.populateDatabase():
        jugadores = Jugador.objects.all().count()
        html = (
            "<html><body>Datos cargados correctamente. "
            + "Se han almacenado en la base de datos: "
            + str(jugadores)
            + " jugadores."
            + "</body></html>"
        )
    else:
        html = "<html><body>Error en la carga de datos</body></html>"
    return HttpResponse(html)


def inicio(request):
    jugadores = Jugador.objects.all()
    return render(request, "inicio.html", {"jugadores": jugadores})


def lista_jugadores(request):
    jugadores = Jugador.objects.all().order_by("ranking")
    return render(request, "ranking.html", {"jugadores": jugadores})


def busca_jugadores_nombre(request):
    formulario = JugadorNombreForm()
    lista = []
    if request.method == "POST":
        formulario = JugadorNombreForm(request.POST)
        if formulario.is_valid():
            entry = formulario.cleaned_data["nombre"]
            ix = open_dir("Index")
            # creamos un searcher en el Ã­ndice
            with ix.searcher() as searcher:
                query = QueryParser("nombre", ix.schema).parse(str(entry))
                # llamamos a la funciÃ³n search del searcher, pasÃ¡ndole como parÃ¡metro la consulta creada
                results = searcher.search(query, limit=None)
                for r in results:
                    lista.append(
                        [r["ranking"], r["puntos"], r["nombre"], r["posicion"], r["altura"], r["fechaNac"], r["lugarNac"], r["compañero"]]
                    )
    return render(request, "busca_jugadores_nombre.html", {"formulario": formulario, "results": lista})


def lista_jugadores_posicion(request):
    formulario = JugadorPosicionForm()
    lista = []
    if request.method == "POST":
        formulario = JugadorPosicionForm(request.POST)
        if formulario.is_valid():
            entry = formulario.cleaned_data["posicion"]
            ix = open_dir("Index")
            # creamos un searcher en el Ã­ndice
            with ix.searcher() as searcher:
                query = QueryParser("posicion", ix.schema).parse(str(entry))
                results = searcher.search(query, limit=None)
                for r in results:
                    lista.append(
                        [r["ranking"], r["puntos"], r["nombre"], r["posicion"], r["altura"], r["fechaNac"], r["lugarNac"], r["compañero"]]
                    )
    return render(request, "lista_jugadores_posicion.html", {"formulario": formulario, "results": lista})


def busca_jugadores_ciudad(request):
    formulario = JugadorCiudadForm()
    lista = []
    if request.method == "POST":
        formulario = JugadorCiudadForm(request.POST)
        if formulario.is_valid():
            entry = formulario.cleaned_data["ciudad"]
            ix = open_dir("Index")
            # creamos un searcher en el Ã­ndice
            with ix.searcher() as searcher:
                query = MultifieldParser(["residencia", "lugarNac"], ix.schema).parse(str(entry))
                # llamamos a la funciÃ³n search del searcher, pasÃ¡ndole como parÃ¡metro la consulta creada
                results = searcher.search(query, limit=None)
                for r in results:
                    lista.append(
                        [r["ranking"], r["puntos"], r["nombre"], r["posicion"], r["altura"], r["fechaNac"], r["lugarNac"], r["residencia"]]
                    )
    return render(request, "busca_jugadores_ciudad.html", {"formulario": formulario, "results": lista})


def filtra_jugadores_edad(request):
    formulario = JugadorEdadForm()
    lista = []
    if request.method == "POST":
        formulario = JugadorEdadForm(request.POST)
        if formulario.is_valid():
            inicio = formulario.cleaned_data["inicio"]
            fin = formulario.cleaned_data["fin"]
            ix = open_dir("Index")
            # creamos un searcher en el Ã­ndice
            with ix.searcher() as searcher:
                query = QueryParser("fechaNac", ix.schema).parse("[" + inicio + " TO " + fin + "]")
                # llamamos a la funciÃ³n search del searcher, pasÃ¡ndole como parÃ¡metro la consulta creada
                results = searcher.search(query, limit=None)
                for r in results:
                    lista.append(
                        [r["ranking"], r["puntos"], r["nombre"], r["posicion"], r["altura"], r["fechaNac"], r["lugarNac"], r["residencia"]]
                    )
    return render(request, "filtra_jugadores_edad.html", {"formulario": formulario, "results": lista})


def estadisticas(request):
    formulario = EstadisticasForm()
    estadisticas = []
    if request.method == "POST":
        formulario = EstadisticasForm(request.POST)
        if formulario.is_valid():
            entry = formulario.cleaned_data["estadisticas"]
            if entry == "Temporada":
                estadisticas = Temporada.objects.all().order_by("-partidosGAnyo")
            else:
                estadisticas = Historico.objects.all().order_by("-partidosG")
    return render(request, "estadisticas.html", {"formulario": formulario, "estadisticas": estadisticas})
