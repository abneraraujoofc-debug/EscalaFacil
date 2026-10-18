import streamlit as st
import pandas as pd
import random
import calendar
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Escala Fácil 5x2 - Gestão por Setor", 
    page_icon="🏢", 
    layout="wide"
)

# Visual moderno
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E293B; text-align: center; }
    .sub-title { font-size: 14px; color: #64748B; text-align: center; margin-bottom: 20px; }
    .sector-badge { 
        background-color: #EFF6FF; 
        color: #1D4ED8; 
        padding: 8px 16px; 
        border-radius: 8px; 
        font-weight: bold; 
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏢 Gestor de Escala Mensal por Setor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Crie e edite escalas organizadas para a sua área de trabalho</div>', unsafe_allow_html=True)

# Painel Lateral - Informações da Empresa e Setor
st.sidebar.header("🏬 Identificação do Setor")

setores_padrao = ["Mercearia", "Friambria / Frios", "Açougue", "Padaria", "Frente de Caixa", "Hortifrúti", "Outro (Personalizado)"]
setor_selecionado = st.sidebar.selectbox("Selecione o seu Setor / Área:", setores_padrao)

if setor_selecionado == "Outro (Personalizado)":
    nome_setor = st.sidebar.text_input("Digite o nome do seu setor:", value="Almoxarifado")
else:
    nome_setor = setor_selecionado

encarregado = st.sidebar.text_input("Nome do Encarregado / Gerente:", value="João Silva")

st.sidebar.divider()
st.sidebar.header("📅 Período da Escala")

ano_atual = datetime.now().year
mes_selecionado = st.sidebar.selectbox("Mês:", list(range(1, 13)), index=datetime.now().month - 1)
ano_selecionado = st.sidebar.number_input("Ano:", min_value=2024, max_value=2030, value=ano_atual)

# Identificar dias do mês
num_dias = calendar.monthrange(ano_selecionado, mes_selecionado)[1]
dias_mes = [f"{dia:02d}/{mes_selecionado:02d}" for dia in range(1, num_dias + 1)]

st.sidebar.divider()
st.sidebar.subheader(f"👥 Colaboradores do Setor ({nome_setor})")
lista_nomes = st.sidebar.text_area(
    "Nomes dos funcionários deste setor (um por linha):",
    value="Carlos Eduardo\nMariana Santos\nLucas Ferreira\nFernanda Lima",
    height=140
)

funcionarios = [nome.strip() for nome in lista_nomes.split("\n") if nome.strip()]

# Destaque do Setor na Tela
st.markdown(f'<div class="sector-badge">📍 Setor: {nome_setor.upper()} | Encarregado(a): {encarregado}</div>', unsafe_allow_html=True)

# Botão de Geração
if st.button("⚡ Gerar Escala do Setor", type="primary"):
    if len(funcionarios) < 1:
        st.error("⚠️ Cadastre pelo menos 1 colaborador para gerar a escala.")
    else:
        dados = {}
        for func in funcionarios:
            escala_func = []
            for dia in range(1, num_dias + 1):
                if dia % 7 in [0, 6]: 
                    escala_func.append("FOLGA")
                else:
                    escala_func.append("TRABALHA")
            random.shuffle(escala_func)
            dados[func] = escala_func
            
        df_base = pd.DataFrame(dados, index=dias_mes).T
        st.session_state['df_escala'] = df_base
        st.session_state['setor_atual'] = nome_setor
        st.success(f"Escala de {nome_setor} gerada com sucesso para {mes_selecionado}/{ano_selecionado} ({num_dias} dias)!")

# Área de Edição e Visualização
if 'df_escala' in st.session_state:
    st.subheader(f"✏️ Tabela de Escala Mensal - {st.session_state.get('setor_atual', nome_setor)}")
    st.info("💡 **Edição livre:** Você pode clicar em qualquer célula abaixo para alterar de 'TRABALHA' para 'FOLGA' ou ajustar conforme a necessidade da sua equipe!")
    
    # Tabela Editável
    df_editado = st.data_editor(
        st.session_state['df_escala'],
        use_container_width=True,
        num_rows="fixed"
    )
    
    # Resumo de Totais
    st.subheader("📊 Totais de Dias Trabalhados e Folgas")
    totais = []
    for func in df_editado.index:
        linha = df_editado.loc[func]
        trabalhos = (linha == "TRABALHA").sum()
        folgas = (linha == "FOLGA").sum()
        totais.append({
            "Setor": nome_setor,
            "Colaborador": func, 
            "Dias Trabalhados": trabalhos, 
            "Total de Folgas": folgas
        })
    
    df_totais = pd.DataFrame(totais)
    st.dataframe(df_totais, use_container_width=True)

    # Resumo Formatado para WhatsApp do Setor
    st.subheader("📲 Resumo do Setor para o WhatsApp")
    texto_whats = f"*ESCALA MENSAL - SETOR {nome_setor.upper()}*\n"
    texto_whats += f"Encarregado: {encarregado} | Mês: {mes_selecionado}/{ano_selecionado}\n\n"
    for func in df_editado.index:
        linha = df_editado.loc[func]
        dias_folga = [dia for dia in linha.index if linha[dia] == "FOLGA"]
        texto_whats += f"👤 *{func}:* Folgas nos dias -> {', '.join(dias_folga)}\n"
        
    st.code(texto_whats, language="markdown")

    # Exportar
    st.subheader("📥 Exportar Relatório do Setor")
    csv = df_editado.to_csv().encode('utf-8')
    st.download_button(
        label=f"📄 Baixar Escala ({nome_setor}) em Excel/CSV",
        data=csv,
        file_name=f"escala_{nome_setor.lower().replace(' ', '_')}_{mes_selecionado}_{ano_selecionado}.csv",
        mime="text/csv"
    )
