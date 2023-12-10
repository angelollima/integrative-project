SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS produto (
    id           INTEGER         PRIMARY KEY AUTOINCREMENT,
    nome         TEXT            NOT NULL,
    preco        INTEGER         NOT NULL,
    descricao    TEXT            NOT NULL,
    categoria    TEXT            NOT NULL
    )
"""

SQL_INSERIR = """
    INSERT INTO produto (nome, preco, descricao, categoria)
    VALUES (?, ?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE produto
    SET nome=?, preco=?, descricao=?, categoria=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM produto
    WHERE id=?
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, preco, descricao, categoria
    FROM produto
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, preco, descricao, categoria
    FROM produto
    WHERE id=?
"""