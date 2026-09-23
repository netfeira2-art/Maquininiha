import streamlit as st
import Telas as gui
import socket as s
import os
from glob import glob
from DataSet import SQL
import time

icon_path=os.path.join(os.getcwd(),'Imagens','*.ico*')
icon=glob(icon_path)

if len(icon)>0:

    st.set_page_config(layout='wide',page_title='Maquininha',page_icon=icon[-1])
    
    pass

else:
    
    st.set_page_config(layout='wide',page_title='Maquininha')
    
    pass

class Login:
    
    
    def __init__(self):
        
        self.IP=s.gethostbyname(s.gethostname())
        
        self.path_base=os.path.join(os.getcwd(),'PC',self.IP)
        os.makedirs(self.path_base,exist_ok=True)
        
        if "usuario" not in st.session_state:
            
            st.session_state.usuario =None
            
            pass          
        
        self.sql=SQL()

        self.sql.criateTable()      
                
        pass
    
    
    def log(self):
        
        temp_path=os.path.join(self.path_base,'*.txt*')
        arquivos=glob(temp_path)
        
        if len(arquivos)>0:
                                    
            with open(arquivos[-1],'r') as file:
                
                tela=file.read()
                
                pass
                            
            if tela=='Motorista':
                
                app=gui.Motorista()
                
                app.main()
                
                pass
            
            elif tela=='Administrador':
                
                if st.session_state.usuario!=None:
                
                    app=gui.Administrador()
                        
                    app.main()
                    
                    pass
                
                else:
                    
                    self.main()
                    
                    pass
                    
                
                pass
            
            pass
        
        else:
        
            self.main()
            
            pass
        
        pass
    
    
    def main(self):
        
        placeholder=st.empty()
        
        with placeholder.container():
                  
            divs=st.columns([1,3,1],vertical_alignment='center')
            
            with divs[1].container():
                
                with st.container():
                    
                    with st.container(vertical_alignment='center',horizontal_alignment='center'): 

                        img_path=os.path.join(os.getcwd(),'Imagens','logo.svg')
                        img=glob(img_path)
                        
                        if len(img)>0:                   
                    
                            st.image(img[-1],width=325)
                            
                            pass
                        
                        pass        
                    
                    st.markdown('<p style="font-family:Arial;">Gestão de patrimônio · frota</p>',unsafe_allow_html=True)
                                                            
                    st.markdown('<h1 style="color:#f1c40f;font-family:Arial;">Uma maquininha.<br>Um responsável.</h1>',unsafe_allow_html=True)
                                        
                    st.markdown('<p style="font-family:Arial;">Controle cada retirada por QR Code e mantenha um histórico completo das entregas.</p>',unsafe_allow_html=True)
                    
                    
                    cols=st.columns(2)
                    
                    with cols[0]:
                    
                        st.button(label='Acessar como motorista',type='primary',key='btn_motorista',use_container_width=True)
                        
                        pass
                    
                    with cols[-1]:
                    
                        st.button(label='Administrador',type='primary',key='btn_adm',use_container_width=True,on_click=self.dialog)
                        
                        pass                    
                                        
                    pass
                
                pass
            
            pass
        
        if st.session_state['btn_motorista']:
            
            temp_path=os.path.join(self.path_base,'tela.txt')
            
            with open(temp_path,'w') as file:
                
                file.write('Motorista')
                
                pass
            
            st.rerun()
            
            pass
        
        pass
    
    @st.dialog(title='Administrador')
    def dialog(self):
        
        placeholder=st.empty()
        
        with placeholder.container():
                        
            st.markdown('<p style="font-family:Arial;font-size:1em;font-weight:bold;">ÁREA RESTRITA</p>',unsafe_allow_html=True)
            
            st.markdown('<p style="font-family:Arial;font-size:2rem;font-weight:bold;">Acesso administrativo</p>',unsafe_allow_html=True)
            
            st.markdown('<p style="font-family:Arial;font-size:1em;color:#7f8c8d;">Entre para gerenciar as maquininhas e o histórico.</p>',unsafe_allow_html=True)
            
            with st.container():
                
                st.text_input('E-mail',key='email')
                st.text_input('Senha',key='senha',type='password')
                
                st.button(label='Entrar no painel',key='btn_conecta',type='primary',use_container_width=True)
                
                pass            
            
            pass
        
        if st.session_state['btn_conecta']:
            
            temp_path=os.path.join(self.path_base,'tela.txt')
            
            querys={
                
                'validar':
                    
                    """
                    
                    SELECT COUNT(*)
                    FROM administrador a
                    WHERE LOWER(a.email)='{0}' and a.senha='{1}'                    
                    
                    """.format(str(st.session_state['email']).strip().lower(),str(st.session_state['senha']).strip())
                    
            }
            
            validar=self.sql.codigo(querys['validar'])
                        
            if validar==0:
                
                mensagem=st.warning('Usuário ou senha não consta em nosso sistema.')
                time.sleep(1)
                mensagem.empty()

                pass
            
            
            else:
                
                st.session_state.usuario= 'ti@demarchibrasil.com.br'
                                        
                with open(temp_path,'w') as file:
                    
                    file.write('Administrador')
                    
                    pass
                
                st.rerun()
                
                pass
            
            pass
        
        pass
    
    pass


if __name__=='__main__':
    
    app=Login()
    
    app.log()
    
    pass