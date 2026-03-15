import streamlit as st

st.set_page_config(page_title="Ley de Ampère-Maxwell", page_icon="🔌", layout="wide")

st.markdown("# 🔌 Ley de Ampère-Maxwell: $\\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J} + \\mu_0 \\varepsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$")

st.markdown("## A) Componente Ampère: $\\mu_0 \\mathbf{J}$")
st.markdown("""
#### 📜 Contexto histórico
**André-Marie Ampère** descubrió en 1820 que una corriente eléctrica genera
un campo magnético circular a su alrededor, estableciendo la conexión fundamental entre
electricidad y magnetismo.

#### 🖥️ Simulación
Los cables con corriente **saliente** (⊙) y **entrante** (⊗) generan campos
magnéticos en sentidos opuestos según la regla de la mano derecha. Añade cables y observa
cómo el campo se superpone dinámicamente.
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
**André-Marie Ampère** discovered in 1820 that an electric current generates
a circular magnetic field around it, establishing the fundamental connection between
electricity and magnetism.

#### 🖥️ Simulation
Wires with **outgoing** (⊙) and **incoming** (⊗) current generate magnetic fields
in opposite directions according to the right-hand rule. Add wires and observe
how the field superimposes dynamically.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)
if 'num_saliente' not in st.session_state:
    st.session_state.num_saliente = 1
if 'num_entrante' not in st.session_state:
    st.session_state.num_entrante = 0

with col1:
    if st.button("⊙ Añadir (Sale)", use_container_width=True):
        if st.session_state.num_saliente + st.session_state.num_entrante < 15:
            st.session_state.num_saliente += 1
            st.rerun()
with col2:
    if st.button("⊗ Añadir (Entra)", use_container_width=True):
        if st.session_state.num_saliente + st.session_state.num_entrante < 15:
            st.session_state.num_entrante += 1
            st.rerun()
with col3:
    if st.button("🗑️ Limpiar Todo", use_container_width=True):
        st.session_state.num_saliente = 0
        st.session_state.num_entrante = 0
        st.rerun()

n_s = st.session_state.num_saliente
n_e = st.session_state.num_entrante
st.caption(f"🟢 Salientes: {n_s}  ·  🔴 Entrantes: {n_e}  ·  Total: {n_s + n_e}")

html_code = f"""
<canvas id="canvasA" style="display:block; margin:0 auto; border-radius:12px;"></canvas>
<script>
const canvas = document.getElementById('canvasA');
const ctx = canvas.getContext('2d');
const NUM_SALIENTE = {n_s};
const NUM_ENTRANTE = {n_e};
const TOTAL = NUM_SALIENTE + NUM_ENTRANTE;

function resize() {{
    const w = Math.min(window.innerWidth - 40, 800);
    canvas.width = w; canvas.height = w;
}}
resize();
window.addEventListener('resize', resize);

const W = () => canvas.width, H = () => canvas.height;
const sc = () => W() / 12.0;
function toS(wx, wy) {{ return [W()/2 + wx*sc(), H()/2 - wy*sc()]; }}

// Particles for B field
const NUM_PART = 6000;
let particles = [];
for (let i=0; i<NUM_PART; i++) {{
    let l = Math.random()*80;
    particles.push({{
        x: (Math.random()-0.5)*13, y: (Math.random()-0.5)*13,
        life: l, max_life: l
    }});
}}

// Wires setup
let wires = [];
for (let i=0; i<TOTAL; i++) {{
    let isSaliente = i < NUM_SALIENTE;
    let angle = (i / Math.max(1, TOTAL)) * Math.PI * 2;
    let r = 2.0 + (i % 2) * 1.5;
    wires.push({{
        dir: isSaliente ? 1 : -1,
        mag: 2.0,
        base_angle: angle,
        base_r: r,
        p1: 0.5 + Math.random()*0.5,
        p2: 0.5 + Math.random()*0.5,
        x: 0, y: 0
    }});
}}

function BField(px, py) {{
    let Bx = 0, By = 0;
    for (let w of wires) {{
        let I_eff = w.dir * w.mag;
        let dx = px - w.x, dy = py - w.y;
        let r2 = dx*dx + dy*dy + 0.05; // smoothing
        Bx += I_eff * (-dy) / r2;
        By += I_eff * dx / r2;
    }}
    return [Bx, By];
}}

let t = 0;
function draw() {{
    t += 0.012;
    const w = W(), h = H(), s = sc();
    
    // Animate wires
    for (let i=0; i<TOTAL; i++) {{
        let cab = wires[i];
        let ang = cab.base_angle + t * cab.p1 * 0.7;
        let r_drift = cab.base_r + Math.sin(t * cab.p2 * 1.3) * 1.0;
        cab.x = Math.cos(ang) * r_drift;
        cab.y = Math.sin(ang) * r_drift;
    }}
    
    ctx.fillStyle = '#0E1117'; ctx.fillRect(0,0,w,h);
    ctx.fillStyle = '#fff'; ctx.font = 'bold '+Math.round(s*0.4)+'px Arial';
    ctx.textAlign='center'; ctx.fillText('Ley de Ampère: ∇×B = μ₀J', w/2, s*0.6);
    
    if (TOTAL > 0) {{
        for (let p of particles) {{
            let [bx, by] = BField(p.x, p.y);
            let mag = Math.sqrt(bx*bx + by*by) + 1e-4;
            // Particles flow along B vectors
            p.x += (bx/mag) * 0.06;
            p.y += (by/mag) * 0.06;
            p.life--;
            
            if (p.life <= 0 || Math.abs(p.x)>7 || Math.abs(p.y)>7) {{
                p.x = (Math.random()-0.5)*14;
                p.y = (Math.random()-0.5)*14;
                let l = 20 + Math.random()*60;
                p.life = l;
                p.max_life = l;
            }}
            
            let [px, py] = toS(p.x, p.y);
            let intensity = Math.min(1, mag * 0.3); // field drops off slower (1/r)
            
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
            // Thick spherical particle matching File 2
            ctx.arc(px, py, Math.max(1.5, s*0.035), 0, Math.PI*2); 
            ctx.fill();
        }}
    }}
    
    // Draw wires
    for (let cab of wires) {{
        let [cx, cy] = toS(cab.x, cab.y);
        ctx.fillStyle = cab.dir > 0 ? '#1E90FF' : '#FF3232'; // Blue and Red to contrast with Green field
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(cx, cy, s*0.35, 0, Math.PI*2); ctx.fill(); ctx.stroke();
        
        ctx.fillStyle = '#000'; ctx.font = 'bold '+Math.round(s*0.4)+'px Arial';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(cab.dir > 0 ? '•' : '×', cx, cy);
    }}
    
    requestAnimationFrame(draw);
}}

draw();
</script>
"""

st.components.v1.html(html_code, height=650)


# ==========================================
# SEGUNDA PARTE: Componente de Maxwell
# ==========================================
st.markdown("---")
st.markdown("## B) Componente Maxwell: $\\mu_0 \\varepsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$")
st.markdown("""
#### 📜 Contexto histórico
**James Clerk Maxwell**, en 1865, descubrió que la ley de Ampère estaba
incompleta. Entre las placas de un capacitor cargándose no hay corriente real ($J=0$), pero
aún así existe un campo magnético. Maxwell dedujo que un **campo eléctrico variable** en el
tiempo ($\partial \mathbf{E} / \partial t$) actúa como una “corriente de desplazamiento”.

#### 🖥️ Simulación
Observa cómo las partículas verdes orbitan entre las placas del capacitor 3D,
visualizando el campo magnético inducido por el cambio temporal del campo eléctrico.
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
**James Clerk Maxwell**, in 1865, discovered that Ampère's law was
incomplete. Between the plates of a charging capacitor there is no real current ($J=0$), yet
a magnetic field still exists. Maxwell deduced that a **time-varying electric field**
($\partial \mathbf{E} / \partial t$) acts as a “displacement current”.

#### 🖥️ Simulation
Observe how the green particles orbit between the 3D capacitor plates,
visualizing the magnetic field induced by the time-varying electric field.
""")

html_code_maxwell = f"""
<canvas id="canvasM" style="display:block; margin:0 auto; border-radius:12px;"></canvas>
<script>
const cvM = document.getElementById('canvasM');
const cxM = cvM.getContext('2d');

function resizeM() {{
    const w = Math.min(window.innerWidth - 40, 850);
    cvM.width = w; cvM.height = w * 0.6;
}}
resizeM();
window.addEventListener('resize', resizeM);

const WM = () => cvM.width, HM = () => cvM.height;

// Particles for induced B field in 3D
const NUM_PART_M = 4000;
let partsM = [];
for (let i=0; i<NUM_PART_M; i++) {{
    let l = Math.random()*80;
    partsM.push({{
        x: (Math.random()-0.5)*13, 
        y: (Math.random()-0.5)*13,
        z: (Math.random()-0.5)*13,
        life: l, max_life: l
    }});
}}

// 3D Projection functions
function project(x, y, z, w, h) {{
    // Isometric projection with slight rotation
    const angle = 0.4; 
    const cx = Math.cos(angle), sx = Math.sin(angle);
    // Rotate around Y axis
    let x1 = x * cx - z * sx;
    let z1 = x * sx + z * cx;
    
    // Tilt down
    const tilt = 0.3;
    const ct = Math.cos(tilt), st = Math.sin(tilt);
    let y1 = y * ct - z1 * st;
    let z2 = y * st + z1 * ct;
    
    // Perspective scale
    const dist = 35;
    const fov = 1000;
    const scale = fov / (fov + z2 + dist);
    
    return {{
        sx: w/2 + x1 * scale * 18,
        sy: h/2 - y1 * scale * 18,
        d: z2,
        scale: scale
    }};
}}

function drawArrow(ctx, x1, y1, x2, y2, color, lw=2.5) {{
    const dx = x2 - x1, dy = y2 - y1;
    const mag = Math.sqrt(dx*dx + dy*dy);
    if (mag < 0.1) return;
    
    ctx.strokeStyle = color; ctx.fillStyle = color;
    ctx.lineWidth = lw;
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    
    const headLen = Math.min(10, mag * 0.3);
    const angle = Math.atan2(dy, dx);
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI/6), y2 - headLen * Math.sin(angle - Math.PI/6));
    ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI/6), y2 - headLen * Math.sin(angle + Math.PI/6));
    ctx.closePath(); ctx.fill();
}}

