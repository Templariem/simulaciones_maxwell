import streamlit as st

st.set_page_config(page_title="Ley de Faraday", page_icon="🔄", layout="wide")

st.markdown("# 🔄 Ley de Faraday: $\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$")

st.markdown("""
#### 📜 Contexto histórico
**Michael Faraday** demostró en 1831 que un campo magnético variable en el
tiempo induce una fuerza electromotriz (FEM). Este descubrimiento revolucionó la tecnología,
dando origen a generadores eléctricos, transformadores y motores.

#### 🖥️ Simulación
Un imán oscila a través de una bobina de cobre. La ampolleta brilla más
cuando el imán se mueve rápido. Más espiras = más voltaje inducido (**V = N × |dΦ/dt|**).
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
**Michael Faraday** demonstrated in 1831 that a time-varying magnetic field
induces an electromotive force (EMF). This discovery revolutionized technology,
giving rise to electric generators, transformers, and motors.

#### 🖥️ Simulation
A magnet oscillates through a copper coil. The bulb glows brighter
when the magnet moves faster. More turns = more induced voltage (**V = N × |dΦ/dt|**).
""")

st.markdown("---")

col1, col2 = st.columns(2)
if 'n_espiras' not in st.session_state:
    st.session_state.n_espiras = 5

with col1:
    if st.button("➕ Más Espiras", use_container_width=True):
        if st.session_state.n_espiras < 15:
            st.session_state.n_espiras += 1
            st.rerun()
with col2:
    if st.button("➖ Menos Espiras", use_container_width=True):
        if st.session_state.n_espiras > 1:
            st.session_state.n_espiras -= 1
            st.rerun()

N = st.session_state.n_espiras
st.caption(f"🔧 Espiras: {N}")

