import streamlit as st
import socket as s
import os
from glob import glob
from DataSet import SQL
import time

class Administrador:
    
    def __init__(self):
        
        self.IP=s.gethostbyname(s.gethostname())
        
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)
        
        if "usuario" not in st.session_state:
            
            st.session_state.usuario ='ti@demarchibrasil.com.br'
            
            pass
        
        st.session_state.usuario= 'ti@demarchibrasil.com.br'
                                     
        self.sql=SQL()
        
        self.sql.criateTable()
                                
        pass    
    
    def main(self):
        
        placeholder=st.empty()
        
        with placeholder.container():
            
            #sqlite
            with st.container():
                
                querys={
                    
                    'contagem':
                        
                        """
                        
                        SELECT COUNT(*) AS Contagem
                        FROM operadoras a                        
                        
                        """,
                        
                    'usado':
                        
                        """
                        
                        SELECT COUNT(*) AS Contagem
                        FROM operadoras a
                        WHERE a.reservado=1                     
                        
                        """,
                        
                    'disponivel':
                        
                        """
                        
                        SELECT COUNT(*) AS Contagem
                        FROM operadoras a
                        WHERE a.reservado=0                 
                        
                        """,                        
                        
                    'baixado':
                        
                        """
                        
                        SELECT COUNT(*) AS [Contagem]
                        FROM historico_maquininha AS a
                        WHERE DATE(a.data_hora) = DATE('now', 'localtime');                        
                        
                        """,
                        
                    'admin':
                        
                        """
                        
                        SELECT a.email 
                        FROM administrador a
                        WHERE a.codigo=1                        
                        
                        """
                        
                                              
                        
                }
                
                cadastros=self.sql.codigo(querys['contagem'])
                cadastros='0'*len(str(cadastros))+str(cadastros) if len(str(cadastros))==1 else cadastros
                
                disponivel=self.sql.codigo(querys['disponivel'])
                disponivel='0'*len(str(disponivel))+str(disponivel) if len(str(disponivel))==1 else disponivel                
                
                usado=self.sql.codigo(querys['usado'])
                usado='0'*len(str(usado))+str(usado) if len(str(usado))==1 else usado
                
                baixado=self.sql.codigo(querys['baixado'])
                baixado='0'*len(str(baixado))+str(baixado) if len(str(baixado))==1 else baixado
                
                usuario=self.sql.codigo(querys['admin'])
                                      
                
                pass            
                        
            with st.container():
                                
                divs=st.columns(2,vertical_alignment='top')
                
                with divs[0].container():
            
                    st.markdown('<h1 style="font-family:Arial;font-size:2.5rem;color:#16a085;">Maquininhas</h1>',unsafe_allow_html=True)
                    
                    st.markdown('<p style="font-family:Arial;font-size:16px;color:#7f8c8d;">Gere QR Codes, acompanhe responsáveis e dê baixa nas entregas.</p>',unsafe_allow_html=True)
                    
                    st.button(label='Atualizar',icon=':material/refresh:',type='primary',key='btn_refresh',width=195)
                    
                    if st.session_state['btn_refresh']:
                        
                        st.rerun()
                        
                        pass                    
                    
                    pass
                
                with divs[-1].container(horizontal_alignment='right'):
            
                    st.markdown('<h1 style="font-family:Arial;font-size:14px;color:#16a085;text-align:right;">ADMINISTRADOR</h1>',unsafe_allow_html=True)
                    
                    st.markdown(f'<p style="font-family:Arial;font-size:16px;color:#7f8c8d;text-align:right;">email: {usuario}</p>',unsafe_allow_html=True)
                    
                    st.button(label='Sair',icon=':material/arrow_back:',type='primary',key='btn_sair',width=195)
                    
                    pass
                
                st.markdown('----')
                
                pass
                    
            #cards
            with st.container():
                
                cards=st.columns(3,vertical_alignment='center')
                
                with cards[0].container(border=True):
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;font-size:12px;">DISPONÍVEIS</p>',unsafe_allow_html=True)
                    
                    st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;font-size:45px;font-weight:bold;color:#16a085;">{disponivel}</p>',unsafe_allow_html=True)
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;font-size:12px;">prontas para vínculo</p>',unsafe_allow_html=True)
                    
                    pass
                
                with cards[1].container(border=True):
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;font-size:12px;">EM USO</p>',unsafe_allow_html=True)
                    
                    st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;font-size:45px;font-weight:bold;color:#f1c40f;">{usado}</p>',unsafe_allow_html=True)
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;font-size:12px;">vinculadas a motoristas</p>',unsafe_allow_html=True)
                    
                    pass
                
                with cards[-1].container(border=True):
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;font-size:12px;">BAIXAS HOJE</p>',unsafe_allow_html=True)
                    
                    st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;font-size:45px;font-weight:bold;color:#c0392b;">{baixado}</p>',unsafe_allow_html=True)
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;font-size:12px;">entregas finalizadas</p>',unsafe_allow_html=True)
                    
                    pass                                
                
                pass
            
            with st.container():
                
                divs=st.columns([4,2],vertical_alignment='top')
                
                with divs[0].container():
                    
                    tags=st.columns(2)
                    
                    with tags[0]:
                    
                        st.markdown(f'<h3 style="font-family:Arial;padding:0px;margin:0px;">Maquininhas<h3><p style="font-family:Arial;padding:0px;margin:0px;font-size:16px">{cadastros} cadastradas<p>',unsafe_allow_html=True)
                        
                        pass
                    
                    with tags[-1]:
                    
                        cols=st.columns(2,vertical_alignment='bottom')
                    
                        with cols[0]:
                    
                            st.text_input(label='Buscar',placeholder='Buscar',label_visibility='hidden',key='txt_buscar')
                            
                            pass
                        
                        with cols[-1]:
                    
                            st.button(label='Cadastrar',icon=":material/receipt_long:",type='primary',key='btn_cad',on_click=self.dialogMaquinas)
                            
                            pass                
                        
                        pass                    
                    
                    with st.container():
                        
                        df=self.sql.dfDados()
                        
                        df['operadoras']=df['operadoras'] if st.session_state['txt_buscar']=='' else df['operadoras'].loc[(df['operadoras']['descricao'].str.contains(str(st.session_state['txt_buscar']).strip().upper()))|(df['operadoras']['numero_maquininha'].str.contains(str(st.session_state['txt_buscar']).strip().upper()))]
                        
                        df['operadoras']=df['operadoras'].merge(df['controle'],on='codigo',how='left')
                        df['operadoras'].loc[df['operadoras']['nome_motorista'].isnull(),'nome_motorista']='sem vínculo'
                        
                        for index,row in df['operadoras'].iterrows():
                            
                            with st.container(border=True):
                            
                                cols=st.columns(2,vertical_alignment='center')
                                
                                with cols[0]:
                                
                                    status='Disponível' if row['reservado']==0 else 'Indisponível'
                                    
                                    motorista=str(row['nome_motorista']).strip().title()
                                    
                                    disabled=True if row['reservado']==0 else False
                                    
                                    st.markdown(f'<h4>{row["descricao"]} - {row["operadora"]}</h4>',unsafe_allow_html=True)
                                    
                                    st.markdown(f'<h5>POS: {row["numero_maquininha"]}</h5>',unsafe_allow_html=True)
                                    
                                    st.markdown(f'<p style="color:#7f8c8d;font-size:16px">{status} - {motorista}</p>',unsafe_allow_html=True)
                                    
                                    pass
                                
                                with cols[-1].container(horizontal_alignment='right'):
                                    
                                    botoes=st.columns(2)
                                    
                                    with botoes[0]:
                                
                                        st.button(label='Editar',icon=":material/edit:",type='primary',use_container_width=True,key=row['codigo'])
                                        
                                        if st.session_state[row['codigo']]:
                                            
                                            self.dialogEdit(row['codigo'])
                                            
                                            pass
                                                                                                                        
                                        pass                                                           
                                    
                                    with botoes[-1]:
                                                                            
                                        st.button(label='Baixar',icon=":material/download_done:",type='primary',use_container_width=True,key=f"baixa_{row['codigo']}",disabled=disabled)
                                        
                                        if st.session_state[f"baixa_{row['codigo']}"]==True:
                                            
                                            querys['delete']="""
                                                                                        
                                            DELETE FROM controle_maquininha
                                            WHERE codigo_maquininha = {0};                                                                                        
                                            
                                            """.format(row['codigo'])
                                            
                                            self.sql.save(querys['delete'])
                                            
                                            st.rerun()                                          
                                            
                                            pass
                                        
                                        pass
                                    
                                    pass
                                
                                pass
                            
                            pass
                        
                        pass
                    
                    pass
                
                with divs[-1].container():
                    
                    st.markdown('<h4>Histórico recente</h4>',unsafe_allow_html=True)
                    
                    with st.container():
                    
                        cols=st.columns(2)
                        
                        with cols[0]:
                        
                            st.date_input(label='Data Inicial',key='dt_inicial',format='DD/MM/YYYY')
                            
                            pass
                        
                        with cols[-1]:
                        
                            st.date_input(label='Data Final',key='dt_final',format='DD/MM/YYYY')
                            
                            pass
                        
                        pass
                    
                    querys={
                        
                        'historico':
                            
                            """
                            
                            SELECT
                                b.codigo,
                                b.descricao,
                                b.operadora,
                                b.numero_maquininha,
                                a.codigo AS id,
                                a.nome_motorista,
                                STRFTIME('%d/%m/%Y %H:%M:%S', a.data_hora) AS data_hora
                            FROM historico_maquininha AS a
                            INNER JOIN operadoras AS b
                                ON a.codigo_maquininha = b.codigo
                            WHERE DATE(a.data_hora) BETWEEN '{0}' AND '{1}'                            
                            
                            """.format(st.session_state['dt_inicial'],st.session_state['dt_final'])
                            
                    }
                   
                    df=self.sql.dfFrame(querys,tabela=['historico'])
                    
                    for id in df['historico']['id'].unique().tolist():
                        
                        with st.container(border=True):
                            
                            df['temp']=df['historico'].loc[df['historico']['id']==id]
                            
                            maquininha=df['temp']['descricao'].unique().tolist()[-1]
                            operadora=df['temp']['operadora'].unique().tolist()[-1]
                            motorista=df['temp']['nome_motorista'].unique().tolist()[-1]
                            
                            st.markdown(f'<h4 style="font-family:Arial;">{maquininha} - {operadora}</h4>',unsafe_allow_html=True)
                            
                            st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;">Motorista: {str(motorista).title()}</p>',unsafe_allow_html=True)
                    
                            for index,row in df['temp'].iterrows():
                                
                                st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;font-size:14px;">Data & Hora: {row["data_hora"]}</p>',unsafe_allow_html=True)                                
                                
                                pass
                            
                            pass
                        
                        pass              
                    
                    pass
                
                pass
                        
            pass
        
        
        if st.session_state['btn_sair']:
            
            temp_path=os.path.join(self.path_base,'tela.txt')
            
            os.remove(temp_path)
            
            st.rerun()
            
            pass
        
        pass
    
    @st.dialog(title='Cadastrar Maquininha')
    def dialogMaquinas(self):
        
        placeholder=st.empty()
        
        querys={
            
            'codigo':
                
                
                """
                
                SELECT COUNT(a.codigo)+1 AS [codigo]
                FROM operadoras a                
                
                """
                
                
        }
        
        codigo=self.sql.codigo(querys['codigo'])
        var=('0'*len(str(codigo)))+str(codigo) if len(str(codigo))==1 else codigo
                
        text_placeholder=f'MC0{var}'
                
        with placeholder.container():
            
            st.text_input(label='Código',placeholder=text_placeholder,key='txt_codigo')
            
            st.text_input(label='Operadora',placeholder='Rede,Cielo,Stone...',key='txt_operadora')
            
            st.text_input(label='POS',placeholder='Numeração da Máquininha',key='txt_numero')
            
            st.button(label='Salvar Maquininha',key='btn_save',type='primary',use_container_width=True)
            
            pass
        
        if st.session_state['btn_save']:
            
            if st.session_state['txt_codigo']!='' and st.session_state['txt_operadora']!='' and st.session_state['txt_numero']!='':
            
                querys['validar']="""
                
                SELECT COUNT(*) AS contagem
                FROM operadoras a
                WHERE a.numero_maquininha='{0}'                
                
                
                """.format(str(st.session_state['txt_numero']).strip().upper())
                
                validar=self.sql.codigo(querys['validar'])
                
                if validar>0:
                    
                    mensagem=st.err('Código da máquininha já consta cadastrado.')
                    time.sleep(1)
                    mensagem.empty()                    
                    
                    pass
                
                
                else:            
            
                    querys['insert']="""
                    
                    INSERT INTO operadoras (descricao, operadora, status,numero_maquininha)
                    VALUES ('{0}', '{1}', 1,'{2}');                        
                    
                    """.format(str(st.session_state['txt_codigo']).strip().upper(),str(st.session_state['txt_operadora']).strip().upper(),str(st.session_state['txt_numero']).strip().upper())
                    
                    
                    self.sql.save(querys['insert'])
                    
                    mensagem=st.success('Dados salvo com sucesso')
                    time.sleep(1)
                    mensagem.empty()
                    
                    st.rerun()
                    
                    pass
                
                pass
            
            else:
                
                mensagem=st.warning('Preencha os campos para prosseguir.')
                time.sleep(1)
                mensagem.empty()
                
                pass
            
            pass
        
        pass
    
    @st.dialog(title='Editar Maquininha')
    def dialogEdit(self,codigo):
        
        querys={
            
            'operadora':
                
                """
                
                SELECT a.codigo,a.descricao,a.operadora,a.numero_maquininha 
                FROM operadoras a
                WHERE a.codigo={0}                
                
                """.format(codigo)         
                
        }
                      
        df=self.sql.dfFrame(querys,tabela=['operadora'])
        
        maquininha=df['operadora']['descricao'].unique().tolist()[-1]
        operadora=df['operadora']['operadora'].unique().tolist()[-1]
        numero=df['operadora']['numero_maquininha'].unique().tolist()[-1]
        
        placeholder=st.empty()
        
        with placeholder.container():
            
            st.text_input(label='Código',placeholder=maquininha,key='edit_codigo')
            
            st.text_input(label='Operadora',placeholder=operadora,key='edit_operadora')
            
            st.text_input(label='POS',placeholder=numero,key='edit_numero')
            
            st.button(label='Salvar Maquininha',key='edit_save',type='primary',use_container_width=True)
                        
            pass
        
        if st.session_state['edit_save']:
            
            querys={
                
                'update':
                                                            
                    """
                    UPDATE operadoras
                    SET
                        descricao = COALESCE(NULLIF('{1}', ''), descricao),
                        operadora = COALESCE(NULLIF('{2}', ''), operadora),
                        numero_maquininha = COALESCE(NULLIF('{3}', ''), numero_maquininha)
                    WHERE codigo = {0}
                    
                    """.format(
                    codigo,
                    str(st.session_state['edit_codigo']).strip().upper(),
                    str(st.session_state['edit_operadora']).strip().upper(),
                    str(st.session_state['edit_numero']).strip().upper()
                    
                    )                 
                    
            }
            
            self.sql.save(querys['update'])
            
            mensagem=st.success('Dados editados com sucesso.')
            time.sleep(1)
            mensagem.empty()
            
            st.rerun()
            
            pass 
        
        pass
        
    pass