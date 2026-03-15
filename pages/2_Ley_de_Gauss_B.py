import streamlit as st

st.set_page_config(page_title="Ley de Gauss (B)", page_icon="🧲", layout="wide")

st.markdown("# 🧲 Ley de Gauss (B): $\\nabla \\cdot \\mathbf{B} = 0$")

st.markdown("""
#### 📜 Contexto histórico
Esta ley, parte del legado de **Gauss**, establece que no existen monopolos
magnéticos en la naturaleza. A diferencia de las cargas eléctricas (que pueden ser aisladas),
los polos magnéticos siempre vienen en pares Norte-Sur.

#### 🖥️ Simulación
Toda línea de campo magnético que sale de un polo N regresa al polo S,
formando bucles cerrados. Añade imanes y observa cómo interactúan sus campos.
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
This law, part of **Gauss's** legacy, states that magnetic monopoles do not exist
in nature. Unlike electric charges (which can be isolated), magnetic poles always
come in North-South pairs.

#### 🖥️ Simulation
Every magnetic field line leaving a N pole returns to a S pole,
forming closed loops. Add magnets and observe how their fields interact.
""")

st.markdown("---")

col1, col2 = st.columns(2)
if 'num_imanes' not in st.session_state:
    st.session_state.num_imanes = 1

with col1:
    if st.button("🧲 Añadir Imán", use_container_width=True):
        if st.session_state.num_imanes < 10:
            st.session_state.num_imanes += 1
            st.rerun()
with col2:
    if st.button("🗑️ Limpiar Todo", use_container_width=True):
        st.session_state.num_imanes = 1
        st.rerun()

n_m = st.session_state.num_imanes
st.caption(f"🧲 Imanes: {n_m}")

