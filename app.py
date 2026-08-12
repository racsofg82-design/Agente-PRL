"""Interfaz Streamlit"""
import streamlit as st
import pandas as pd
import PyPDF2
import json
from engine import execute_prl_workflow
from config import GOODMAN_PMP_RULES

st.set_page_config(page_title="Agente PRL Senior", page_icon="👷‍️", layout="wide")
st.title("‍♂️ Agente PRL Senior - Evaluación Técnica")

with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("OpenAI API Key", type="password", help="Necesaria para el análisis IA")
    if api_key:
        import os
        os.environ["OPENAI_API_KEY"] = api_key
    st.info(" Añade esta web a la pantalla de inicio de Safari en tu iPad para usarla como App.")

tab1, tab2, tab3 = st.tabs(["📄 1. Documentos", "️ 2. Actividad", " 3. Resultados"])

pss_text = ""
with tab1:
    pss_file = st.file_uploader("Subir PSS/RAMS (PDF)", type=["pdf"])
    if pss_file:
        try:
            reader = PyPDF2.PdfReader(pss_file)
            pss_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            st.success(f"✅ {pss_file.name} leído correctamente.")
        except Exception as e:
            st.error(f"Error leyendo PDF: {e}")

with tab2:
    actividad = st.text_input("Nombre de la actividad", placeholder="Ej: Sustitución de paneles de cubierta")
    ubicacion = st.text_input("Ubicación", placeholder="Ej: Nave 4, Madrid")
    pasos = st.text_area("Paso a paso (uno por línea)", height=250, placeholder="1. Montaje de andamio...\n2. Izado de materiales...")
    
    btn_evaluar = st.button("🚀 GENERAR ANÁLISIS PRL", type="primary", use_container_width=True)

with tab3:
    if btn_evaluar:
        if not api_key:
            st.error("⚠️ Introduce tu OpenAI API Key en la barra lateral.")
        elif not actividad or not pasos:
            st.error("⚠️ Completa el nombre de la actividad y los pasos.")
        else:
            with st.spinner("🤖 El Agente está analizando riesgos, normativa y PMP..."):
                lista_pasos = [p.strip() for p in pasos.split("\n") if p.strip()]
                
                try:
                    resultado = execute_prl_workflow(
                        name=actividad, steps=lista_pasos, location=ubicacion, 
                        pss_text=pss_text, pmp_rules=GOODMAN_PMP_RULES
                    )
                    
                    st.success("✅ Análisis completado con éxito.")
                    
                    if resultado.get("final_report"):
                        st.subheader(" Resumen Ejecutivo")
                        st.write(resultado["final_report"]["executive_summary"])
                        
                        st.subheader("💡 Recomendaciones Clave")
                        for rec in resultado["final_report"]["recommendations"]:
                            st.markdown(f"- {rec}")
                    
                    if resultado.get("risk_assessment"):
                        ra = resultado["risk_assessment"]
                        st.subheader(f"📊 Matriz de Riesgos ({ra.critical_hazards_count} Críticos)")
                        
                        rows = []
                        for step in ra.steps:
                            for h in step.hazards:
                                rows.append({
                                    "Paso": f"{step.step_number}. {step.description}",
                                    "Peligro": h.description,
                                    "Tipo": h.hazard_type.value,
                                    "P": h.probability, "S": h.severity, "Nivel": h.risk_level,
                                    "Clasificación": h.classification.value,
                                    "Justificación": h.justification,
                                    "Medidas de Control": " | ".join(h.control_measures)
                                })
                        
                        df = pd.DataFrame(rows)
                        st.dataframe(df, use_container_width=True, height=400)
                        
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Descargar Matriz (CSV/Excel)", csv, f"matriz_{actividad.replace(' ', '_')}.csv", "text/csv")
                        
                except Exception as e:
                    st.error(f"❌ Error en el sistema: {str(e)}")
