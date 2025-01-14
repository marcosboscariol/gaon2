import streamlit as st
import os
from crewai_tools import FileReadTool
from langchain_cohere import ChatCohere
from crewai import Agent, Task, Crew
import pandas as pd
from dotenv import load_dotenv
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# Configuração de variáveis de ambiente
os.environ["COHERE_API_KEY"] = 'Sid93B0NN5Vc3luKBnbaD07IYTj93V1HGix5nDEe'
os.environ["SERPER_API_KEY"] = '52d11d82675319c2143361c8584d7af496e78cf4'

# Modelo LLM
llm = ChatCohere(temperature=0.9)

teoria_matriz_ce = '''
O que é Matriz de Causa e Efeito?
Matriz de Causa e Efeito é uma ferramenta que auxilia, através da definição, identificação e priorização de causas, quais são as raízes e seus impactos dentro de um problema.
Esse tipo de matriz possibilita entender o processo sobre o qual está inserido a oportunidade, vulgo problema, de uma maneira mais analítica.
Dessa forma, depois de selecionar as variáveis que mais tem influência no resultado final, podem ser aplicadas outras ferramentas de planejamento e ação, como Brainstorming e Matriz de Força x Impacto, para alcançar uma conclusão mais eficaz e satisfatória.
Como aplicar a Matriz de Causa e Efeito?
As etapas para aplicação da ferramenta Matriz de Causa e Efeito são:
Desenhar as linhas e colunas da matriz;
Definir as saídas do processo (Y´s) que serão utilizados;
Defina um peso de 5 a 10 para cada saída;
Escreva todas as entradas do processo (X´s);
Estabeleça a relação entre cada entrada e cada saída utilizando a seguinte legenda: 0 (não existe correlação), 1 (correlação fraca), 3 (correlação moderada) e 5 (correlação forte.);
Multiplique o valor de cada célula pelo peso de cada saída;
Some os valores da linha para obter a nota final.
Definir as causas mais importantes com base nos maiores valores finais.
Depois disso, faça um ranking com as causas com maior influencia e defina os principais fatores que podem ocasionar essas causas
'''


ramo = st.text_input('Informe a área: ')
setor = st.text_input('Informe o setor: ')
dor = st.text_input('Informe o problema a ser resolvido: ')


agente_ishikawa = Agent(
    role="Consultor de Qualidade",
    goal="Contextualizar a aplicação da ferramenta Ishikawa com os dados do usuario",
    backstory=f"""
    Você é um consultor de qualidade focado na ferramenta Ishikawa
    Seu papel é ajudar o usuario a aplicar a ferramenta Ishikawa
    O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
    """,
    verbose=True,
    llm=llm
)


contextualizar_ishikawa = Task(
    description=(
        f"""
        Gerar uma explicação personalizada sobre a ferramenta Ishikawa para o usuário
        O usuário informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
        """
    ),
    agent=agente_ishikawa,
    expected_output="Contexto e explicação específica sobre a ferramenta Ishikawa para o usuário, para ajuda-lo a realizar a ferramenta Ishikawa",
    llm=llm
)


# Equipe
equipe_introducao_ishikawa = Crew(
    agents=[agente_ishikawa],
    tasks=[contextualizar_ishikawa],
    verbose=True
)

st.title('Diagrama de Ishikawa')
with st.expander('Clique para entender o conceito do Diagrama de Ishikawa'):

    # Inicializa a mensagem apenas se ainda não estiver no session_state
    if "mensagem_ishikawa" not in st.session_state:
        st.session_state.mensagem_ishikawa = None

    # Botão para solicitar ajuda
    if st.button('Solicitar ajuda para explicar o Diagrama de Ishikawa'):
        # Simula a chamada de equipe_introducao_ishikawa.kickoff()
        st.session_state.mensagem_ishikawa = equipe_introducao_ishikawa.kickoff()

    # Mostra a mensagem armazenada no session_state
    if st.session_state.mensagem_ishikawa:
        st.markdown(st.session_state.mensagem_ishikawa)


