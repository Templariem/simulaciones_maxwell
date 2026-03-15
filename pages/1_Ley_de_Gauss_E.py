import streamlit as st

st.set_page_config(page_title="Ley de Gauss (E)", page_icon="⚡", layout="wide")

st.markdown("# ⚡ Ley de Gauss: $\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\varepsilon_0}$")

st.markdown("""
#### 📜 Contexto histórico
Formulada por **Carl Friedrich Gauss** en 1835, esta ley unifica los trabajos previos
de Coulomb sobre fuerzas eléctricas. Establece que el flujo eléctrico neto a través de cualquier
superficie cerrada es proporcional a la carga total encerrada.

#### 🖥️ Simulación
Las líneas de campo **salen** de cargas positivas y **entran** en cargas negativas.
Añade cargas y observa cómo el campo eléctrico se superpone y adapta dinámicamente.
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
Formulated by **Carl Friedrich Gauss** in 1835, this law unifies Coulomb's earlier work
on electric forces. It states that the net electric flux through any closed surface
is proportional to the total enclosed charge.

#### 🖥️ Simulation
Field lines **emerge** from positive charges and **enter** negative charges.
Add charges and observe how the electric field superimposes and adapts dynamically.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)
if 'num_pos' not in st.session_state:
    st.session_state.num_pos = 1
if 'num_neg' not in st.session_state:
    st.session_state.num_neg = 0

with col1:
    if st.button("➕ Añadir Carga (+)", use_container_width=True):
        if st.session_state.num_pos + st.session_state.num_neg < 15:
            st.session_state.num_pos += 1
            st.rerun()
with col2:
    if st.button("➖ Añadir Carga (−)", use_container_width=True):
        if st.session_state.num_pos + st.session_state.num_neg < 15:
            st.session_state.num_neg += 1
            st.rerun()
with col3:
    if st.button("🗑️ Limpiar Todo", use_container_width=True):
        st.session_state.num_pos = 0
        st.session_state.num_neg = 0
        st.rerun()

n_p = st.session_state.num_pos
n_n = st.session_state.num_neg
st.caption(f"🟡 Positivas: {n_p}  ·  🔵 Negativas: {n_n}  ·  Total: {n_p + n_n}")

html_code = f"""
<canvas id="canvasE" style="display:block; margin:0 auto; border-radius:12px;"></canvas>
<script>
const canvas = document.getElementById('canvasE');
const ctx = canvas.getContext('2d');
const N_POS = {n_p};
const N_NEG = {n_n};
const TOTAL = N_POS + N_NEG;

function resize() {{
    const w = Math.min(window.innerWidth - 40, 800);
    canvas.width = w; canvas.height = w;
}}
resize();
window.addEventListener('resize', resize);

const W = () => canvas.width, H = () => canvas.height;
const sc = () => W() / 12.0;
function toS(wx, wy) {{ return [W()/2 + wx*sc(), H()/2 - wy*sc()]; }}

// Particles for field lines
const NUM_PARTICLES = 6000; // Updated name and value
let particles = [];
for (let i=0; i<NUM_PARTICLES; i++) {{ // Use NUM_PARTICLES
    let l = Math.random()*100;
    particles.push({{
        x: (Math.random()-0.5)*14, // Updated range
        y: (Math.random()-0.5)*14, // Updated range
        life: l,    // Updated range
        max_life: l
    }});
}}

// Charges setup
let charges = [];
// Distribute uniformly in a circle, with slightly different radii
for (let i=0; i<TOTAL; i++) {{
    let isPos = i < N_POS;
    let angle = (i / TOTAL) * Math.PI * 2;
    let r = 2.0 + (i % 2) * 1.0;
    // Each charge gets its own oscillation parameters
    charges.push({{
        q: isPos ? 1 : -1,
        base_angle: angle,
        base_r: r,
        p1: 0.5 + Math.random()*0.5,
        p2: 0.5 + Math.random()*0.5,
        x: 0, y: 0
    }});
}}

function EField(px, py) {{
    let Ex = 0, Ey = 0;
    for (let c of charges) {{
        let dx = px - c.x, dy = py - c.y;
        let r3 = Math.pow(dx*dx + dy*dy + 0.05, 1.5);
        // If exact opposite charges exist, they might cancel exactly, add 0.05 smoothing
        Ex += c.q * dx / r3;
        Ey += c.q * dy / r3;
    }}
    return [Ex, Ey];
}}

let t = 0;
function draw() {{
    t += 0.012;
    const w = W(), h = H(), s = sc();
    
    // Animate charges (slow drifting around their base position)
    for (let i=0; i<TOTAL; i++) {{
        let c = charges[i];
        let ang = c.base_angle + t * c.p1 * 0.8;
        let r_drift = c.base_r + Math.sin(t * c.p2 * 1.2) * 1.5;
        c.x = Math.cos(ang) * r_drift;
        c.y = Math.sin(ang) * r_drift;
    }}
    
    ctx.fillStyle = '#0E1117'; ctx.fillRect(0,0,w,h);
    ctx.fillStyle = '#fff'; ctx.font = 'bold '+Math.round(s*0.4)+'px Arial';
    ctx.textAlign='center'; ctx.fillText('Ley de Gauss (E): ∇·E = ρ/ε₀', w/2, s*0.6);
    
    if (TOTAL > 0) {{
        // Update & draw field lines
        for (let p of particles) {{
            let [ex, ey] = EField(p.x, p.y);
            let mag = Math.sqrt(ex*ex + ey*ey) + 1e-4;
            // Particles always flow in direction of E (so + to -)
            p.x += (ex/mag) * 0.06;
            p.y += (ey/mag) * 0.06;
            p.life--;
            
            if (p.life <= 0 || Math.abs(p.x)>7 || Math.abs(p.y)>7) {{
                // If only positive charges, spawn everywhere
                // If mixed or negative, field lines go into -, spawn everywhere too
                p.x = (Math.random()-0.5)*14;
                p.y = (Math.random()-0.5)*14;
                let l = 20 + Math.random()*60;
                p.life = l;
                p.max_life = l;
            }}
            
            let [px, py] = toS(p.x, p.y);
            
            let intensity = Math.min(1, mag * 0.5);
            
            // 2-Color Gradient: White (weak) -> Red (strong)
            let r=255, g=255, b=255;
            // White to Red transition
            g = 255 - Math.round(intensity * 255);
            b = 255 - Math.round(intensity * 255);
            
            // Fade in and out smoothly based on life fraction to prevent "popping"
            let life_fade = Math.sin((p.life / p.max_life) * Math.PI);
            let alpha = Math.max(0.2, intensity * 0.8) * life_fade; 
            
            ctx.fillStyle = 'rgba('+r+','+g+','+b+','+alpha+')';
            ctx.beginPath(); 
            // Thick spherical particle
            ctx.arc(px, py, Math.max(2.5, s*0.035), 0, Math.PI*2); 
            ctx.fill();
        }}
    }}
    
    // Draw charges
    for (let c of charges) {{
        let [cx, cy] = toS(c.x, c.y);
        ctx.fillStyle = c.q > 0 ? '#3296FF' : '#FF3232'; // Blue (+), Red (-)
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(cx, cy, s*0.4, 0, Math.PI*2); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#fff'; ctx.font = 'bold '+Math.round(s*0.4)+'px Arial';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(c.q > 0 ? '+' : '−', cx, cy);
    }}
    
    requestAnimationFrame(draw);
}}

draw();
</script>
"""

st.components.v1.html(html_code, height=840)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; margin-top: 2rem; padding: 1.5rem; border-top: 1px solid #333;">
    <p><strong>Creado por:</strong> Ph.D Student Giovanni Cocca-Guardia</p>
    <p><strong>Asistido por:</strong> Gemini Pro 3.1 & Claude Opus 4.6</p>
    <p>🔗 <strong>GitHub:</strong> <a href="#" style="color: #FFD700;">[Repositorio próximamente]</a></p>
    <p>🏛️ <strong>Escuela de Ingeniería Eléctrica</strong></p>
    <p>🏰 <strong>Pontificia Universidad Católica de Valparaíso</strong></p>
    <p><strong>🇨🇱 Chile 🍷🗿</strong></p>
</div>
""", unsafe_allow_html=True)
