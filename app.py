import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparación M/M/1", layout="wide")

st.title("📊 Simulación de Sistemas - Ejercicio 2")
st.subheader("Comparación de alternativas (M/M/1)")

st.markdown("""
Esta aplicación compara dos configuraciones de atención utilizando teoría de colas M/M/1.
Incluye indicadores clave y gráficos para análisis gerencial.
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
# RESULTADOS NUMÉRICOS
# ==============================

col1, col2 = st.columns(2)

with col1:
    st.header("🔵 Alternativa A")
    if res_A:
        rho_A, Lq_A, L_A, Wq_A, W_A = res_A
        st.metric("Utilización", f"{rho_A:.4f}")
        st.metric("Lq", f"{Lq_A:.4f}")
        st.metric("L", f"{L_A:.4f}")
        st.metric("Wq (min)", f"{Wq_A*60:.2f}")
        st.metric("W (min)", f"{W_A*60:.2f}")
    else:
        st.error("Sistema inestable")

with col2:
    st.header("🟢 Alternativa B")
    if res_B:
        rho_B, Lq_B, L_B, Wq_B, W_B = res_B
        st.metric("Utilización", f"{rho_B:.4f}")
        st.metric("Lq", f"{Lq_B:.4f}")
        st.metric("L", f"{L_B:.4f}")
        st.metric("Wq (min)", f"{Wq_B*60:.2f}")
        st.metric("W (min)", f"{W_B*60:.2f}")
    else:
        st.error("Sistema inestable")

# ==============================
# GRÁFICO 1: COMPARACIÓN DIRECTA
# ==============================

st.divider()
st.header("📊 Comparación de Indicadores")

if res_A and res_B:
    indicadores = ["Utilización", "Lq", "L", "Wq(min)", "W(min)"]

    valores_A = [
        rho_A,
        Lq_A,
        L_A,
        Wq_A * 60,
        W_A * 60
    ]

    valores_B = [
        rho_B,
        Lq_B,
        L_B,
        Wq_B * 60,
        W_B * 60
    ]

    fig, ax = plt.subplots()

    x = range(len(indicadores))
    width = 0.35

    ax.bar(x, valores_A, width, label="Alternativa A")
    ax.bar([i + width for i in x], valores_B, width, label="Alternativa B")

    ax.set_xticks([i + width/2 for i in x])
    ax.set_xticklabels(indicadores)
    ax.set_title("Comparación de desempeño")
    ax.legend()

    st.pyplot(fig)

# ==============================
# GRÁFICO 2: SENSIBILIDAD (μ vs Wq)
# ==============================

st.header("📉 Sensibilidad: Tiempo de espera vs tasa de servicio")

if lam > 0:
    mu_values = []
    Wq_values = []

    mu_test = lam + 1
    while mu_test <= lam + 50:
        Wq_test = lam / (mu_test * (mu_test - lam))
        mu_values.append(mu_test)
        Wq_values.append(Wq_test * 60)  # minutos
        mu_test += 1

    fig2, ax2 = plt.subplots()

    ax2.plot(mu_values, Wq_values)
    ax2.set_xlabel("μ (tasa de servicio)")
    ax2.set_ylabel("Wq (minutos)")
    ax2.set_title("Sensibilidad del tiempo de espera")

    st.pyplot(fig2)

# ==============================
# MEJORA PORCENTUAL
# ==============================

st.divider()
st.header("📈 Mejora del sistema")

if res_A and res_B:
    mejora = ((Wq_A - Wq_B) / Wq_A) * 100
    st.success(f"Mejora en Wq: {mejora:.2f}%")

# ==============================
# CONCLUSIÓN AUTOMÁTICA
# ==============================

st.header("🧠 Conclusión Gerencial")

if res_A and res_B:
    if Wq_B < Wq_A:
        st.markdown("""
        ✅ **Se recomienda la Alternativa B**

        - Reduce significativamente los tiempos de espera
        - Disminuye la congestión
        - Mejora la eficiencia operativa
        - Proporciona mejor experiencia al paciente
        """)
    else:
        st.warning("No hay mejora significativa")