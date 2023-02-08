from sqlalchemy import create_engine

# Creates connection with the SQLite Database
engine = create_engine('sqlite:///data/database.db', echo=False)

with engine.connect() as con:
  con.execute(
    """
    CREATE TABLE Musica(
      track_nome VARCHAR,
      url VARCHAR,
      img VARCHAR,
      PRIMARY KEY(track_nome)
    );
    """)

with engine.connect() as con:
  con.execute(
    """
    CREATE TABLE Artista(
      nome_artistico VARCHAR,
      PRIMARY KEY(nome_artistico)
    );
    """)

with engine.connect() as con:
  con.execute(
    """
    CREATE TABLE Paises(
      pais VARCHAR,
      PRIMARY KEY(pais)
    );
    """)

with engine.connect() as con:
  con.execute(
    """
    CREATE TABLE Musicas_Artistas(
      fk_track_nome VARCHAR,
      fk_nome_artistico VARCHAR,
      FOREIGN KEY(fk_nome_artistico) REFERENCES Artista(nome_artistico),
      FOREIGN KEY(fk_track_nome) REFERENCES Musica(track_nome),
      PRIMARY KEY(fk_track_nome, fk_nome_artistico)
    );
    """)

with engine.connect() as con:
  con.execute(
    """
    CREATE TABLE Musicas_Charts_Paises(
      fk_track_nome VARCHAR,
      fk_pais VARCHAR,
      posicao INTEGER,
      streams NUMERIC,
      FOREIGN KEY(fk_track_nome) REFERENCES Musica(track_nome),
      FOREIGN KEY(fk_pais) REFERENCES Paises(pais),
      PRIMARY KEY(fk_track_nome, fk_pais)
    );
    """)
