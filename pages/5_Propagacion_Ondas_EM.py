import streamlit as st

st.set_page_config(page_title="Ondas EM", page_icon="🌊", layout="wide")

st.markdown("# 🌊 Propagación de Ondas Electromagnéticas")

st.markdown("""
#### 📜 Contexto histórico
**Maxwell** predijo en 1865 la existencia de ondas electromagnéticas a partir
de sus ecuaciones. **Heinrich Hertz** las confirmó experimentalmente en 1887, demostrando que los
campos **E** y **B** oscilantes se propagan a la velocidad de la luz.

#### 🖥️ Simulación
Visualiza ondas en tres modos: **Longitudinal** (flechas 3D de E, B y S),
**Plana** (superficie 3D + mapa 2D) y **Radial** (propagación circular desde una fuente puntual).
""")

with st.expander("🇬🇧 English"):
    st.markdown("""
#### 📜 Historical context
**Maxwell** predicted in 1865 the existence of electromagnetic waves from
his equations. **Heinrich Hertz** confirmed them experimentally in 1887, demonstrating that
oscillating **E** and **B** fields propagate at the speed of light.

#### 🖥️ Simulation
Visualize waves in three modes: **Longitudinal** (3D arrows of E, B, and S),
**Plane** (3D surface + 2D map), and **Radial** (circular propagation from a point source).
""")

st.markdown("---")

modo = st.selectbox("Modo de Propagación", ["Longitudinal", "Plana", "Radial"])

modo_js = {"Longitudinal": "longitudinal", "Plana": "plana", "Radial": "radial"}[modo]