let tm = 0;
function drawM() {{
    tm += 0.02;
    const w = WM(), h = HM();
    
    const omega = 1.0;
    const E_val = Math.sin(omega * tm);
    const dEdt = Math.cos(omega * tm);
    
    // Larger and centered plates, further apart
    const R = 8.5;   // Plate radius
    const D = 6.0;   // Half-distance between plates
    
    cxM.fillStyle = '#0E1117'; cxM.fillRect(0,0,w,h);
    cxM.fillStyle = '#fff'; cxM.font = 'bold '+Math.round(w*0.018)+'px Arial';
    cxM.textAlign='center'; cxM.fillText('Corriente de Desplazamiento: ∇×B = μ₀ε₀(∂E/∂t)', w/2, h*0.08);
    
    let drawQueue = [];
    
    // 1. Draw Plates and Wires using solid slice stacking (perfect 3D cylinders)
    for (let side of [-1, 1]) {{
        let x_inner = side * D;
        let x_outer = side * (D + 0.8); // Plate thickness 0.8
        
        let min_x = Math.min(x_inner, x_outer);
        let max_x = Math.max(x_inner, x_outer);
        
        // Stack slices for the thick plate
        for (let x = min_x; x <= max_x; x += 0.05) {{
            let perimeter = [];
            let center = project(x, 0, 0, w, h);
            for (let a=0; a<Math.PI*2; a+=0.15) {{
                perimeter.push(project(x, R * Math.cos(a), R * Math.sin(a), w, h));
            }}
            
            // Draw a stroke on the very edges (inner and outer faces)
            let isFace = (Math.abs(x - min_x) < 0.06 || Math.abs(x - max_x) < 0.06);
            
            drawQueue.push({{
                type: 'solid_slice', d: center.d, perim: perimeter, 
                color: 'rgb(80, 80, 90)', // Dark gray plate solid
                stroke: isFace ? 'rgba(0,0,0,0.8)' : 'rgb(60, 60, 65)',
                lw: isFace ? 2.0 : 1.0
            }});
        }}
        
        // Stack slices for the wire attached to the outer face
        let wire_outer = side * (D + 5.0);
        let w_min_x = Math.min(x_outer, wire_outer);
        let w_max_x = Math.max(x_outer, wire_outer);
        for (let x = w_min_x; x <= w_max_x; x += 0.1) {{
            let perimeter = [];
            let center = project(x, 0, 0, w, h);
            for (let a=0; a<Math.PI*2; a+=0.3) {{
                perimeter.push(project(x, 0.4 * Math.cos(a), 0.4 * Math.sin(a), w, h));
            }}
            drawQueue.push({{
                type: 'solid_slice', d: center.d, perim: perimeter, 
                color: 'rgb(50, 50, 50)', // Darker gray wire
                stroke: 'rgba(0,0,0,0.3)', lw: 1.0
            }});
        }}
        
        // Add charges (+ and -) on the inner surface of the plate (distributed across whole area)
        let sign = 0;
        if (side < 0) sign = E_val > 0 ? 1 : -1;
        if (side > 0) sign = E_val > 0 ? -1 : 1;
        
        let p_alpha = Math.abs(E_val);
        // Reduced step to increase density and ensure they cover edge to edge perfectly
        let e_step = 1.8; 
        if (p_alpha > 0.15) {{
            let chargeList = [];
            // Centered square grid covering the plate
            for (let cy=-R*0.85; cy<=R*0.85; cy+=e_step) {{
                for (let cz=-R*0.85; cz<=R*0.85; cz+=e_step) {{
                    if (cy*cy + cz*cz <= (R*0.85)*(R*0.85)) {{
                        // Apply an artificial offset for the left plate to counteract the isometric thickness distortion
                        let draw_x = x_inner;
                        if (side < 0) draw_x -= 0.5; // Shift left plate charges visually to the left edge
                        
                        let pp = project(draw_x, cy, cz, w, h);
                        chargeList.push(pp);
                    }}
                }}
            }}
            
            // Find the closest point of the plate to the camera to ensure charges draw on top
            let d1 = project(min_x, 0, 0, w, h).d;
            let d2 = project(max_x, 0, 0, w, h).d;
            let current_plate_closest_d = Math.min(d1, d2);

            drawQueue.push({{
                type: 'charge_group', 
                d: current_plate_closest_d - 0.1,  // force it to draw exactly after ALL slices of this plate
                charges: chargeList,
                sign: sign, 
                alpha: p_alpha
            }});
        }}
    }}
    
    // 2. E Field Arrows (Horizontal along X axis)
    const e_step = 2.5;
    for (let cy=-R*0.7; cy<=R*0.7; cy+=e_step) {{
        for (let cz=-R*0.7; cz<=R*0.7; cz+=e_step) {{
            if (cy*cy + cz*cz <= (R*0.8)*(R*0.8)) {{
                // Slight offset to start/end just inside the plates
                let sx = E_val > 0 ? -D + 0.5 : D - 0.5;
                let ex = E_val > 0 ? -D + 0.5 + Math.abs(E_val)*(2*D-1) : D - 0.5 - Math.abs(E_val)*(2*D-1);
                
                if (Math.abs(E_val) > 0.05) {{
                    let p1 = project(sx, cy, cz, w, h);
                    let p2 = project(ex, cy, cz, w, h);
                    let alpha = Math.max(0.2, Math.abs(E_val));
                    drawQueue.push({{ type: 'arrow', d: (p1.d+p2.d)/2, p1: p1, p2: p2, c: 'rgba(255,50,50,' + alpha + ')', lw: 2.5 }});
                }}
            }}
        }}
    }}
    
    // 3. Moving Particles for B Field (Orbiting in YZ Plane)
    for (let p of partsM) {{
        let r = Math.sqrt(p.y*p.y + p.z*p.z) + 1e-4;
        let b_mag = 0;
        if (r <= R) b_mag = (r / R) * dEdt * 3.5;
        else b_mag = (R / r) * dEdt * 3.5;
        
        // The rotation vector is perpendicular to the radial vector (p.y, p.z)
        // Its direction automatically flips when dEdt (and thus b_mag) changes sign
        let by = -p.z / r * b_mag;
        let bz = p.y / r * b_mag;
        
        // Exact physical synchronization: speed scales exactly with dE/dt. Stops completely at E_max.
        p.y += by * 0.12;
        p.z += bz * 0.12;
        p.life--;
        
        if (p.life <= 0 || r > 11.0) {{
            let angle = Math.random() * Math.PI * 2;
            let radius = Math.random() * R * 1.2;
            p.x = (Math.random() * 2 * D) - D;
            p.y = radius * Math.cos(angle);
            p.z = radius * Math.sin(angle);
            let l = 20 + Math.random() * 60;
            p.life = l;
            p.max_life = l;
        }}
        
        // Particles should fade smoothly instead of staying full-bright
        let speed_factor = Math.abs(b_mag);
        let intensity = Math.min(1, speed_factor * 0.4); 
        
        if (Math.abs(p.x) <= D) {{
            let pp = project(p.x, p.y, p.z, w, h);
            
            // 2-Color Gradient: White (weak) -> Green (strong)
            let cr=255, cg=255, cb=255;
            // White to Green transition
            cr = 255 - Math.round(intensity * 255);
            cb = 255 - Math.round(intensity * 255);
            
            let life_fade = Math.sin((p.life / p.max_life) * Math.PI);
            // Drastically increased baseline alpha and intensity multiplier so displacement current is very visible
            let alpha = Math.max(0.7, intensity * 1.5) * life_fade; 
            
            drawQueue.push({{ 
                type: 'point', d: pp.d, p: pp, 
                // Always visible with smooth fading
                c: 'rgba(' + cr + ',' + cg + ',' + cb + ',' + alpha + ')', 
                r: 0.8 // Thick radius for displacement current particles
            }});
        }}
    }}
    
    // Sort and Draw (Painter's Algorithm)
    drawQueue.sort((a,b) => b.d - a.d); 
    for (let q of drawQueue) {{
        if (q.type === 'solid_slice') {{
            cxM.fillStyle = q.color;
            cxM.strokeStyle = q.stroke;
            cxM.lineWidth = q.lw;
            cxM.beginPath();
            cxM.moveTo(q.perim[0].sx, q.perim[0].sy);
            for(let i=1; i<q.perim.length; i++) cxM.lineTo(q.perim[i].sx, q.perim[i].sy);
            cxM.closePath();
            cxM.fill();
            cxM.stroke();
            
        }} else if (q.type === 'charge_group') {{
            // Positive charge (blue), Negative charge (red)
            if (q.sign > 0) {{
                cxM.fillStyle = 'rgba(50, 150, 255, ' + q.alpha + ')';
                cxM.font = 'bold 20px Arial';
                cxM.textAlign = 'center'; cxM.textBaseline = 'middle';
                for (let pp of q.charges) {{
                    cxM.fillText('+', pp.sx, pp.sy);
                }}
            }} else if (q.sign < 0) {{
                cxM.fillStyle = 'rgba(255, 50, 50, ' + q.alpha + ')';
                cxM.font = 'bold 20px Arial';
                cxM.textAlign = 'center'; cxM.textBaseline = 'middle';
                for (let pp of q.charges) {{
                    cxM.fillText('−', pp.sx, pp.sy);
                }}
            }}
        }} else if (q.type === 'arrow') {{
            drawArrow(cxM, q.p1.sx, q.p1.sy, q.p2.sx, q.p2.sy, q.c, q.lw);
        }} else if (q.type === 'point') {{
            cxM.fillStyle = q.c;
            cxM.beginPath(); cxM.arc(q.p.sx, q.p.sy, q.r, 0, Math.PI*2); cxM.fill();
        }}
    }}
    
    // Legend
    let ly = h * 0.95;
    cxM.font = Math.round(w*0.015)+'px Arial'; cxM.textAlign='center';
    cxM.fillStyle = '#44FF44'; cxM.fillText('■ B (Flujo magnético)', w*0.2, ly);
    cxM.fillStyle = '#FF4444'; cxM.fillText('■ E / Cargas Negativas (-)', w*0.5, ly);
    cxM.fillStyle = '#4488FF'; cxM.fillText('■ Cargas Positivas (+)', w*0.8, ly);
    
    requestAnimationFrame(drawM);
}}

drawM();
</script>
"""

st.components.v1.html(html_code_maxwell, height=750)

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
