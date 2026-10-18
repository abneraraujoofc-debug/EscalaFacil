import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Gerador de Escala 5x2", page_icon="📅", layout="wide")

st.title("📅 Gerador Automático de Escala 5x2")
st.markdown("Crie escalas de trabalho de forma justa, rápida e sem complicação!")

st.sidebar.header("⚙️ Configurações da Empresa")

modo_operacao = st.sidebar.radio(
    "Escolha o período de funcionamento da empresa:",
    ["Segunda a Sábado (6 dias de operação)", "Segunda a Domingo (7 dias de operação)"]
)

if "Sábado" in modo_operacao:
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
else:
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

st.sidebar.subheader("👥 Cadastro de Funcionários")
lista_nomes = st.sidebar.text_area(
    "Digite os nomes dos funcionários (um por linha):",
    value="Ana\nBruno\nCarlos\nDiana\nEduardo\nFernanda\nGabriel"
)

funcionarios = [nome.strip() for nome in lista_nomes.split("\n") if nome.strip()]

if st.button("🚀 Gerar Escala 5x2", type="primary"):
    if len(funcionarios) < 2:
        st.error("Por favor, adicione pelo menos 2 funcionários para gerar a escala.")
    else:
        escala_resultado = {func: [] for func in funcionarios}
        
        for func in funcionarios:
            folgas = random.sample(dias_semana, 2)
            for dia in dias_semana:
                if dia in folgas:
                    escala_resultado[func].append("FOLGA 😴")
                else:
                    escala_resultado[func].append("TRABALHA 💼")
        
        df_escala = pd.DataFrame(escala_resultado, index=dias_semana).T
        
        st.success(f"Escala gerada com sucesso para modo: **{modo_operacao}**!")
        
        st.subheader("📋 Tabela da Escala Semanal")
        st.dataframe(df_escala, use_container_width=True)
        
        st.subheader("📊 Visão Diária da Equipe")
        cols = st.columns(len(dias_semana))
        for idx, dia in enumerate(dias_semana):
            with cols[idx]:
                trabalham = df_escala[df_escala[dia] == "TRABALHA 💼"].index.tolist()
                folgam = df_escala[df_escala[dia] == "FOLGA 😴"].index.tolist()
                st.metric(label=dia, value=f"{len(trabalham)} em serviço")
                st.caption(f"**Folgam:** {', '.join(folgam) if folgam else 'Ninguém'}")

        csv = df_escala.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Baixar Escala (CSV / Excel)",
            data=csv,
            file_name="escala_trabalho_5x2.csv",
            mime="text/csv"
        )
