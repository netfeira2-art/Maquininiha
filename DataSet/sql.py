import sqlite3
import pandas as pd

class SQL:
    
    def conecta(self):
        
        try:
            
            conecta=sqlite3.connect('MOINHO.db')
            
            return conecta
            
            pass
        
        except:
            
            print('Sem Conexão')
            
            pass
        
        pass
    
    
    def criateTable(self):
        
        querys={
                        
            'admin':
                                
                """
                
                CREATE TABLE IF NOT EXISTS administrador (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    senha VARCHAR(255) NOT NULL
                );                
                
                """,
                            
            'maquina':
                
                """
                        
                CREATE TABLE IF NOT EXISTS operadoras (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao VARCHAR(255) NOT NULL,
                    operadora VARCHAR(100),
                    status BOOLEAN NOT NULL DEFAULT 1,
                    reservado BOOLEAN NOT NULL DEFAULT 0,
                    numero_maquininha VARCHAR(50)
                );
                            
                """,
                
            'controle':
                
                """
                                
                CREATE TABLE IF NOT EXISTS controle_maquininha (
                    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_motorista VARCHAR(255) NOT NULL,
                    codigo_maquininha INTEGER NOT NULL,
                    data_hora DATETIME NOT NULL DEFAULT (DATETIME('now', 'localtime')),

                    FOREIGN KEY (codigo_maquininha)
                        REFERENCES operadoras(codigo)
                );               
                
                
                """,                
                                
            'historico':
                
                """
                
                CREATE TABLE IF NOT EXISTS historico_maquininha (
                    codigo INTEGER NOT NULL,
                    nome_motorista VARCHAR(255) NOT NULL,
                    codigo_maquininha INTEGER NOT NULL,
                    data_hora DATETIME NOT NULL,
                    
                    FOREIGN KEY (codigo_maquininha)
                        REFERENCES operadoras(codigo)
                );
                
                """,
                
            'trigger_insert_operadora':
                
                """
                
                CREATE TRIGGER IF NOT EXISTS trg_reservar_maquininha
                AFTER INSERT ON controle_maquininha
                FOR EACH ROW
                BEGIN

                    UPDATE operadoras
                    SET reservado = 1
                    WHERE codigo = NEW.codigo_maquininha;

                END;                                
                
                """,
                
            'insert_admin':
                
                """
                
                INSERT INTO administrador (
                    email,
                    senha
                )
                SELECT
                    'ti@demarchibrasil.com.br',
                    'admin123#NET'
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM administrador
                    WHERE email = 'ti@demarchibrasil.com.br'
                );                                
                
                """,
                
            'trg_troca_motorista_before_insert':
                
                """

                CREATE TRIGGER IF NOT EXISTS trg_troca_motorista_before_insert
                BEFORE INSERT ON controle_maquininha
                FOR EACH ROW
                WHEN EXISTS (
                    SELECT 1
                    FROM controle_maquininha
                    WHERE codigo_maquininha = NEW.codigo_maquininha
                )
                BEGIN

                    -- Salva o motorista anterior no histórico
                    INSERT INTO historico_maquininha (
                        codigo,
                        nome_motorista,
                        codigo_maquininha,
                        data_hora
                    )
                    SELECT
                        codigo,
                        nome_motorista,
                        codigo_maquininha,
                        DATETIME('now', 'localtime')
                    FROM controle_maquininha
                    WHERE codigo_maquininha = NEW.codigo_maquininha;

                    -- Remove o motorista anterior
                    DELETE FROM controle_maquininha
                    WHERE codigo_maquininha = NEW.codigo_maquininha;

                END;               
                
                """,
                
            'trg_controle_insert_historico':
                
                """

                CREATE TRIGGER IF NOT EXISTS trg_controle_insert_historico
                AFTER INSERT ON controle_maquininha
                FOR EACH ROW
                BEGIN

                    INSERT INTO historico_maquininha (
                        codigo,
                        nome_motorista,
                        codigo_maquininha,
                        data_hora
                    )
                    VALUES (
                        NEW.codigo,
                        NEW.nome_motorista,
                        NEW.codigo_maquininha,
                        NEW.data_hora
                    );

                END;                
                
                """,
                
                
            'unico':
                
                """
                
                CREATE UNIQUE INDEX IF NOT EXISTS
                idx_controle_maquininha_unica
                ON controle_maquininha (codigo_maquininha);                
                
                """,
                
            'trg_controle_delete_historico':
                
                """
                
                CREATE TRIGGER IF NOT EXISTS trg_controle_delete_historico
                BEFORE DELETE ON controle_maquininha
                FOR EACH ROW
                BEGIN

                    INSERT INTO historico_maquininha (
                        codigo,
                        nome_motorista,
                        codigo_maquininha,
                        data_hora
                    )
                    VALUES (
                        OLD.codigo,
                        OLD.nome_motorista,
                        OLD.codigo_maquininha,
                        DATETIME('now', 'localtime')
                    );

                    UPDATE operadoras
                    SET reservado = 0
                    WHERE codigo = OLD.codigo_maquininha;

                END;                
                
                """,
                
            'trg_limpar_historico_365_dias':
                
                """
                
                CREATE TRIGGER IF NOT EXISTS trg_limpar_historico_365_dias
                AFTER INSERT ON historico_maquininha
                FOR EACH ROW
                BEGIN

                    DELETE FROM historico_maquininha
                    WHERE data_hora < DATETIME('now', 'localtime', '-365 days');

                END;      
                
                """
                
                
                
                
                
            
        }
        
        with self.conecta() as conecta:
            
            cursor=conecta.cursor()
            
            for query in querys.values():
            
                cursor.execute(query)
                
                pass
            
            pass
        
        pass
    
    
    def codigo(self,query):
        
        with self.conecta() as conecta:
            
            cursor=conecta.cursor()
            
            cursor.execute(query)
            
            codigo=[l for l in cursor.fetchone()]
            
            pass
        
        return codigo[-1]       
        
        pass
    
    
    def save(self,query):
        
        with self.conecta() as conecta:
            
            cursor=conecta.cursor()
            
            cursor.execute(query)
                        
            pass
        
        
        pass
    
    
    def dfDados(self):
        
        df=dict()
        
        querys={
            
            'operadoras':
                
                """
                
                SELECT * FROM operadoras
                
                """,
                
            'controle':
                
                """
                
                SELECT a.codigo_maquininha AS codigo,a.nome_motorista,a.data_hora 
                FROM (

                SELECT a.codigo,a.codigo_maquininha,a.nome_motorista,a.data_hora,
                MAX(a.codigo)OVER(PARTITION BY  a.codigo_maquininha) AS codigo_max
                FROM controle_maquininha a

                )a
                INNER JOIN operadoras b ON a.codigo_maquininha=b.codigo AND b.reservado=1
                WHERE a.codigo=a.codigo_max
                
                """
               
                
        }
        
        with self.conecta() as conecta:
                        
            for tabela,query in querys.items():
                
                df[tabela]=pd.read_sql(query,conecta)
                
                pass
            
            pass
        
        return df        
        
        pass
    
    
    def dfFrame(self,querys:dict,tabela:list):
        
        df=dict()
                        
        with self.conecta() as conecta:
            
            for tab in tabela:
                
                df[tab]=pd.read_sql(querys[tab],conecta)
                
                pass
            
            pass
        
        return df        
        
        pass
    
    
    pass