with st.expander('Clique para solicitar ajuda para classificar os erros'):
    ishikawa_ia_1 = st.text_input('Problema Ishikawa 1')
    ishikawa_ia_2 = st.text_input('Problema Ishikawa 2')
    ishikawa_ia_3 = st.text_input('Problema Ishikawa 3')
    ishikawa_ia_4 = st.text_input('Problema Ishikawa 4')

    agente_ishikawa_ia = Agent(
        role="Consultor de Qualidade",
        goal="Classificar os problemas listados pelo usuario dentro da ferramenta Ishikawa",
        backstory=f"""
    Você é um consultor de qualidade focado na ferramenta Ishikawa
    Seu papel é classificar os problemas listados pelo usuário dentro das categorias da ferramenta Ishikawa, Método, Máquinas, Materiais,  Mão de obra, Medição e Meio ambiente
    O usuario informou que os problemas identificados são {ishikawa_ia_1}, {ishikawa_ia_2}, {ishikawa_ia_3} e {ishikawa_ia_4}
    O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
    """,
        verbose=True,
        llm=llm
    )

    agente_ishikawa_ia = Agent(
        role="Consultor de Qualidade",
        goal="Classificar os problemas listados pelo usuario dentro da ferramenta Ishikawa",
        backstory=f"""
    Você é um consultor de qualidade focado na ferramenta Ishikawa
    Seu papel é classificar os problemas listados pelo usuário dentro das categorias da ferramenta Ishikawa, Método, Máquinas, Materiais,  Mão de obra, Medição e Meio ambiente
    O usuario informou que os problemas identificados são {ishikawa_ia_1}, {ishikawa_ia_2}, {ishikawa_ia_3} e {ishikawa_ia_4}
    O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
    """,
        verbose=True,
        llm=llm
    )

    contextualizar_ishikawa_ia = Task(
        description=(
            f"""
        Gerar uma classificação dos problemas listados pelo usuário dentro das categorias da ferramenta Ishikawa, Método, Máquinas, Materiais,  Mão de obra, Medição e Meio ambiente
        O usuario informou que os problemas identificados são {ishikawa_ia_1}, {ishikawa_ia_2}, {ishikawa_ia_3} e {ishikawa_ia_4}
        O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
        """
        ),
        agent=agente_ishikawa_ia,
        expected_output="Classificação dos problemas listados pelo usuário dentro das categorias da ferramenta Ishikawa",
        llm=llm
    )

    # Equipe
    equipe_introducao_ishikawa_ia = Crew(
        agents=[agente_ishikawa_ia],
        tasks=[contextualizar_ishikawa_ia],
        verbose=True
    )

    # Inicializa a mensagem apenas se ainda não estiver no session_state
    if "classificacao_ishikawa" not in st.session_state:
        st.session_state.classificacao_ishikawa = None

    # Botão para solicitar ajuda
    if st.button('Gerar classificação dos problemas para a ferramenta Ishikawa'):
        # Simula a chamada de equipe_introducao_ishikawa.kickoff()
        st.session_state.classificacao_ishikawa = equipe_introducao_ishikawa_ia.kickoff()

    # Mostra a mensagem armazenada no session_state
    if st.session_state.classificacao_ishikawa:
        st.markdown(st.session_state.classificacao_ishikawa)


with st.expander('Clique para preencher o Diagrama de Ishikawa'):

    with st.container():
        col1, col2, col3 = st.columns(3)

    # Primeira seção (colunas 1 a 3)
    with col1:
        medicao_sihikawa = st.text_input(label="Medição")

    with col2:
        material_ishikawa = st.text_input(label="Material")

    with col3:
        pessoal_ishikawa = st.text_input(label="Pessoal")

    with st.container():
        col4, col5, col6 = st.columns(3)

    # Segunda seção (colunas 4 a 6)
    with col4:
        maquina_ishikawa = st.text_input(label="Máquinas")

    with col5:
        metodo_ishikawa = st.text_input(label="Métodos")

    with col6:
        ambiente_ishikawa = st.text_input(label="Ambiente")

    problema_priorizados_ishikawa = st.multiselect(
        "Selecione um problema priorizado:",  # Rótulo do dropdown
        [medicao_sihikawa, material_ishikawa, pessoal_ishikawa, maquina_ishikawa,
            metodo_ishikawa, ambiente_ishikawa]  # Lista de opções
    )


st.title('Matriz Causa e Efeito')

problemas_priorizados_matriz_ce = None

