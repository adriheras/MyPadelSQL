# encoding:utf-8
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
import time
from tkinter import NUMERIC
from principal.models import Temporada, Historico, Jugador
from bs4 import BeautifulSoup
import urllib.request
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME


def populateDatabase():

    # borrar tablas
    Temporada.objects.all().delete()
    Jugador.objects.all().delete()
    Historico.objects.all().delete()

    
    schem = Schema(
        nombre=TEXT(stored=True),
        ranking=TEXT(stored=True),
        puntos=TEXT(stored=True),
        compañero=TEXT(stored=True),
        posicion=TEXT(stored=True),
        lugarNac=TEXT(stored=True),
        fechaNac=DATETIME(stored=True),
        altura=TEXT(stored=True),
        residencia=TEXT(stored=True)
    )

    # eliminamos el directorio del Ã­ndice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")

    # creamos el Ã­ndice
    ix = create_in("Index", schema=schem)
    # creamos un writer para poder aÃ±adir documentos al indice
    writer = ix.writer()
    i = 0

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.worldpadeltour.com/jugadores?ranking=masculino")
    ScrollNumber = 5
    for i in range(1,ScrollNumber): 
        driver.execute_script("window.scrollTo(1,50000)")
        time.sleep(1)
    file = open('DS.html', 'w', encoding="utf-8")
    file.write(driver.page_source)
    file.close()
    driver.close()

    data = open('DS.html','r', encoding="utf-8")
    s = BeautifulSoup(data, "lxml")
    lista_jugadores = s.find("ul", class_="c-player-card u-list-clean").find_all("li")
    for jugador in lista_jugadores:
        req = urllib.request.Request(jugador.a["href"], headers={"User-Agent": "Mozilla/5.0"})
        f = urllib.request.urlopen(req)
        s = BeautifulSoup(f, "lxml")

        nombre = s.find("h1", class_="c-ranking-header__title").string
        datos = s.find_all("li", class_="c-player__data-item")
        compañero = datos[0].a.string
        posicion = datos[1].p.string
        lugarNac = datos[2].p.string
        fechaNac = datos[3].p.string
        fechaNac = datetime.datetime.strptime(fechaNac, "%d/%m/%Y").strftime("%Y-%m-%d")
        altura = int(datos[4].p.string.replace(",", "").replace("'","").replace(" m ","").replace("cm","").replace(".","").replace(" m",""))
        residencia = datos[5].p.string

        header = s.find_all("p", class_="c-ranking-header__data")
        ranking = header[0].string
        puntos = header[1].string
        partidosJ = header[2].string
        partidosG = header[3].string
        partidosP = header[4].string
        efectividad = float(header[5].string.replace(",", "."))
        victoriasConsec = header[6].string

        stats = s.find_all("span", class_="c-flex-table__item-data")
        if stats:
            partidosJAnyo = stats[0].string
            partidosGAnyo = stats[1].string
            partidosPAnyo = int(partidosJAnyo)-int(partidosGAnyo)
            efectividadAnyo = float(stats[2].string.replace(",", "."))
            campeon = stats[3].string
            finalista = stats[4].string
            semifinalista = stats[5].string
            cuartos = stats[6].string
            octavos = stats[7].string
            dieciseisavos = stats[8].string

        Jugador.objects.create(
            nombre=nombre,
            ranking=ranking,
            puntos=puntos,
            compañero=compañero,
            posicion=posicion,
            lugarNac=lugarNac,
            fechaNac=fechaNac,
            altura=altura,
            residencia=residencia,
        )

        Historico.objects.create(
            jugador=Jugador.objects.get(nombre=nombre),
            partidosJ=partidosJ,
            partidosG=partidosG,
            partidosP=partidosP,
            efectividad=efectividad,
            victoriasConsec=victoriasConsec,
        )

        Temporada.objects.create(
            jugador=Jugador.objects.get(nombre=nombre),
            partidosJAnyo=partidosJAnyo,
            partidosGAnyo=partidosGAnyo,
            partidosPAnyo=partidosPAnyo,
            efectividadAnyo=efectividadAnyo,
            campeon=campeon,
            finalista=finalista,
            semifinalista=semifinalista,
            cuartos=cuartos,
            octavos=octavos,
            dieciseisavos=dieciseisavos,
        )

        writer.add_document(
            nombre=str(nombre),
            ranking=str(ranking),
            puntos=str(puntos),
            compañero=str(compañero),
            posicion=str(posicion),
            lugarNac=str(lugarNac),
            fechaNac=str(fechaNac),
            altura=str(altura),
            residencia=str(residencia)
        )
        i += 1

    writer.commit()
    print("Fin de indexado", "Se han indexado " + str(i) + " jugadores")

    return True
