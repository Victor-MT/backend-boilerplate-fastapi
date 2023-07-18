FROM postgres:14.5

# Copie o arquivo de inicialização do banco de dados
ADD init.sql /docker-entrypoint-initdb.d/

# Expõe a porta padrão do Postgres
EXPOSE 5432

# Inicializa o banco de dados do Postgres
CMD ["postgres"]