agente_matriz_ce = Agent(
    role="Consultor de Qualidade",
    goal="Contextualizar a aplicação da ferramenta Matriz Causa e Efeito com os dados do usuario",
    backstory=f"""
    Você é um consultor de qualidade focado na ferramenta Matriz Causa e Efeito
    Seu papel é ajudar o usuario a aplicar a ferramenta Matriz Causa e Efeito
    O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
    Ele também acabou de preencher a ferramenta Ishikawa, e o resultado foram esses possiveis problema: {problema_priorizados_ishikawa}
    Você só deve utilziar esse material para explicar a Matriz Causa e Feito e ajudar o usuario a preenche-la: {teoria_matriz_ce}
    """,
    verbose=True,
    llm=llm
)


contextualizar_matriz_ce = Task(
    description=(
        f"""
        Gerar uma explicação personalizada sobre a ferramenta MAtriz Causa e Efeito para o usuário
        O usuário informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
        O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
        Ele também acabou de preencher a ferramenta Ishikawa, e o resultado foram esses possiveis problema: {problema_priorizados_ishikawa}
        Você só deve utilziar esse material para explicar a Matriz Causa e Feito e ajudar o usuario a preenche-la: {teoria_matriz_ce}
        """
    ),
    agent=agente_matriz_ce,
    expected_output="Contexto e explicação específica sobre a ferramenta Matriz Causa e Efeito para o usuário, para ajuda-lo a realizar a ferramenta Matriz Causa e Efeito",
    llm=llm
)


# Equipe
equipe_introducao_matriz_ce = Crew(
    agents=[agente_matriz_ce],
    tasks=[contextualizar_matriz_ce],
    verbose=True
)

with st.expander('Clique aqui para entender o conceito de Matriz de Causa e Efeito'):
    # Inicializa a mensagem apenas se ainda não estiver no session_state
    if "resultado_introducao_matriz_ce" not in st.session_state:
        st.session_state.resultado_introducao_matriz_ce = None

    if st.button('Explicar o conceito de Matriz Causa e Efeito'):
        st.session_state.resultado_introducao_matriz_ce = equipe_introducao_matriz_ce.kickoff()

    # Mostra a mensagem armazenada no session_state
    if st.session_state.resultado_introducao_matriz_ce:
        st.markdown(st.session_state.resultado_introducao_matriz_ce)

