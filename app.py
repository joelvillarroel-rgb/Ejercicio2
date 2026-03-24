import streamlit as st

st.set_page_config(page_title="Comparación M/M/1", layout="wide")

st.title("Simulación de Sistemas - Ejercicio 2")
st.subheader("Comparación de alternativas (M/M/1)")

st.markdown("""
Esta aplicación permite comparar dos configuraciones de atención en un sistema de colas M/M/1.
""")

# ==============================
# INPUTS
# ==============================

st.sidebar.header("Parámetros del sistema")

lam = st.sidebar.number_input("Tasa de llegada λ (pacientes/hora)", value=20.0)

mu_A = st.sidebar.number_input("Tasa de servicio μ A", value=26.0)
mu_B = st.sidebar.number_input("Tasa de servicio μ B", value=32.0)

# ==============================
# FUNCIONES
# ==============================

def calcular_mm1(lam, mu):
    if lam >= mu:
        return None

    rho = lam / mu
    Lq = (lam**2) / (mu * (mu - lam))
    L = lam / (mu - lam)
    Wq = lam / (mu * (mu - lam))
    W = 1 / (mu - lam)

    return rho, Lq, L, Wq, W

# ==============================
# CÁLCULOS
# ==============================

res_A = calcular_mm1(lam, mu_A)
res_B = calcular_mm1(lam, mu_B)

# ==============================
# RESULTADOS
# ==============================

col1, col2 = st.columns(2)

# -------- Alternativa A --------
with col1:
    st.header("Alternativa A")

    if res_A:
        rho, Lq, L, Wq, W = res_A

        st.metric("Utilización (ρ)", f"{rho:.4f}")
        st.metric("Lq (cola)", f"{Lq:.4f}")
        st.metric("L (sistema)", f"{L:.4f}")
        st.metric("Wq (horas)", f"{Wq:.4f}")
        st.metric("W (horas)", f"{W:.4f}")

        st.markdown(f"⏱️ **Wq en minutos:** {Wq*60:.2f}")
        st.markdown(f"⏱️ **W en minutos:** {W*60:.2f}")

    else:
        st.error("Sistema inestable (λ ≥ μ)")

# -------- Alternativa B --------
with col2:
    st.header("Alternativa B")

    if res_B:
        rho, Lq, L, Wq, W = res_B

        st.metric("Utilización (ρ)", f"{rho:.4f}")
        st.metric("Lq (cola)", f"{Lq:.4f}")
        st.metric("L (sistema)", f"{L:.4f}")
        st.metric("Wq (horas)", f"{Wq:.4f}")
        st.metric("W (horas)", f"{W:.4f}")

        st.markdown(f"⏱️ **Wq en minutos:** {Wq*60:.2f}")
        st.markdown(f"⏱️ **W en minutos:** {W*60:.2f}")

    else:
        st.error("Sistema inestable (λ ≥ μ)")

# ==============================
# COMPARACIÓN
# ==============================

st.divider()
st.header("Comparación y análisis")

if res_A and res_B:
    _, _, _, Wq_A, _ = res_A
    _, _, _, Wq_B, _ = res_B

    mejora = ((Wq_A - Wq_B) / Wq_A) * 100

    st.success(f"✅ Mejora en tiempo de espera en cola: {mejora:.2f}%")

    if mejora > 0:
        st.markdown("""
        📊 **Conclusión:**

        La Alternativa B es superior porque reduce significativamente el tiempo de espera,
        disminuye la congestión y mejora la eficiencia del sistema.

        Desde una perspectiva gerencial, representa una mejor experiencia para el paciente
        y menor presión operativa.
        """)