html_code = f"""
<canvas id="canvasB" style="display:block; margin:0 auto; border-radius:12px;"></canvas>
<script>
const canvas = document.getElementById('canvasB');
const ctx = canvas.getContext('2d');
const NUM_IMANES = {n_m};

function resize() {{
    const w = Math.min(window.innerWidth - 40, 800);
    canvas.width = w; canvas.height = w;
}}
resize();
window.addEventListener('resize', resize);

const W = () => canvas.width, H = () => canvas.height;
const sc = () => W() / 14.0;
function toS(wx, wy) {{ return [W()/2 + wx*sc(), H()/2 - wy*sc()]; }}

// Particles for field lines
const NUM_PARTICLES = 6000;
let particles = [];
for(let i=0; i<NUM_PARTICLES; i++) {{
    let l = Math.random()*100;
    particles.push({{
        x: (Math.random()-0.5)*15,
        y: (Math.random()-0.5)*15,
        life: l,
        max_life: l
    }});
}}

// Magnets setup
let magnets = [];
for (let i=0; i<NUM_IMANES; i++) {{
    let angle = (i / Math.max(1, NUM_IMANES)) * Math.PI * 2;
    let r = 3.0;
    magnets.push({{
        base_angle: angle,
        base_r: r,
        p1: 0.4 + Math.random()*0.4,
        p2: 0.4 + Math.random()*0.4,
        rot_speed: (Math.random()-0.5)*0.5,
        x: 0, y: 0, theta: angle
    }});
}}

function BField(px, py) {{
    let Bx = 0, By = 0;
    const hw = 0.5; // half width of magnet
    const stroke = 1.5;
    for (let m of magnets) {{
        // Magnet poles relative to its center and rotation
        let nx = m.x + hw * Math.cos(m.theta);
        let ny = m.y + hw * Math.sin(m.theta);
        let sx = m.x - hw * Math.cos(m.theta);
        let sy = m.y - hw * Math.sin(m.theta);
        
        let dxn = px - nx, dyn = py - ny;
        let r3n = Math.pow(dxn*dxn + dyn*dyn + 0.05, 1.5);
        Bx += stroke * dxn / r3n;
        By += stroke * dyn / r3n;
        
        let dxs = px - sx, dys = py - sy;
        let r3s = Math.pow(dxs*dxs + dys*dys + 0.05, 1.5);
        Bx -= stroke * dxs / r3s;
        By -= stroke * dys / r3s;
    }}
    return [Bx, By];
}}

let t = 0;
function draw() {{
    t += 0.016;
    const w = W(), h = H(), s = sc();
    
    // Animate magnets
    for (let i=0; i<NUM_IMANES; i++) {{
        let m = magnets[i];
        let ang = m.base_angle + t * m.p1;
        let r_drift = m.base_r + Math.sin(t * m.p2) * 1.5;
        m.x = Math.cos(ang) * r_drift;
        m.y = Math.sin(ang) * r_drift;
        m.theta += m.rot_speed * 0.02; // slow rotation
    }}
    
    ctx.fillStyle = '#0E1117'; ctx.fillRect(0,0,w,h);
    ctx.fillStyle = '#fff'; ctx.font = 'bold '+Math.round(s*0.4)+'px Arial';
    ctx.textAlign='center'; ctx.fillText('Ley de Gauss (B): ∇·B = 0', w/2, s*0.6);
    
    if (NUM_IMANES > 0) {{
        for (let p of particles) {{
            let [bx, by] = BField(p.x, p.y);
            let mag = Math.sqrt(bx*bx + by*by) + 1e-4;
            // Particles flow along B
            p.x += (bx/mag) * 0.06;
            p.y += (by/mag) * 0.06;
            p.life--;
            
            if (p.life <= 0 || Math.abs(p.x)>8 || Math.abs(p.y)>8) {{
                p.x = (Math.random()-0.5)*15;
                p.y = (Math.random()-0.5)*15;
                let l = 20 + Math.random()*60;
                p.life = l;
                p.max_life = l;
            }}
            
            let [px, py] = toS(p.x, p.y);
            
            // Dipole fields drop as 1/r³, meaning the field far away is incredibly weak.
            // We artificially boost the visual intensity so particles light up the whole screen.
            let visual_mag = Math.pow(mag, 0.35) * 1.5;
            let intensity = Math.min(1, visual_mag * 0.4);
            
            // 2-Color Gradient: White (weak) -> Green (strong)
            let r=255, g=255, b=255;
            // White to Green transition
            r = 255 - Math.round(intensity * 255);
            b = 255 - Math.round(intensity * 255);
            
            // Fade in and out smoothly based on life fraction to prevent "popping"
            let life_fade = Math.sin((p.life / p.max_life) * Math.PI);
            let alpha = Math.max(0.2, intensity * 0.8) * life_fade; 
            
            ctx.fillStyle = 'rgba('+r+','+g+','+b+','+alpha+')';
            ctx.beginPath(); 
            // Thick spherical particle, explicitly larger for maximum visibility
            ctx.arc(px, py, Math.max(1.5, s*0.035), 0, Math.PI*2); 
            ctx.fill();
        }}
    }}
    
    // Draw magnets
    for (let m of magnets) {{
        let mw = 2.0, mh = 1.0;
        ctx.save();
        let [cx, cy] = toS(m.x, m.y);
        ctx.translate(cx, cy);
        ctx.rotate(-m.theta); // - because screen Y is flipped
        
        let pw = s * mw/2, ph = s * mh;
        // South (left, cyan)
        ctx.fillStyle = '#00FFFF'; ctx.fillRect(-pw, -ph/2, pw, ph);
        // North (right, red)
        ctx.fillStyle = '#FF4500'; ctx.fillRect(0, -ph/2, pw, ph);
        // Border
        ctx.strokeStyle = 'white'; ctx.lineWidth = 2;
        ctx.strokeRect(-pw, -ph/2, pw*2, ph);
        
        // Labels
        ctx.fillStyle = 'black'; ctx.font = 'bold '+Math.round(s*0.4)+'px Arial';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('S', -pw/2, 0);
        ctx.fillStyle = 'white';
        ctx.fillText('N', pw/2, 0);
        
        ctx.restore();
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
    <p>🔗 <strong>GitHub:</strong> <a href="https://github.com/Templariem/simulaciones_maxwell" style="color: #FFD700;" target="_blank">Repositorio oficial</a></p>
    <p>🏛️ <strong>Escuela de Ingeniería Eléctrica</strong></p>
    <p>🏰 <strong>Pontificia Universidad Católica de Valparaíso</strong></p>
    <p><strong>🇨🇱 Chile 🍷🗿</strong></p>
</div>
""", unsafe_allow_html=True)
