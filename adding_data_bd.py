# Imports
from sqlalchemy import create_engine

# Creates connection with the SQLite Database
engine = create_engine('sqlite:///data/database.db', echo=False)

#Tabela Música
with engine.connect() as con:
  con.execute(
    """
    INSERT or REPLACE INTO Musica(track_nome, url, img)
    SELECT track, url, img from charts
    """)

#Tabela Artista
with engine.connect() as con:
  con.execute(
    """
    INSERT or REPLACE INTO Artista(nome_artistico)
    SELECT artist from charts
    """)

#Tabela País
with engine.connect() as con:
  con.execute(
    """
    INSERT or REPLACE INTO Paises(pais)
    SELECT country from charts
    """)

#Tabela Musicas_Artistas
with engine.connect() as con:
  con.execute(
    """
    INSERT or REPLACE INTO Musicas_Artistas(fk_track_nome, fk_nome_artistico)
    SELECT track, artist from charts
    """)

#Tabela Musica_Charts_Paises
with engine.connect() as con:
  con.execute(
    """
    INSERT or REPLACE INTO Musicas_Charts_Paises(fk_track_nome, fk_pais, posicao, streams)
    SELECT track, country, position, streams from charts
    """)

#DROP TABLE CHARTS
with engine.connect() as con:
  con.execute(
    """
    DROP TABLE charts
    """)