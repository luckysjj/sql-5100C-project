# run in project dir and open PostgreSQ software
export PG_HOME=/Library/PostgreSQL/16
export PATH=$PATH:$PG_HOME/bin
# execute sql documents using psql
psql -U postgres -d postgres -f DDL.sql
psql -U postgres -d postgres -f Data.sql
