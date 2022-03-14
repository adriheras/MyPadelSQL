# MyPadelSQL
El objetivo de este proyecto era obtener los datos de la página web de World Padel
Tour, el circuito de pádel más popular que existe en la actualidad. Dado que esta
página solo muestra un ranking básico de los jugadores, creo que es una
oportunidad genial para crear una web que obtenga esos datos y los manipule para
crear funciones que aportan realmente valor al usuario y que no están disponibles
en la página oficial. Para ello, se han obtenido los datos de la página. Primero
haciendo scroll con Selenium ya que el contenido de https://www.worldpadeltour.com/jugadores?ranking=masculino se genera
dinámicamente. Después, una vez generado el contenido, se hace uso de
Beautifulsoup para realizar el scraping y así cargar tanto la base de atos como el
índice de Whoosh. Hecho esto, hemos implementado una serie de funcionalidades
usando las queries de Django y de Whoosh, para establecer búsquedas, listados y
filtros con los que gracias a ellos podemos obtener resultados en muy poco tiempo.