with st.expander('Clique aqui para aplicar a Matriz de Causa e Efeito'):
    if not problema_priorizados_ishikawa:
        st.warning('Para dar sequência, você deve realizar a MAtriz de Ishikawa')
    # Input para número e títulos das colunas
    num_colunas = st.number_input(
        "Quantas colunas você quer?",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    colunas = []
    for i in range(num_colunas):
        colunas.append(st.text_input(
            f"Digite o título da coluna {i + 1}:", value=f"Coluna {i + 1}"))

    # Construção da matriz como DataFrame
    if problema_priorizados_ishikawa and colunas:
        # Adiciona a coluna de resultado
        colunas_com_resultado = colunas + ["Resultado"]
        matriz = pd.DataFrame(
            index=problema_priorizados_ishikawa,
            columns=colunas_com_resultado
        )

        # Permitir edição apenas das colunas configuradas pelo usuário
        st.write("### Matriz Editável (Sem Resultado):")
        matriz_editada = st.data_editor(
            matriz[colunas], use_container_width=True)

        # Atualizar os valores da coluna "Resultado" com a multiplicação das outras colunas
        # Atualiza os valores das colunas editáveis
        matriz[colunas] = matriz_editada

        for index in matriz.index:
            try:
                # Certifique-se de converter os valores para numéricos antes da multiplicação
                numeric_values = pd.to_numeric(
                    matriz.loc[index, colunas], errors="coerce")
                matriz.at[index, "Resultado"] = numeric_values.prod()
            except Exception:
                # Caso haja erro, define como None
                matriz.at[index, "Resultado"] = None

        # Exibir matriz completa com coluna "Resultado"
        st.write("### Matriz Atualizada com Resultado:")
        st.write(matriz)

        st.write("### Priorização de Causas:")
        problemas_priorizados_matriz_ce = st.multiselect('Selecione ',
                                                         problema_priorizados_ishikawa)


st.title('FMEA')


agente_fmea = Agent(
    role="Consultor de Qualidade",
    goal="Contextualizar a aplicação da ferramenta FMEA com os dados do usuario",
    backstory=f"""
    Você é um consultor de qualidade focado na ferramenta FMEA
    Seu papel é ajudar o usuario a aplicar a ferramenta FMEA
    O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
    Ele também acabou de preencher a ferramenta Diagrama de Causa e Efeito, e o resultado foram esses possiveis problema: {problemas_priorizados_matriz_ce}
    """,
    verbose=True,
    llm=llm
)


contextualizar_fmea = Task(
    description=(
        f"""
        Gerar uma explicação personalizada sobre a ferramenta FMEA para o usuário
        O usuário informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
        Ele também acabou de preencher a ferramenta Diagrama de Causa e Efeito, e o resultado foram esses possiveis problema: {problemas_priorizados_matriz_ce}
        """
    ),
    agent=agente_fmea,
    expected_output="Contexto e explicação específica sobre a ferramenta FMEA para o usuário, para ajuda-lo a realizar a ferramenta Matriz Causa e Efeito",
    llm=llm
)


# Equipe
equipe_introducao_fmea = Crew(
    agents=[agente_fmea],
    tasks=[contextualizar_fmea],
    verbose=True
)


with st.expander('Clique aqui para entender o conceito do FMEA'):

    if "resultado_introducao_fmea" not in st.session_state:
        st.session_state.resultado_introducao_fmea = None

    if st.button('Solicitar ajuda para preencher o FMEA'):
        # Inicializa a mensagem apenas se ainda não estiver no session_state
        st.session_state.resultado_introducao_fmea = equipe_introducao_fmea.kickoff()

    if st.session_state.resultado_introducao_fmea:
        st.markdown(st.session_state.resultado_introducao_fmea)


with st.expander('Clique aqui para aplicar o FMEA'):
    modo_falha_priorizado_fmea_1 = st.text_input('Modo Falha FMEA 1')
    modo_falha_priorizado_fmea_2 = st.text_input('Modo Falha FMEA 2')
    modo_falha_priorizado_fmea_3 = st.text_input('Modo Falha FMEA 3')
    modo_falha_priorizado_fmea_4 = st.text_input('Modo Falha FMEA 4')


agente_fmea_modo_falha = Agent(
    role="Consultor de Qualidade",
    goal="Gerar sugestões de controle dos modos de falha priorizados no FMEA",
    backstory=f"""
        Você é um consultor de qualidade focado na ferramenta FMEA
        Seu papel é ajudar o usuario a Gerar sugestões de controle dos modos de falha priorizados no FMEA
        O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
        Ele acabou de aplicar a ferramenta FMEA, e priorizou os sequinbtes modos de falha: {modo_falha_priorizado_fmea_1},{modo_falha_priorizado_fmea_2},{modo_falha_priorizado_fmea_3},{modo_falha_priorizado_fmea_4}
        Agora, quero que gere soluções de controles e indicadores para mitigar ou controlar cada um desses modos de falha
        """,
    verbose=True,
    llm=llm
)


realizar_fmea_modo_falha = Task(
    description=(
        f"""
        Gerar sugestões de controle dos modos de falha priorizados no FMEA
        O usuario informou que o ramo de trabalho dele é {ramo}, o setor com o problema a ser resolvido é o {setor} e o problema específico é {dor}
    Ele acabou de aplicar a ferramenta FMEA, e priorizou os sequinbtes modos de falha: {modo_falha_priorizado_fmea_1},{modo_falha_priorizado_fmea_2},{modo_falha_priorizado_fmea_3},{modo_falha_priorizado_fmea_4}
    Agora, quero que gere soluções de controles e indicadores para mitigar ou controlar cada um desses modos de falha
    """),
    agent=agente_fmea_modo_falha,
    expected_output="Sugestões de controle dos modos de falha priorizados no FMEA",
    llm=llm
)


# Equipe
equipe_fmea_modo_falha = Crew(
    agents=[agente_fmea_modo_falha],
    tasks=[realizar_fmea_modo_falha],
    verbose=True
)

with st.expander('Clique aqui para obter sugestões controle dos modos de falha priorizados no FMEA'):
    # Inicializa a mensagem apenas se ainda não estiver no session_state
    if "resultado_fmea_modo_falha" not in st.session_state:
        st.session_state.resultado_fmea_modo_falha = None

    # Botão para solicitar ajuda
    if st.button('Solicitar sugestões de indicadores para controlar os Modos de Falha'):
        # Simula a chamada de equipe_introducao_ishikawa.kickoff()
        st.session_state.resultado_fmea_modo_falha = equipe_fmea_modo_falha.kickoff()

    # Mostra a mensagem armazenada no session_state
    if st.session_state.resultado_fmea_modo_falha:
        st.markdown(st.session_state.resultado_fmea_modo_falha)
