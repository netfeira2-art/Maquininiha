import streamlit as st
import socket as s
import os
import time
from DataSet import SQL
from glob import glob
from datetime import datetime

class Motorista:
    
    def __init__(self):
        
        self.IP=s.gethostbyname(s.gethostname())
        
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)        
        
        self.sql=SQL()
        
        self.sql.criateTable()     
        
        pass
    
    
    def main(self):
                
        placeholder=st.empty()
        
        with placeholder.container():
            
            with st.container():
                
                divs=st.columns(3,vertical_alignment='center')
                
                with divs[1].container():
                    
                    with st.container(vertical_alignment='center',horizontal_alignment='center'): 
                    
                        img_path=os.path.join(os.getcwd(),'Imagens','logo.svg')
                        img=glob(img_path)
                        
                        if len(img)>0:                   
                    
                            st.image(img[-1],width=325)
                            
                            pass
                        
                        pass
                    
                    st.markdown('<h2 style="font-family:Arial;color:#16a085;text-align:left;">Controle do Motorista</h2>',unsafe_allow_html=True)
                    
                    st.markdown('<p style="font-family:Arial;color:#7f8c8d;text-align:left;font-size:16px">Controle de entrega de máquininha</p>',unsafe_allow_html=True)
                    
                    st.text_input(label='Código',placeholder='Número da Máquininha',key='codigo_maquininha')
                    
                    st.text_input(label='Motorista',placeholder='Nome do motorista',key='motorista')
                    
                    st.button(label='Salvar',icon=':material/save:',key='btn_save',use_container_width=True,type='primary')
                    
                    st.button(label='Voltar para tela inicial',key='btn_voltar',use_container_width=True,type='tertiary')                                
                    
                    pass
                
                pass
            
            pass
        
        if st.session_state['btn_voltar']:
            
            temp_path=os.path.join(self.path_base,'tela.txt')
            
            os.remove(temp_path)
            
            st.rerun()
            
            pass
        
        if st.session_state['btn_save']:
            
            if st.session_state['codigo_maquininha']=='' and st.session_state['motorista']=='':
                
                img_path=os.path.join(os.getcwd(),'Imagens','error.svg')
                img=glob(img_path)                
                
                self.dialogMSG(mensagem='Preencha os campos em questão.',imagem=img[-1],titulo='Erro')
                
                pass
            
            else:
                
                valor=str(st.session_state['codigo_maquininha']).isdigit()
                
                if valor==False:
                    
                    img_path=os.path.join(os.getcwd(),'Imagens','error.svg')
                    img=glob(img_path)                       
                    
                    self.dialogMSG(mensagem='Número da maquininha inválido.',imagem=img[-1],titulo='Erro')
                    
                    pass
                
                else:
                                        
                    querys={
                        
                        'validar':
                            
                            
                            """
                            
                            SELECT COUNT(*) AS contagem FROM operadoras a
                            WHERE a.codigo={0}
                            
                            """.format(int(st.session_state['codigo_maquininha'])),
                            
                        'insert':
                            
                            """
                            
                            INSERT INTO controle_maquininha (nome_motorista,codigo_maquininha,data_hora) VALUES('{0}',{1},'{2}')
                            
                            """.format(str(st.session_state['motorista']).strip().upper(),int(st.session_state['codigo_maquininha']),datetime.now())
                            
                            
                    }
                    
                    validar=self.sql.codigo(querys['validar'])
                    
                    if validar<=0:
                                                
                        img_path=os.path.join(os.getcwd(),'Imagens','error.svg')
                        img=glob(img_path)                        
                        
                        self.dialogMSG(mensagem='Número da maquininha inválido.',imagem=img[-1],titulo='Erro')
                        
                        pass
                    
                    else:
                        
                        self.sql.save(querys['insert'])
                        
                        mensagem=st.success('Dados salvo com sucesso.')
                        time.sleep(1)
                        mensagem.empty()
                        
                        temp_path=os.path.join(self.path_base,'tela.txt')
                        os.remove(temp_path)
                        
                        st.rerun()                     
                        
                        pass
                    
                    pass
                
                pass
            
            pass
        
        
        pass
    
    @st.dialog(title='Mensagem')
    def dialogMSG(self,mensagem,imagem,titulo):
        
        placeholder=st.empty()
        
        with placeholder.container():
            
            with st.container(vertical_alignment='center',horizontal_alignment='center'):
                
                st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;text-align:center;">{titulo}</p>',unsafe_allow_html=True)
                
                st.image(imagem,width=195)
                
                st.markdown(f'<p style="font-family:Arial;color:#7f8c8d;text-align:center;">{mensagem}</p>',unsafe_allow_html=True)
                
                st.button(label='OK',type='primary',width=195,key='btn_ok')
                
                pass
            
            pass
        
        if st.session_state['btn_ok']:
            
            st.rerun()
            
            pass
        
        pass
    
    
    pass