html_code = f"""
<canvas id="faradayCanvas" style="display:block; margin:0 auto; border-radius:12px;"></canvas>
<script>
const canvas = document.getElementById('faradayCanvas');
const ctx = canvas.getContext('2d');
const N_ESPIRAS = {N};

function resize() {{
    const w = Math.min(window.innerWidth - 40, 800);
    canvas.width = w; canvas.height = w;
}}
resize();
window.addEventListener('resize', resize);

const W = () => canvas.width;
const H = () => canvas.height;
const scale = () => W() / 14.0;

function toScreen(wx, wy) {{
    return [W()/2 + wx * scale(), H()/2 - wy * scale()];
}}

// Particles — 4000 for dense field visualization
const NUM_PARTICLES = 6000;
let particles = [];

function initParticles() {{
    particles = [];
    for (let i = 0; i < NUM_PARTICLES; i++) {{
        let l = Math.random() * 60;
        particles.push({{
            x: (Math.random() - 0.5) * 13,
            y: (Math.random() - 0.5) * 13,
            life: l, max_life: l  // short lifetime for uniform density
        }});
    }}
}}
initParticles();

function fieldAt(px, py, mx, my) {{
    const s = 2.5;
    const hw = 0.5;
    let dxn = px - (mx + hw), dyn = py - my;
    let r3n = Math.pow(dxn*dxn + dyn*dyn + 0.05, 1.5);
    let Bx = s * dxn / r3n, By = s * dyn / r3n;
    let dxs = px - (mx - hw), dys = py - my;
    let r3s = Math.pow(dxs*dxs + dys*dys + 0.05, 1.5);
    Bx -= s * dxs / r3s;
    By -= s * dys / r3s;
    return [Bx, By];
}}

let prevMx = 0;
let t = 0;

function draw() {{
    t += 0.016;
    const w = W(), h = H(), sc = scale();
    
    const mx = 4.0 * Math.sin(t * 1.2);
    const my = 0;
    
    const speed = Math.abs(mx - prevMx);
    const brightness = Math.min(1.0, N_ESPIRAS * speed * 2.5);
    prevMx = mx;
    
    ctx.fillStyle = '#0E1117';
    ctx.fillRect(0, 0, w, h);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold ' + Math.round(sc * 0.4) + 'px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Ley de Faraday: ∇ × E = −∂B/∂t', w/2, sc * 0.6);
    
    // Update and draw particles — ALL follow B direction (physically correct)
    for (let p of particles) {{
        let [bx, by] = fieldAt(p.x, p.y, mx, my);
        let mag = Math.sqrt(bx*bx + by*by) + 0.001;
        let step = 0.05;
        p.x += (bx / mag) * step;
        p.y += (by / mag) * step;
        p.life--;
        
        // Respawn UNIFORMLY across entire space (not at poles)
        // Short lifetime ensures even density everywhere
        if (p.life <= 0 || Math.abs(p.x) > 7 || Math.abs(p.y) > 7) {{
            p.x = (Math.random() - 0.5) * 13;
            p.y = (Math.random() - 0.5) * 13;
            let l = 30 + Math.random() * 50;
            p.life = l;
            p.max_life = l;
        }}
        
        let [sx, sy] = toScreen(p.x, p.y);
        let intensity = Math.min(1, mag * 0.3);
        
        // 2-Color Gradient: White (weak) -> Green (strong)
        let pr=255, pg=255, pb=255;
        pr = 255 - Math.round(intensity * 255);
        pb = 255 - Math.round(intensity * 255);
        
        let life_fade = Math.sin((p.life / p.max_life) * Math.PI);
        let alpha = Math.max(0.2, intensity * 0.8) * life_fade; 
        
        ctx.fillStyle = 'rgba(' + pr + ',' + pg + ',' + pb + ',' + alpha + ')';
        ctx.beginPath();
        ctx.arc(sx, sy, Math.max(1.5, sc * 0.035), 0, Math.PI * 2);
        ctx.fill();
    }}
    
    // Magnet (drawn BEFORE the coil so it passes BEHIND)
    const mw = 2.0, mh = 1.0;
    let [ms1x, ms1y] = toScreen(mx - mw/2, my + mh/2);
    let sWidth = sc * mw/2, sHeight = sc * mh;
    ctx.fillStyle = '#00FFFF';
    ctx.fillRect(ms1x, ms1y, sWidth, sHeight);
    let [mn1x, mn1y] = toScreen(mx, my + mh/2);
    ctx.fillStyle = '#FF4500';
    ctx.fillRect(mn1x, mn1y, sWidth, sHeight);
    let [mb1x, mb1y] = toScreen(mx - mw/2, my + mh/2);
    ctx.strokeStyle = 'white'; ctx.lineWidth = 2;
    ctx.strokeRect(mb1x, mb1y, sc * mw, sHeight);
    ctx.fillStyle = 'black';
    ctx.font = 'bold ' + Math.round(sc * 0.4) + 'px Arial';
    ctx.textAlign = 'center';
    let [slx, sly] = toScreen(mx - mw/4, my);
    ctx.fillText('S', slx, sly + sc * 0.15);
    ctx.fillStyle = 'white';
    let [nlx, nly] = toScreen(mx + mw/4, my);
    ctx.fillText('N', nlx, nly + sc * 0.15);

    // Coil
    const coilWidth = 2.0;
    for (let i = 0; i < N_ESPIRAS; i++) {{
        let xo = (i - N_ESPIRAS/2 + 0.5) * (coilWidth / Math.max(1, N_ESPIRAS));
        let [sx1, sy1] = toScreen(xo, -3.5);
        let [sx2, sy2] = toScreen(xo, 3.5);
        // Darker copper colour
        ctx.strokeStyle = '#6B3E11';
        ctx.lineWidth = Math.max(2, sc * 0.06);
        ctx.beginPath(); ctx.moveTo(sx1, sy1); ctx.lineTo(sx2, sy2); ctx.stroke();
    }}
    
    // Wire to bulb
    let [wx1, wy1] = toScreen(0, 3.5);
    let [wx2, wy2] = toScreen(0, 5.0);
    ctx.strokeStyle = '#888888';
    ctx.lineWidth = Math.max(1, sc * 0.04);
    ctx.beginPath(); ctx.moveTo(wx1, wy1); ctx.lineTo(wx2, wy2); ctx.stroke();
    
    // Bulb halo
    let [bsx, bsy] = toScreen(0, 5.5);
    if (brightness > 0.02) {{
        let grad = ctx.createRadialGradient(bsx, bsy, 0, bsx, bsy, sc * 1.5);
        // Whiter yellow for better contrast
        grad.addColorStop(0, 'rgba(255,255,180,' + (brightness * 0.6) + ')');
        grad.addColorStop(1, 'rgba(255,255,180,0)');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(bsx, bsy, sc * 1.5, 0, Math.PI * 2); ctx.fill();
    }}
    
    ctx.fillStyle = brightness > 0.05 ? 
        'rgba(255,255,180,' + Math.max(0.3, brightness) + ')' : '#444444';
    ctx.strokeStyle = 'white'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(bsx, bsy, sc * 0.6, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    

    ctx.fillStyle = '#888888';
    ctx.font = Math.round(sc * 0.25) + 'px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Espiras: ' + N_ESPIRAS + '  |  Brillo: ' + brightness.toFixed(2), w/2, h - sc * 0.3);
    
    requestAnimationFrame(draw);
}}

draw();
</script>
"""

st.components.v1.html(html_code, height=820)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; margin-top: 2rem; padding: 1.5rem; border-top: 1px solid #333;">
    <p><strong>Creado por:</strong> Ph.D Student Giovanni Cocca-Guardia</p>
    <p><strong>Asistido por:</strong> Gemini Pro 3.1 & Claude Opus 4.6</p>
    <p>🔗 <strong>GitHub:</strong> <a href="https://github.com/Templariem/simulaciones_maxwell" style="color: #FFD700;" target="_blank">Repositorio oficial</a></p>
    <p>🏛️ <strong>Escuela de Ingeniería Eléctrica</strong></p>
    <p>🏰 <strong>Pontificia Universidad Católica de Valparaíso</strong></p>
    <p><strong>🇨🇱 Chile 🍷🗿</strong></p>
</div>
""", unsafe_allow_html=True)
