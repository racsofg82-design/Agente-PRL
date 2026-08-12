"""Interfaz Streamlit - Con Referencias Normativas"""
import streamlit as st
import pandas as pd
import PyPDF2
from engine import execute_prl_workflow
from config import GOODMAN_PMP_RULES

st.set_page_config(page_title="Agente PRL Senior", page_icon="👷‍♂️", layout="wide")

st.title("👷‍♂️ Agente PRL Senior - Con Biblioteca INSST")
st.caption("Análisis técnico con NTPs y normativa específica integrada")

with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        import os
        os.environ["OPENAI_API_KEY"] = api_key
    st.divider()
    st.info("💡 **Tip iPad:** En Safari, pulsa Compartir > Añadir a pantalla de inicio.")

def extract_text_from_pdf(file) -> str:
    try:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    except Exception as e:
        st.error(f"Error leyendo {file.name}: {e}")
        return ""

tab1, tab2 = st.tabs(["📂 1. Carga de Documentos", "📊 2. Análisis y Matriz"])

with tab1:
    st.subheader("Documentos de Entrada")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📄 Principal (A analizar)**")
        proc_file = st.file_uploader("Procedimiento / Borrador RAMS", type=["pdf", "txt"])
        proc_text = ""
        if proc_file:
            if proc_file.type == "application/pdf":
                proc_text = extract_text_from_pdf(proc_file)
            else:
                proc_text = proc_file.read().decode("utf-8")
            st.success(f"✅ {proc_file.name} cargado ({len(proc_text)} chars)")
            
    with col2:
        st.markdown("**📋 Referencia 1**")
        pss_file = st.file_uploader("PSS del Cliente (Opcional)", type=["pdf", "txt"])
        pss_text = ""
        if pss_file:
            pss_text = extract_text_from_pdf(pss_file) if pss_file.type == "application/pdf" else pss_file.read().decode("utf-8")
            st.success(f"✅ PSS cargado")
            
    with col3:
        st.markdown("**📑 Referencia 2**")
        pmp_file = st.file_uploader("PMP del Cliente (Opcional)", type=["pdf", "txt"])
        pmp_text = ""
        if pmp_file:
            pmp_text = extract_text_from_pdf(pmp_file) if pmp_file.type == "application/pdf" else pmp_file.read().decode("utf-8")
            st.success(f"✅ PMP cargado")

    st.divider()
    
    with st.expander("✏️ Editar/Pegar texto del procedimiento manualmente"):
        manual_proc = st.text_area("Pega aquí el texto del procedimiento o pasos:", height=200)
        if manual_proc:
            proc_text = manual_proc

    btn_analyze = st.button("🚀 ANALIZAR CON NORMATIVA INSST", type="primary", use_container_width=True)

with tab2:
    if btn_analyze:
        if not api_key:
            st.error("⚠️ Introduce tu API Key en la barra lateral.")
        elif not proc_text:
            st.error("⚠️ Debes subir el Procedimiento/Borrador RAMS o pegar su texto.")
        else:
            with st.spinner("🤖 El Agente está analizando con la biblioteca completa del INSST..."):
                resultado = execute_prl_workflow(proc_text, pss_text, pmp_text)
                
                st.success("✅ Análisis completado con referencias normativas.")
                
                ra = resultado["risk_assessment"]
                
                st.subheader("📋 Resumen Ejecutivo")
                st.write(resultado["final_report"]["executive_summary"])
                
                st.subheader(" Recomendaciones y Hallazgos")
                for rec in ra.recommendations:
                    st.markdown(f"- {rec}")
                
                st.subheader(f"📊 Matriz de Riesgos 5x5 ({ra.critical_hazards_count} Críticos)")
                
                rows = []
                for step in ra.steps:
                    for h in step.hazards:
                        rows.append({
                            "Paso": f"{step.step_number}. {step.description[:40]}...",
                            "Peligro": h.description,
                            "Tipo": h.hazard_type.value,
                            "P": h.probability, "S": h.severity, "Nivel": h.risk_level,
                            "Clasif.": h.classification.value,
                            "Justificación": h.justification,
                            "Medidas Propuestas": " | ".join(h.control_measures),
                            "Referencia Normativa": ", ".join(h.normative_references) if h.normative_references else "N/A"
                        })
                
                if rows:
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, height=500)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Descargar Matriz (CSV/Excel)", csv, f"matriz_{ra.activity_name.replace(' ', '_')}.csv", "text/csv")
                else:
                    st.warning("No se generaron filas en la matriz.")
