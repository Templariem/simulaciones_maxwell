import streamlit as st
import time as _time
import json

st.set_page_config(page_title="Vector de Poynting", page_icon="✨", layout="wide")

st.markdown("# ✨ Vector de Poynting: $\\vec{S} = \\frac{1}{\\mu_0} \\vec{E} \\times \\vec{B}$")

st.markdown("""
#### 📜 Contexto histórico
**John Henry Poynting** formuló en 1884 el teorema que describe cómo la
energía electromagnética fluye por el espacio. Contrario a la intuición, la energía no viaja
"dentro" de los cables, sino por los campos **E** y **B** que los rodean.

#### 🖥️ Simulación
Al encender el circuito, un pulso radial de energía S = (1/μ₀) E×B se propaga
desde la batería. Los electrones vibran donde la onda ha llegado y derivan una vez el circuito
se energiza completamente.
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
**John Henry Poynting** formulated in 1884 the theorem describing how
electromagnetic energy flows through space. Counterintuitively, the energy does not travel
"inside" the wires, but through the **E** and **B** fields surrounding them.

#### 🖥️ Simulation
When the circuit is turned on, a radial energy pulse S = (1/μ₀) E×B propagates
from the battery. Electrons vibrate where the wave has arrived and drift once the circuit
is fully energized.
""")

st.markdown("---")

# --- Event tracking (persistent) ---
if 'poyn_app_start' not in st.session_state:
    st.session_state.poyn_app_start = _time.time()
if 'poyn_events' not in st.session_state:
    st.session_state.poyn_events = []
if 'poyn_prev_on' not in st.session_state:
    st.session_state.poyn_prev_on = False

on_state = st.toggle("🔌 Encender Circuito", value=st.session_state.poyn_prev_on, key="poyn_on")

if on_state != st.session_state.poyn_prev_on:
    event_time = _time.time() - st.session_state.poyn_app_start
    st.session_state.poyn_events.append({'on': on_state, 't': event_time})
    st.session_state.poyn_prev_on = on_state

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Reiniciar", use_container_width=True):
        st.session_state.poyn_events = []
        st.session_state.poyn_app_start = _time.time()
        st.session_state.poyn_prev_on = False
        st.rerun()

events_json = json.dumps(st.session_state.poyn_events)
app_start_ms = int(st.session_state.poyn_app_start * 1000)

