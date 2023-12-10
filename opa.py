import sqlite3
def criar_conexao():
    conexao = sqlite3.connect("dados.db")
    return conexao

with criar_conexao() as conexao:
        cursor = conexao.cursor()
        resultado = cursor.execute("""
 DROP TABLE usuario
""")