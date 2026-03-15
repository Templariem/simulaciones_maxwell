import streamlit as st

st.set_page_config(
    page_title="Ecuaciones de Maxwell — Simulaciones Interactivas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS personalizado ---
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700, #FF6B35, #FF1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .eq-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .eq-card h3 {
        color: #FFD700;
        margin-bottom: 0.5rem;
    }
    .eq-card p {
        color: #ccc;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        color: #888;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #333;
    }
    .footer a {
        color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown('<div class="main-title">⚡ Ecuaciones de Maxwell</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Simulaciones Interactivas de Electromagnetismo</div>', unsafe_allow_html=True)

st.markdown("---")

# --- Las 4 ecuaciones ---
st.markdown("### 📐 Las Cuatro Ecuaciones Fundamentales")
st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="eq-card">
        <h3>I. Ley de Gauss (Eléctrica)</h3>
        <p style="font-size: 1.4rem; color: white;">∇ · E = ρ / ε₀</p>
        <p>Formulada por Gauss (1835). Las cargas eléctricas son fuentes y sumideros del campo eléctrico.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="eq-card">
        <h3>III. Ley de Ampère-Maxwell</h3>
        <p style="font-size: 1.4rem; color: white;">∇ × B = μ₀J + μ₀ε₀ ∂E/∂t</p>
        <p>Ampère (1820) + Maxwell (1865). Las corrientes y campos eléctricos variables generan campo magnético.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="eq-card">
        <h3>II. Ley de Gauss (Magnética)</h3>
        <p style="font-size: 1.4rem; color: white;">∇ · B = 0</p>
        <p>No existen monopolos magnéticos. Las líneas de B siempre se cierran formando bucles.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="eq-card">
        <h3>IV. Ley de Faraday</h3>
        <p style="font-size: 1.4rem; color: white;">∇ × E = −∂B/∂t</p>
        <p>Faraday (1831). Un campo magnético variable induce un campo eléctrico rotacional y una FEM.</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🇬🇧 English"):
    st.markdown("""
| Equation | Formula | Description |
|----------|---------|-------------|
| **I. Gauss's Law (Electric)** | ∇ · E = ρ / ε₀ | Gauss (1835). Electric charges are sources and sinks of the electric field. |
| **II. Gauss's Law (Magnetic)** | ∇ · B = 0 | No magnetic monopoles exist. B-field lines always form closed loops. |
| **III. Ampère-Maxwell Law** | ∇ × B = μ₀J + μ₀ε₀ ∂E/∂t | Ampère (1820) + Maxwell (1865). Currents and time-varying E fields generate B fields. |
| **IV. Faraday's Law** | ∇ × E = −∂B/∂t | Faraday (1831). A time-varying magnetic field induces a rotational electric field and an EMF. |
""")

st.markdown("---")

# --- Contenido de la app ---
st.markdown("### 🧭 Navegación")
st.markdown("""
Utiliza el menú lateral (**←**) para explorar las simulaciones:

| # | Página | Descripción |
|---|--------|-------------|
| 1 | **Ley de Gauss (E)** | Gauss (1835) — Campo eléctrico de cargas puntuales con superposición |
| 2 | **Ley de Gauss (B)** | Gauss — Líneas de campo magnético dipolar, sin monopolos |
| 3 | **Ley de Ampère-Maxwell** | Ampère (1820) + Maxwell (1865) — Corrientes y corriente de desplazamiento |
| 4 | **Ley de Faraday** | Faraday (1831) — Inducción electromagnética con imán y bobina |
| 5 | **Propagación Ondas EM** | Maxwell (1865) / Hertz (1887) — Propagación longitudinal, plana y radial |
| 6 | **Circuito Poynting** | Poynting (1884) — Flujo de energía EM en un circuito eléctrico |
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
**Maxwell's Equations** are the four fundamental laws that describe all electromagnetic phenomena.
Formulated by James Clerk Maxwell in 1865, they unified electricity, magnetism, and optics into
a single coherent theory, predicting the existence of electromagnetic waves.

| # | Page | Description |
|---|------|-------------|
| 1 | **Gauss's Law (E)** | Gauss (1835) — Electric field from point charges with superposition |
| 2 | **Gauss's Law (B)** | Gauss — Dipole magnetic field lines, no monopoles |
| 3 | **Ampère-Maxwell Law** | Ampère (1820) + Maxwell (1865) — Conduction & displacement current |
| 4 | **Faraday's Law** | Faraday (1831) — Electromagnetic induction with magnet and coil |
| 5 | **EM Wave Propagation** | Maxwell (1865) / Hertz (1887) — Longitudinal, plane & radial propagation |
| 6 | **Poynting Circuit** | Poynting (1884) — EM energy flow in an electrical circuit |
""")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>Creado por:</strong> Ph.D Student Giovanni Cocca-Guardia</p>
    <p><strong>Asistido por:</strong> Gemini Pro 3.1 & Claude Opus 4.6</p>
    <p>🔗 <strong>GitHub:</strong> <a href="#" style="color: #FFD700;">[Repositorio próximamente]</a></p>
    <p>🏛️ <strong>Escuela de Ingeniería Eléctrica</strong></p>
    <p>🏰 <strong>Pontificia Universidad Católica de Valparaíso</strong></p>
    <p><strong>🇨🇱 Chile 🍷🗿</strong></p>
</div>
""", unsafe_allow_html=True)