html_code = f"""
<div style="display:flex; flex-direction:column; align-items:center; gap:8px;">
    <canvas id="canvas3d" style="border-radius:12px;"></canvas>
    <canvas id="canvas2d" style="border-radius:12px;"></canvas>
</div>
<script>
const c3d = document.getElementById('canvas3d');
const ctx3 = c3d.getContext('2d');
const c2d = document.getElementById('canvas2d');
const ctx2 = c2d.getContext('2d');
const MODO = '{modo_js}';

function resize() {{
    const w = Math.min(window.innerWidth - 40, 850);
    if (MODO === 'longitudinal') {{
        c3d.width = 0; c3d.height = 0; c3d.style.display = 'none';
        c2d.width = w; c2d.height = w * 0.5;
    }} else {{
        c3d.width = w; c3d.height = w * 0.5; c3d.style.display = 'block';
        c2d.width = w; c2d.height = w * 0.5;
    }}
    c2d.style.display = 'block';
}}
resize();
window.addEventListener('resize', resize);

let t = 0;
const k = 0.5, omega = 0.5;

// --- 3D Projection — fixed diagonal ---
const camAngle = -0.75;
const camElev = 0.35;

function project(x3, y3, z3, cw, ch, cx, cy) {{
    // cx,cy = center offset in world coords
    let x3c = x3 - (cx||0), y3c = y3 - (cy||0);
    let ca = Math.cos(camAngle), sa = Math.sin(camAngle);
    let rx = x3c * ca + y3c * sa;
    let ry = -x3c * sa + y3c * ca;
    let ce = Math.cos(camElev), se = Math.sin(camElev);
    let rz = ry * se + z3 * ce;
    ry = ry * ce - z3 * se;
    let fov = 4.5;
    let sc = fov / (fov + ry * 0.12);
    return {{ sx: cw/2 + rx * cw * 0.04 * sc, sy: ch*0.5 - rz * ch * 0.04 * sc, d: ry, sc: sc }};
}}

// --- Colors: E=red, B=green, S=orange ---
const COL_E = '#FF3333';
const COL_B = '#33CC33';
const COL_S = '#FF8800'; // orange for Poynting everywhere

function drawArrow(ctx, x1, y1, x2, y2, color, lw) {{
    let dx = x2-x1, dy = y2-y1, len = Math.sqrt(dx*dx+dy*dy);
    if (len < 1.5) return;
    ctx.strokeStyle = color; ctx.lineWidth = lw;
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    let hl = Math.min(len*0.3, 10), a = Math.atan2(dy,dx);
    ctx.fillStyle = color; ctx.beginPath(); ctx.moveTo(x2,y2);
    ctx.lineTo(x2-hl*Math.cos(a-0.35), y2-hl*Math.sin(a-0.35));
    ctx.lineTo(x2-hl*Math.cos(a+0.35), y2-hl*Math.sin(a+0.35));
    ctx.closePath(); ctx.fill();
}}

function draw() {{
    t += 0.03;
    
    if (MODO === 'longitudinal') {{ drawLong2D(); }}
    else if (MODO === 'plana') {{ drawPlana3D(); drawPlana2D(); }}
    else {{ drawRadial3D(); drawRadial2D(); }}
    
    requestAnimationFrame(draw);
}}

// ======== LONGITUDINAL 3D ========
function drawLong3D() {{
    const w = c3d.width, h = c3d.height;
    ctx3.fillStyle = '#0E1117'; ctx3.fillRect(0,0,w,h);
    
    ctx3.fillStyle = '#fff'; ctx3.font = 'bold ' + Math.round(w*0.018) + 'px Arial';
    ctx3.textAlign = 'center';
    ctx3.fillText('Vista 3D — E (rojo, Y) · B (verde, Z) · S (naranja, X)', w/2, h*0.07);
    
    let p0 = project(0,0,0,w,h,10,0), pEnd = project(20,0,0,w,h,10,0);
    ctx3.strokeStyle = '#555'; ctx3.lineWidth = 1;
    ctx3.setLineDash([4,4]); ctx3.beginPath(); ctx3.moveTo(p0.sx,p0.sy); ctx3.lineTo(pEnd.sx,pEnd.sy); ctx3.stroke();
    ctx3.setLineDash([]);
    
    const N = 20;
    let arrows = [];
    for (let i = 0; i < N; i++) {{
        let xw = (i / (N-1)) * 20;
        let phase = k * xw - omega * t;
        let E = Math.cos(phase);
        let B = Math.cos(phase);
        let S = E * B;
        let base = project(xw, 0, 0, w, h, 10, 0);
        let tipE = project(xw, 0, E * 2.0, w, h, 10, 0);
        let tipB = project(xw, E * 2.0, 0, w, h, 10, 0);
        let tipS = project(xw + S * 1.8, 0, 0, w, h, 10, 0);
        arrows.push({{ bx:base.sx, by:base.sy, tx:tipE.sx, ty:tipE.sy, c:COL_E, d:base.d, lw:3.0 }});
        arrows.push({{ bx:base.sx, by:base.sy, tx:tipB.sx, ty:tipB.sy, c:COL_B, d:base.d-0.01, lw:3.0 }});
        arrows.push({{ bx:base.sx, by:base.sy, tx:tipS.sx, ty:tipS.sy, c:COL_S, d:base.d-0.02, lw:3.0 }});
    }}
    arrows.sort((a,b) => b.d - a.d);
    for (let a of arrows) drawArrow(ctx3, a.bx, a.by, a.tx, a.ty, a.c, a.lw || 3.0);
    
    let ly = h*0.96;
    ctx3.font = Math.round(w*0.013)+'px Arial'; ctx3.textAlign='center';
    ctx3.fillStyle = COL_E; ctx3.fillText('■ E (y)', w*0.3, ly);
    ctx3.fillStyle = COL_B; ctx3.fillText('■ B (z)', w*0.5, ly);
    ctx3.fillStyle = COL_S; ctx3.fillText('■ S (x)', w*0.7, ly);
}}

// ======== LONGITUDINAL 2D — E vertical, B tilted, S along axis ========
function drawLong2D() {{
    const w = c2d.width, h = c2d.height;
    ctx2.fillStyle = '#0E1117'; ctx2.fillRect(0,0,w,h);
    
    ctx2.fillStyle = '#fff'; ctx2.font = 'bold ' + Math.round(w*0.016)+'px Arial';
    ctx2.textAlign = 'center';
    ctx2.fillText('Onda Longitudinal', w/2, h*0.08);
    
    const mx = w*0.08, pw = w - 2*mx;
    const cy = h*0.52;
    const amp = h*0.28;
    
    // Propagation axis
    ctx2.strokeStyle = '#555'; ctx2.lineWidth = 1;
    ctx2.setLineDash([4,4]); ctx2.beginPath(); ctx2.moveTo(mx, cy); ctx2.lineTo(mx+pw, cy); ctx2.stroke();
    ctx2.setLineDash([]);
    // Axis label
    ctx2.fillStyle = '#666'; ctx2.font = Math.round(w*0.012)+'px Arial';
    ctx2.textAlign = 'right'; ctx2.fillText('x', mx+pw, cy-5);
    
    // E wave envelope (faint sine)
    ctx2.strokeStyle = 'rgba(255,50,50,0.15)'; ctx2.lineWidth = 1;
    ctx2.beginPath();
    for (let i = 0; i <= 200; i++) {{
        let xf = i/200, xw = xf*20;
        let E = Math.cos(k*xw - omega*t);
        let sx = mx + xf*pw, sy = cy - E*amp;
        if(i===0) ctx2.moveTo(sx,sy); else ctx2.lineTo(sx,sy);
    }}
    ctx2.stroke();
    
    const N = 20;
    const spacing = pw / N;
    for (let i = 0; i < N; i++) {{
        let xf = (i+0.5)/N, xw = xf*20;
        let phase = k*xw - omega*t;
        let E = Math.cos(phase);
        let B = Math.cos(phase);
        let S = E*B;
        let sx = mx + xf*pw;
        
        // E arrow (red, VERTICAL — Y axis)
        drawArrow(ctx2, sx, cy, sx, cy - E*amp, COL_E, 4.0);
        
        // B arrow (green, TILTED for 3D isometric effect — Z axis out/into page)
        drawArrow(ctx2, sx, cy, sx - B*spacing*0.5, cy + B*spacing*0.7, COL_B, 4.0);
        
        // S arrow (orange, along propagation axis — X axis)
        drawArrow(ctx2, sx, cy, sx + S * spacing * 1.0, cy, COL_S, 4.0);
    }}
    
    let ly = h*0.96;
    ctx2.font = Math.round(w*0.013)+'px Arial'; ctx2.textAlign='center';
    ctx2.fillStyle = COL_E; ctx2.fillText('■ E (↕ eje Y)', w*0.2, ly);
    ctx2.fillStyle = COL_B; ctx2.fillText('■ B (↔ eje Z)', w*0.5, ly);
    ctx2.fillStyle = COL_S; ctx2.fillText('■ S (→ eje X)', w*0.8, ly);
}}

// ======== PLANA 3D ========
function drawPlana3D() {{
    const w = c3d.width, h = c3d.height;
    ctx3.fillStyle = '#0E1117'; ctx3.fillRect(0,0,w,h);
    
    ctx3.fillStyle = '#fff'; ctx3.font = 'bold ' + Math.round(w*0.018)+'px Arial';
    ctx3.textAlign = 'center';
    ctx3.fillText('Onda Plana - 3D', w/2, h*0.05);
    
    const res = 35;
    let quads = [];
    for (let i=0;i<res-1;i++) {{
        for (let j=0;j<res-1;j++) {{
            let pts = [];
            for (let [di,dj] of [[0,0],[1,0],[1,1],[0,1]]) {{
                let xw = -10+((i+di)/res)*20, yw = -10+((j+dj)/res)*20;
                let Ez = Math.cos(k*(xw+10)-omega*t)*1.5;
                pts.push(project(xw*0.7,yw*0.7,Ez,w,h));
            }}
            let avgD = (pts[0].d+pts[1].d+pts[2].d+pts[3].d)/4;
            let xc = -10+((i+0.5)/res)*20;
            let Ec = Math.cos(k*(xc+10)-omega*t);
            quads.push({{pts,d:avgD,E:Ec}});
        }}
    }}
    quads.sort((a,b)=>b.d-a.d);
    for (let q of quads) {{
        // Direct colormap: Red(+1) #9C2A2A <-> Blue(-1) #D9EEFF — no white
        let E = q.E;
        let normE = Math.max(-1, Math.min(1, E));
        let tt = (normE + 1) / 2; // 0=blue, 1=red
        let r = Math.round(217 + tt * (156 - 217));
        let g = Math.round(238 + tt * (42 - 238));
        let b = Math.round(255 + tt * (42 - 255));
        ctx3.fillStyle='rgba('+r+','+g+','+b+',0.85)';
        ctx3.strokeStyle='rgba(100,100,100,0.15)'; ctx3.lineWidth=0.5;
        ctx3.beginPath(); ctx3.moveTo(q.pts[0].sx,q.pts[0].sy);
        for(let k2=1;k2<4;k2++) ctx3.lineTo(q.pts[k2].sx,q.pts[k2].sy);
        ctx3.closePath(); ctx3.fill(); ctx3.stroke();
    }}
    ctx3.font=Math.round(w*0.013)+'px Arial'; ctx3.textAlign='center';
    ctx3.fillStyle='#9C2A2A'; ctx3.fillText('■ E+',w*0.35,h*0.96);
    ctx3.fillStyle='#D9EEFF'; ctx3.fillText('■ E−',w*0.65,h*0.96);
}}

function drawPlana2D() {{
    const w=c2d.width, h=c2d.height;
    const m=w*0.06, pw=w-2*m, ph=h-2*m;
    
    ctx2.fillStyle='#0E1117'; ctx2.fillRect(0,0,w,h);
    ctx2.fillStyle='#fff'; ctx2.font='bold '+Math.round(w*0.016)+'px Arial';
    ctx2.textAlign='center';
    ctx2.fillText('Onda Plana - 2D', w/2, m*0.6);
    
    const res=60;
    const cw=pw/res, ch2=ph/res;
    for(let i=0;i<res;i++) {{
        for(let j=0;j<res;j++) {{
            let xw=-10+(i/res)*20;
            let E=Math.cos(k*(xw+10)-omega*t);
            // Direct colormap: Red(+1) #9C2A2A <-> Blue(-1) #D9EEFF
            let normE = Math.max(-1, Math.min(1, E));
            let tt = (normE + 1) / 2;
            let r = Math.round(217 + tt * (156 - 217));
            let g = Math.round(238 + tt * (42 - 238));
            let b = Math.round(255 + tt * (42 - 255));
            ctx2.fillStyle='rgb('+r+','+g+','+b+')'; ctx2.globalAlpha=0.6;
            ctx2.fillRect(m+i*cw,m+j*ch2,cw+1,ch2+1);
        }}
    }}
    ctx2.globalAlpha=1.0;
    
    const step=6;
    for(let i=0;i<res;i+=step) {{
        for(let j=0;j<res;j+=step) {{
            let xw=-10+(i/res)*20;
            let E=Math.cos(k*(xw+10)-omega*t);
            let sx=m+(i+step/2)*cw, sy=m+(j+step/2)*ch2;
            let aLen=cw*step*0.5;
            // B green arrows (vertical)
            drawArrow(ctx2,sx,sy,sx,sy+E*aLen,COL_B,4.0);
            // S orange arrows (horizontal)
            drawArrow(ctx2,sx,sy,sx+E*E*aLen*0.9,sy,COL_S,4.0);
        }}
    }}
    ctx2.font=Math.round(w*0.013)+'px Arial'; ctx2.textAlign='center';
    const ly=h-m*0.25;
    ctx2.fillStyle='#9C2A2A'; ctx2.fillText('■ E+',w*0.15,ly);
    ctx2.fillStyle='#D9EEFF'; ctx2.fillText('■ E−',w*0.3,ly);
    ctx2.fillStyle=COL_B; ctx2.fillText('■ B',w*0.5,ly);
    ctx2.fillStyle=COL_S; ctx2.fillText('■ S',w*0.75,ly);
}}

// ======== RADIAL 3D ========
function drawRadial3D() {{
    const w=c3d.width, h=c3d.height;
    ctx3.fillStyle='#0E1117'; ctx3.fillRect(0,0,w,h);
    ctx3.fillStyle='#fff'; ctx3.font='bold '+Math.round(w*0.018)+'px Arial';
    ctx3.textAlign='center';
    ctx3.fillText('Onda Radial - 3D', w/2, h*0.05);
    
    const res=35;
    let quads=[];
    for(let i=0;i<res-1;i++) {{
        for(let j=0;j<res-1;j++) {{
            let pts=[];
            for(let [di,dj] of [[0,0],[1,0],[1,1],[0,1]]) {{
                let xw=-10+((i+di)/res)*20, yw=-10+((j+dj)/res)*20;
                let R=Math.max(0.5,Math.sqrt(xw*xw+yw*yw));
                let Ez=Math.cos(k*R-omega*t)/Math.sqrt(R)*1.5;
                Ez=Math.max(-2,Math.min(2,Ez));
                pts.push(project(xw*0.7,yw*0.7,Ez,w,h));
            }}
            let avgD=(pts[0].d+pts[1].d+pts[2].d+pts[3].d)/4;
            let xc=-10+((i+0.5)/res)*20, yc=-10+((j+0.5)/res)*20;
            let Rc=Math.max(0.5,Math.sqrt(xc*xc+yc*yc));
            let Ec=Math.cos(k*Rc-omega*t)/Math.sqrt(Rc);
            Ec=Math.max(-1,Math.min(1,Ec));
            quads.push({{pts,d:avgD,E:Ec}});
        }}
    }}
    quads.sort((a,b)=>b.d-a.d);
    for(let q of quads) {{
        // Direct colormap: Red(+1) #9C2A2A <-> Blue(-1) #D9EEFF — no white
        let normE = Math.max(-1, Math.min(1, q.E));
        let tt = (normE + 1) / 2;
        let r = Math.round(217 + tt * (156 - 217));
        let g = Math.round(238 + tt * (42 - 238));
        let b = Math.round(255 + tt * (42 - 255));
        ctx3.fillStyle='rgba('+r+','+g+','+b+',0.85)';
        ctx3.strokeStyle='rgba(100,100,100,0.15)'; ctx3.lineWidth=0.5;
        ctx3.beginPath(); ctx3.moveTo(q.pts[0].sx,q.pts[0].sy);
        for(let k2=1;k2<4;k2++) ctx3.lineTo(q.pts[k2].sx,q.pts[k2].sy);
        ctx3.closePath(); ctx3.fill(); ctx3.stroke();
    }}
    ctx3.font=Math.round(w*0.013)+'px Arial'; ctx3.textAlign='center';
    ctx3.fillStyle='#9C2A2A'; ctx3.fillText('■ E+',w*0.35,h*0.96);
    ctx3.fillStyle='#D9EEFF'; ctx3.fillText('■ E−',w*0.65,h*0.96);
}}

function drawRadial2D() {{
    const w=c2d.width, h=c2d.height;
    const cx2=w/2, cy2=h/2, maxR=Math.min(w,h)*0.42;
    
    ctx2.fillStyle='#0E1117'; ctx2.fillRect(0,0,w,h);
    ctx2.fillStyle='#fff'; ctx2.font='bold '+Math.round(w*0.016)+'px Arial';
    ctx2.textAlign='center';
    ctx2.fillText('Onda Radial - 2D', w/2, h*0.05);
    
    const res=70, cs=maxR*2/res;
    for(let i=0;i<res;i++) {{
        for(let j=0;j<res;j++) {{
            let px=(i/res-0.5)*20, py=(j/res-0.5)*20;
            let R=Math.max(0.5,Math.sqrt(px*px+py*py));
            let E=Math.max(-1,Math.min(1,Math.cos(k*R-omega*t)/Math.sqrt(R)));
            // Direct colormap: Red(+1) #9C2A2A <-> Blue(-1) #D9EEFF
            let normE = Math.max(-1, Math.min(1, E));
            let tt = (normE + 1) / 2;
            let r = Math.round(217 + tt * (156 - 217));
            let g = Math.round(238 + tt * (42 - 238));
            let b = Math.round(255 + tt * (42 - 255));
            ctx2.fillStyle='rgb('+r+','+g+','+b+')'; ctx2.globalAlpha=0.6;
            ctx2.fillRect(cx2-maxR+i*cs,cy2-maxR+j*cs,cs+1,cs+1);
        }}
    }}
    ctx2.globalAlpha=1.0;
    ctx2.fillStyle='white'; ctx2.beginPath(); ctx2.arc(cx2,cy2,4,0,Math.PI*2); ctx2.fill();
    
    const step=10;
    for(let i=0;i<res;i+=step) {{
        for(let j=0;j<res;j+=step) {{
            // Centered perfectly in the step x step grid block
            let px=((i+step/2)/res-0.5)*20, py=((j+step/2)/res-0.5)*20;
            let R=Math.sqrt(px*px+py*py);
            if(R<1.5) continue;
            let E=Math.cos(k*R-omega*t)/Math.sqrt(R);
            let S=Math.cos(k*R-omega*t)**2/R;
            let sx=cx2+(px/10)*maxR, sy=cy2-(py/10)*maxR;
            // Larger arrows as requested
            let aLen=cs*step*0.9;
            let ux=-py/R, uy=px/R;
            // B green tangential
            drawArrow(ctx2,sx,sy,sx+ux*E*aLen,sy-uy*E*aLen,COL_B,4.0);
            let urx=px/R, ury=py/R;
            // S orange radial
            drawArrow(ctx2,sx,sy,sx+urx*S*aLen,sy-ury*S*aLen,COL_S,4.0);
        }}
    }}
    ctx2.font=Math.round(w*0.013)+'px Arial'; ctx2.textAlign='center';
    const ly=h-h*0.02;
    ctx2.fillStyle='#9C2A2A'; ctx2.fillText('■ E+',w*0.15,ly);
    ctx2.fillStyle='#D9EEFF'; ctx2.fillText('■ E−',w*0.3,ly);
    ctx2.fillStyle=COL_B; ctx2.fillText('■ B',w*0.5,ly);
    ctx2.fillStyle=COL_S; ctx2.fillText('■ S',w*0.75,ly);
}}

draw();
</script>
"""

height = 460 if modo == "Longitudinal" else 870

st.components.v1.html(html_code, height=height)

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