html_code = f"""
<canvas id="poyntingCanvas" style="display:block; margin:0 auto; border-radius:12px;"></canvas>
<script>
const canvas = document.getElementById('poyntingCanvas');
const ctx = canvas.getContext('2d');

function resize() {{
    const w = Math.min(window.innerWidth - 40, 800);
    canvas.width = w; canvas.height = w;
}}
resize();
window.addEventListener('resize', resize);

const EVENTS = {events_json};
const APP_START = {app_start_ms};
const LO = 7.0, LI = 5.0;
const SPEED = 22.0 / 15.0;
const BX = -6, BY = 0, LX = 6, LY = 0;
const T_TRANS = 2.0; // seconds for radial → stable transition

// ==========================================
// PRE-COMPUTE FIELD GRIDS (matching original)
// ==========================================
const gridStep = 1.0;
let gridPts = [];
for (let px = -9.5; px <= 9.5; px += gridStep) {{
    for (let py = -9.5; py <= 9.5; py += gridStep) {{
        let ma = Math.max(Math.abs(px), Math.abs(py));
        if (ma <= LO && ma >= LI) continue; // in wire
        gridPts.push({{x: px, y: py}});
    }}
}}

// Radial field (from battery)
function radialAt(px, py) {{
    let dx = px - BX, dy = py - BY;
    let r = Math.sqrt(dx*dx + dy*dy) + 0.1;
    let Sx = dx / (r*r), Sy = dy / (r*r);
    let n = Math.sqrt(Sx*Sx + Sy*Sy) + 1e-5;
    return [Sx/n, Sy/n];
}}

// Stable field (battery → bulb with radial-toward-cable component)
function stableAt(px, py) {{
    let rb = Math.sqrt((px-BX)**2 + (py-BY)**2) + 0.1;
    let rl = Math.sqrt((px-LX)**2 + (py-LY)**2) + 0.1;
    let Sx = (px-BX)/rb**3 - (px-LX)/rl**3;
    let Sy = (py-BY)/rb**3 - (py-LY)/rl**3;
    
    // Radial component toward cable
    let ma = Math.max(Math.abs(px), Math.abs(py));
    let crx = 0, cry = 0;
    if (ma > LO) {{ crx = -px/((ma+0.1)**2); cry = -py/((ma+0.1)**2); }}
    else if (ma < LI) {{
        if (Math.abs(px) >= Math.abs(py)) crx = Math.sign(px)/(ma+0.6);
        else cry = Math.sign(py)/(ma+0.6);
    }}
    Sx += 0.25*crx; Sy += 0.25*cry;
    let n = Math.sqrt(Sx*Sx + Sy*Sy) + 1e-5;
    return [Sx/n, Sy/n];
}}

// ==========================================
// PHYSICS: matching original poynting_EM.py
// ==========================================

// estado_del_campo: for a given distance, which events' waves have reached?
// Latest reached event determines if ON or OFF
function estadoDelCampo(dist, t) {{
    let isOn = false;
    for (let ev of EVENTS) {{
        let radio = (t - ev.t) * SPEED;
        if (dist < radio) isOn = ev.on;
    }}
    return isOn;
}}

// circuito_fluyendo: TRUE only if LAST event is ON and its wave >= 14.8
function circuitoFluyendo(t) {{
    if (EVENTS.length === 0) return false;
    let ultimo = EVENTS[EVENTS.length - 1];
    let radio = (t - ultimo.t) * SPEED;
    return ultimo.on === true && radio >= 14.8;
}}

// blend per point: only from ON events, how long since ON wave reached
function blendPorPunto(dist, t) {{
    let blend = 0;
    for (let ev of EVENTS) {{
        if (!ev.on) continue; // Only ON events contribute to blend
        let radio = (t - ev.t) * SPEED;
        if (dist < radio) {{
            let tLlegada = ev.t + dist / SPEED;
            let tiempoEnc = t - tLlegada;
            blend = Math.min(1, Math.max(0, tiempoEnc / T_TRANS));
        }}
    }}
    return blend;
}}

// ==========================================
// ELECTRONS (Drude gas)
// ==========================================
const NE = 2000;
let elec_L = [], elec_s_base = [];

// Pseudo-random deterministic function so positions are ALWAYS the same on re-render
function seededRandom(i) {{
    let x = Math.sin(i * 12.9898) * 43758.5453;
    return x - Math.floor(x);
}}

for (let i = 0; i < NE; i++) {{
    let L = 5.15 + seededRandom(i) * 1.7;
    elec_L.push(L);
    elec_s_base.push(seededRandom(i + 10000) * 8 * L);
}}

// Calculate exactly how much time the circuit has been ON (flowing) up to "now"
function calcTotalFlowTime(t) {{
    let total = 0;
    for (let i = 0; i < EVENTS.length; i++) {{
        let ev = EVENTS[i];
        if (ev.on) {{
            // It turned ON. Did it turn OFF later?
            let next_t = (i + 1 < EVENTS.length) ? EVENTS[i+1].t : t;
            // The flow starts once the wave reaches the full circuit (radius >= 14.8)
            let t_start_flow = ev.t + (14.8 / SPEED);
            if (next_t > t_start_flow) {{
                total += (next_t - t_start_flow);
            }}
        }}
    }}
    return Math.max(0, total);
}}

function eXY(s, L) {{
    const p = 8*L;
    let sm = ((s%p)+p)%p;
    if (sm < 2*L) return [-L, L-sm];
    if (sm < 4*L) return [-L+(sm-2*L), -L];
    if (sm < 6*L) return [L, -L+(sm-4*L)];
    return [L-(sm-6*L), L];
}}

function toS(wx, wy) {{
    const w = canvas.width, sc = w/20.0;
    return [w/2+wx*sc, w/2-wy*sc];
}}
function sc() {{ return canvas.width/20.0; }}

function drawArrow(x1,y1,x2,y2,color,lw) {{
    let dx=x2-x1,dy=y2-y1,len=Math.sqrt(dx*dx+dy*dy);
    if(len<1) return;
    ctx.strokeStyle=color; ctx.lineWidth=lw;
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    let hl=Math.min(len*0.35,5),a=Math.atan2(dy,dx);
    ctx.fillStyle=color; ctx.beginPath(); ctx.moveTo(x2,y2);
    ctx.lineTo(x2-hl*Math.cos(a-0.4),y2-hl*Math.sin(a-0.4));
    ctx.lineTo(x2-hl*Math.cos(a+0.4),y2-hl*Math.sin(a+0.4));
    ctx.closePath(); ctx.fill();
}}

function draw() {{
    const t = (Date.now() - APP_START) / 1000.0;
    const w = canvas.width, h = canvas.height, s = sc();
    
    ctx.fillStyle = '#000'; ctx.fillRect(0,0,w,h);
    
    // Title
    ctx.fillStyle='#fff'; ctx.font='bold '+Math.round(s*0.4)+'px Arial';
    ctx.textAlign='center';
    ctx.fillText('Vector de Poynting: S = (1/μ₀) E × B', w/2, s*0.7);
    
    // Cable ring
    ctx.strokeStyle='#8B4513'; ctx.lineWidth=2;
    let [ox1,oy1]=toS(-LO,LO), [ox2,oy2]=toS(LO,-LO);
    ctx.strokeRect(ox1,oy1,ox2-ox1,oy2-oy1);
    let [ix1,iy1]=toS(-LI,LI), [ix2,iy2]=toS(LI,-LI);
    ctx.strokeRect(ix1,iy1,ix2-ix1,iy2-iy1);
    ctx.fillStyle='#1a0a00';
    ctx.fillRect(ox1,oy1,ox2-ox1,iy1-oy1);
    ctx.fillRect(ox1,iy2,ox2-ox1,oy2-iy2);
    ctx.fillRect(ox1,iy1,ix1-ox1,iy2-iy1);
    ctx.fillRect(ix2,iy1,ox2-ix2,iy2-iy1);
    
    // Battery
    let [bx1,by1]=toS(-7,3);
    ctx.fillStyle='#222'; ctx.strokeStyle='white'; ctx.lineWidth=1.5;
    ctx.fillRect(bx1,by1,s*2,s*6); ctx.strokeRect(bx1,by1,s*2,s*6);
    let [cx1,cy1]=toS(-6.5,3.4);
    ctx.fillStyle='#CC0000'; ctx.fillRect(cx1,cy1,s*1,s*0.4);
    ctx.fillStyle='white'; ctx.font='bold '+Math.round(s*0.4)+'px Arial'; ctx.textAlign='center';
    let [tp,tp2]=toS(-6,2); ctx.fillText('+',tp,tp2);
    let [tm,tm2]=toS(-6,-2); ctx.fillText('−',tm,tm2);
    ctx.font=Math.round(s*0.35)+'px Arial'; let [tv,tv2]=toS(-6,0); ctx.fillText('V',tv,tv2);
    
    // --- Physics ---
    let isFlowing = circuitoFluyendo(t);
    let ampEnergized = estadoDelCampo(12.0, t);
    
    // Poynting vectors with blend (radial → stable per point)
    for (let pt of gridPts) {{
        let dist = Math.sqrt((pt.x-BX)**2 + (pt.y-BY)**2);
        let visible = estadoDelCampo(dist, t);
        if (!visible) continue;
        
        let blend = blendPorPunto(dist, t);
        let [srx, sry] = radialAt(pt.x, pt.y);
        let [sex, sey] = stableAt(pt.x, pt.y);
        let Sx = (1-blend)*srx + blend*sex;
        let Sy = (1-blend)*sry + blend*sey;
        let n = Math.sqrt(Sx*Sx + Sy*Sy) + 1e-5;
        Sx /= n; Sy /= n;
        
        let [ax1,ay1] = toS(pt.x, pt.y);
        let al = s * 0.45;
        drawArrow(ax1, ay1, ax1+Sx*al, ay1-Sy*al, '#FFD700', 1);
    }}
    
    // Electrons: vibrate if wave reached, drift based on TOTAL historical flow time
    let totalFlowTime = calcTotalFlowTime(t);
    // 9.0 drift units per second = 0.15 drift units per 16.6ms frame
    let driftOffset = totalFlowTime * 9.0;
    
    for (let i = 0; i < NE; i++) {{
        // Analytical position based on total time flowing, prevents jumping on page reload
        let current_s = (elec_s_base[i] + driftOffset) % (8 * elec_L[i]);
        
        let [bex, bey] = eXY(current_s, elec_L[i]);
        let eDist = Math.sqrt((bex-BX)**2 + (bey-BY)**2);
        let eReached = estadoDelCampo(eDist, t);
        
        let drawX = bex, drawY = bey;
        if (eReached) {{
            // Thermal vibration only if energized
            drawX += (Math.random()-0.5)*0.12;
            drawY += (Math.random()-0.5)*0.12;
        }}
        
        // Hide electrons inside the battery rectangle (x: -7 to -5, y: -3 to 3)
        if (drawX >= -7 && drawX <= -5 && drawY >= -3 && drawY <= 3) continue;
        
        let [esx, esy] = toS(drawX, drawY);
        ctx.fillStyle = '#FF1111';
        ctx.beginPath();
        ctx.arc(esx, esy, Math.max(1.5, s*0.035), 0, Math.PI*2);
        ctx.fill();
    }}
    
    // Bulb
    let [blx,bly] = toS(LX, LY);
    let bR = s*1.2;
    
    if (ampEnergized && isFlowing) {{
        // Fully on
        let grad=ctx.createRadialGradient(blx,bly,0,blx,bly,bR*2.5);
        grad.addColorStop(0,'rgba(255,255,200,0.8)'); grad.addColorStop(1,'rgba(255,255,0,0)');
        ctx.fillStyle=grad; ctx.beginPath(); ctx.arc(blx,bly,bR*2.5,0,Math.PI*2); ctx.fill();
        ctx.fillStyle='#FFFFBB';
    }} else if (ampEnergized && !isFlowing) {{
        // Energized but not flowing
        ctx.fillStyle='#666633';
    }} else {{
        ctx.fillStyle='#333333';
    }}
    ctx.strokeStyle='white'; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.arc(blx,bly,bR,0,Math.PI*2); ctx.fill(); ctx.stroke();
    
    let fc = (ampEnergized && isFlowing) ? '#FFFF80' : 
             (ampEnergized ? '#AAAA66' : '#444444');
    ctx.strokeStyle=fc; ctx.lineWidth=2;
    let [f1x,f1y]=toS(5.7,-0.3), [f2x,f2y]=toS(6,0.3), [f3x,f3y]=toS(6.3,-0.3);
    ctx.beginPath(); ctx.moveTo(f1x,f1y); ctx.lineTo(f2x,f2y); ctx.lineTo(f3x,f3y); ctx.stroke();
    
    // Filament glow
    if (ampEnergized && isFlowing) {{
        ctx.fillStyle='rgba(255,255,200,0.8)';
        ctx.beginPath(); ctx.arc(blx, bly-s*0.1, s*0.3, 0, Math.PI*2); ctx.fill();
    }}
    
    let [rbx,rby]=toS(5.5,-1.2);
    ctx.fillStyle='#AAA'; ctx.strokeStyle='white'; ctx.lineWidth=1;
    ctx.fillRect(rbx,rby,s*1,s*1.2); ctx.strokeRect(rbx,rby,s*1,s*1.2);
    
    // Info
    ctx.fillStyle='#888'; ctx.font=Math.round(s*0.25)+'px Arial'; ctx.textAlign='center';
    let estado = isFlowing ? '🟢 Circuito fluyendo' : (EVENTS.length > 0 ? '⚡ Onda propagándose' : '🔴 Apagado');
    ctx.fillText(estado + '  |  Eventos: ' + EVENTS.length + '  |  t = ' + t.toFixed(1)+'s', w/2, h-s*0.3);
    
    requestAnimationFrame(draw);
}}

draw();
</script>
"""

st.components.v1.html(html_code, height=820)

st.caption(f"📊 Eventos: {len(st.session_state.poyn_events)}")

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
