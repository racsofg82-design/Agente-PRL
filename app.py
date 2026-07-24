"""Interfaz Streamlit"""
import streamlit as st
import pandas as pd
import PyPDF2
import json
from workflow import execute_prl_workflow
from config import GOODMAN_PMP_RULES

st.set_page_config(page_title="Agente PRL Senior", page_icon="👷‍♂️", layout="wide")

st.title("👷‍♂️ Agente PRL Senior")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("️ Configuración")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        import os
        os.environ["OPENAI_API_KEY"] = api_key

# Tabs
tab1, tab2, tab3 = st.tabs(["📄 Documentos", "🏗️ Actividad", "📊 Resultados"])

with tab1:
    pss_file = st.file_uploader("PSS/RAMS (PDF)", type=["pdf"])
    pmp_file = st.file_uploader("PMP Cliente (PDF)", type=["pdf"])

with tab2:
    actividad = st.text_input("Nombre de la actividad")
    ubicacion = st.text_input("Ubicación")
    pasos = st.text_area("Paso a paso (uno por línea)", height=200)
    
    btn_evaluar = st.button("🚀 GENERAR EVALUACIÓN", type="primary")

with tab3:
    if btn_evaluar:
        if not actividad or not pasos:
            st.error("Completa actividad y pasos")
        elif not api_key:
            st.error("Introduce API Key")
        else:
            with st.spinner("Evaluando..."):
                pss_text = ""
                if pss_file:
                    reader = PyPDF2.PdfReader(pss_file)
                    pss_text = "\n".join([p.extract_text() for p in reader.pages])
                
                lista_pasos = [p.strip() for p in pasos.split("\n") if p.strip()]
                
                resultado = execute_prl_workflow(
                    activity_name=actividad,
                    activity_steps=lista_pasos,
                    location=ubicacion,
                    pss_document=pss_text,
                    pmp_rules=GOODMAN_PMP_RULES
                )
                
                st.success("✅ Evaluación completada")
                
                if resultado.get("final_report"):
                    st.markdown(resultado["final_report"]["executive_summary"])
                    
                    st.markdown("### Recomendaciones")
                    for rec in resultado["final_report"]["recommendations"]:
                        st.markdown(f"- {rec}")
                
                if resultado.get("risk_assessment"):
                    st.markdown("### Matriz de Riesgos")
                    
                    rows = []
                    for step in resultado["risk_assessment"].steps:
                        for h in step.hazards:
                            rows.append({
                                "Paso": f"{step.step_number}. {step.description[:30]}",
                                "Peligro": h.description,
                                "P": h.probability,
                                "S": h.severity,
                                "Nivel": h.risk_level,
                                "Clasificación": h.classification.value,
                                "Medidas": ", ".join(h.control_measures)
                            })
                    
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True)
                    
                    json_data = json.dumps(resultado, indent=2, default=str)
                    st.download_button(" Descargar JSON", json_data, "resultado.json")