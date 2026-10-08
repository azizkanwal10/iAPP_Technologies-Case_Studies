// "Meet our AI": a studio-lit AI headset that turns to face the cursor.
// Brushed aluminium frame, curved dark glass and a live display reading "iApp Technologies".
// Built with three.js and bundled to /assets/mascot.js (see package.json). Everything is drawn in code.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

// ---------- helpers ----------
const W = 2.5, H = 1.06, RAD = 0.47;         // front outline of the headset
const BEND_X = 2.4, BEND_Y = 7;              // curvature of the front

export function roundedRectPoints(w, h, r, n = 520) {
  // evenly spaced points around a rounded rectangle (dense, so the shape can be bent smoothly)
  const hw = w / 2, hh = h / 2, sx = w - 2 * r, sy = h - 2 * r, arc = (Math.PI / 2) * r;
  const per = 2 * sx + 2 * sy + 4 * arc, pts = [];
  const seg = [
    [sx, (t) => [-hw + r + t, -hh]],
    [arc, (t) => { const a = -Math.PI / 2 + t / r; return [hw - r + Math.cos(a) * r, -hh + r + Math.sin(a) * r]; }],
    [sy, (t) => [hw, -hh + r + t]],
    [arc, (t) => { const a = t / r; return [hw - r + Math.cos(a) * r, hh - r + Math.sin(a) * r]; }],
    [sx, (t) => [hw - r - t, hh]],
    [arc, (t) => { const a = Math.PI / 2 + t / r; return [-hw + r + Math.cos(a) * r, hh - r + Math.sin(a) * r]; }],
    [sy, (t) => [-hw, hh - r - t]],
    [arc, (t) => { const a = Math.PI + t / r; return [-hw + r + Math.cos(a) * r, -hh + r + Math.sin(a) * r]; }],
  ];
  for (let i = 0; i < n; i++) {
    let d = (i / n) * per, p;
    for (const [len, f] of seg) { if (d <= len) { p = f(d); break; } d -= len; }
    pts.push(new THREE.Vector2(p[0], p[1]));
  }
  return pts;
}

export function bend(geo, BX = BEND_X, BY = BEND_Y) {
  // wrap a flat, front-facing geometry around a horizontal and a gentle vertical curve
  const pos = geo.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) {
    v.fromBufferAttribute(pos, i);
    const a = v.x / BX, r1 = BX + v.z;
    const x = Math.sin(a) * r1; let z = Math.cos(a) * r1 - BX;
    const b = v.y / BY, r2 = BY + z;
    const y = Math.sin(b) * r2; z = Math.cos(b) * r2 - BY;
    pos.setXYZ(i, x, y, z);
  }
  geo.computeVertexNormals();
  return geo;
}

export function ringGeometry(w, h, r, inset, depth, bevel = 0.018, BX, BY) {
  const outer = new THREE.Shape(roundedRectPoints(w, h, r));
  outer.holes.push(new THREE.Path(roundedRectPoints(w - 2 * inset, h - 2 * inset, Math.max(0.05, r - inset)).reverse()));
  const g = new THREE.ExtrudeGeometry(outer, { depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 5, curveSegments: 4 });
  g.translate(0, 0, -depth - bevel);
  return bend(g, BX, BY);
}

export function solidGeometry(w, h, r, depth, bevel = 0.04, BX, BY) {
  const g = new THREE.ExtrudeGeometry(new THREE.Shape(roundedRectPoints(w, h, r)), { depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 6, curveSegments: 4 });
  g.translate(0, 0, -depth - bevel);
  return bend(g, BX, BY);
}

export function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export function roundedMask(w, h, r) {
  return canvasTex(1024, Math.round(1024 * h / w), (g, cw, ch) => {
    const s = cw / w; g.fillStyle = "#000"; g.fillRect(0, 0, cw, ch);
    g.fillStyle = "#fff"; g.beginPath(); g.roundRect(0, 0, cw, ch, r * s); g.fill();
  }, false);
}

export function knitBump() {
  const t = canvasTex(256, 256, (g) => {
    g.fillStyle = "#808080"; g.fillRect(0, 0, 256, 256);
    for (let y = 0; y < 256; y += 8) for (let x = 0; x < 256; x += 8) {
      const o = (y / 8) % 2 ? 4 : 0;
      const gr = g.createRadialGradient(x + o + 4, y + 4, 0, x + o + 4, y + 4, 5);
      gr.addColorStop(0, "#d0d0d0"); gr.addColorStop(1, "#505050");
      g.fillStyle = gr; g.beginPath(); g.ellipse(x + o + 4, y + 4, 3.6, 4.6, 0.5, 0, Math.PI * 2); g.fill();
    }
  }, false);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(6, 3);
  return t;
}

export function brushedRoughness() {
  const t = canvasTex(512, 64, (g, w, h) => {
    g.fillStyle = "#6a6a6a"; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 1400; i++) { const y = Math.random() * h, v = 90 + Math.random() * 60 | 0; g.fillStyle = `rgba(${v},${v},${v},.35)`; g.fillRect(0, y, w, 0.6 + Math.random()); }
  }, false);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(1, 8);
  return t;
}

export function studioEnvironment(renderer) {
  // a dark studio with soft boxes, used only for reflections
  const env = new THREE.Scene();
  env.background = new THREE.Color(0x050507);
  const box = (w, h, color, intensity, pos) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(intensity), side: THREE.DoubleSide }));
    m.position.set(...pos); m.lookAt(0, 0, 0); env.add(m);
  };
  box(8, 2.2, "#ffffff", 1.2, [0, 7, 2]);       // top strip
  box(2.2, 7, "#ffffff", 1.6, [-8, 1, 3]);      // left key
  box(2.2, 7, "#f3e8ff", 1.2, [8, 1, 2]);       // right fill
  box(5, 1.2, "#ff4d8d", 1.4, [-4, -2, -6]);    // magenta kicker
  box(5, 1.2, "#7c3aed", 1.5, [5, 2, -6]);      // violet kicker
  box(14, 4, "#1a1622", 1, [0, -6, 0]);         // floor bounce
  const pm = new THREE.PMREMGenerator(renderer);
  const tex = pm.fromScene(env, 0.02).texture;
  pm.dispose();
  return tex;
}

// ---------- display shader ----------
export function displayMaterial(text, sub = "AI  ·  AGENTS  ·  APPS") {
  const textTex = canvasTex(2048, 870, () => {}, true);
  const draw = () => {
    const c = textTex.image, g = c.getContext("2d");
    g.clearRect(0, 0, c.width, c.height);
    g.textAlign = "center"; g.textBaseline = "middle";
    g.font = "700 176px 'Archivo', 'Helvetica Neue', Arial, sans-serif";
    if ("letterSpacing" in g) g.letterSpacing = "2px";
    g.fillStyle = "#ffffff"; g.fillText(text, c.width / 2, c.height / 2 + 8);
    if (!sub) { textTex.needsUpdate = true; return; }
    g.font = "700 48px 'Space Mono', monospace";
    if ("letterSpacing" in g) g.letterSpacing = "18px";
    g.fillStyle = "rgba(255,255,255,.55)"; g.fillText(sub, c.width / 2, c.height / 2 + 150);
    textTex.needsUpdate = true;
  };
  draw();
  textTex.anisotropy = 16;
  if (document.fonts) Promise.all([document.fonts.load("700 176px Archivo"), document.fonts.load("500 44px 'Space Mono'")]).then(draw, () => {});
  return new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uText: { value: textTex } },
    vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `
      uniform float uTime; uniform sampler2D uText; varying vec2 vUv;
      float blob(vec2 p, vec2 c, float r){ return smoothstep(r, 0., length(p-c)); }
      void main(){
        vec2 p = vUv*vec2(2.36,1.);
        float t = uTime*.35;
        vec3 col = vec3(.015,.012,.03);
        col += vec3(.45,.12,.95) * blob(p, vec2(.7+.25*sin(t),.35+.12*cos(t*1.3)), .9) * .55;
        col += vec3(1.,.18,.48) * blob(p, vec2(1.7+.25*cos(t*.8),.62+.12*sin(t*1.1)), .85) * .5;
        col += vec3(.2,.45,1.)  * blob(p, vec2(1.2+.3*sin(t*.6+1.),.2+.1*cos(t)), .7) * .35;
        vec4 tx = texture2D(uText, vUv);
        col = mix(col*1.1, vec3(1.), smoothstep(.25,.6,tx.a));
        float e = smoothstep(0.,.06,vUv.x)*smoothstep(1.,.94,vUv.x)*smoothstep(0.,.14,vUv.y)*smoothstep(1.,.86,vUv.y);
        gl_FragColor = vec4(col*e, 1.);
      }`,
    toneMapped: false,
  });
}

// ---------- the headset ----------
function buildHeadset(text) {
  const g = new THREE.Group();

  const aluminium = new THREE.MeshPhysicalMaterial({ color: 0xd7d9de, metalness: 1, roughness: 0.4, roughnessMap: brushedRoughness(), anisotropy: 0.6, anisotropyRotation: Math.PI / 2, envMapIntensity: 1.0 });
  const darkMetal = new THREE.MeshPhysicalMaterial({ color: 0x2a2b30, metalness: 1, roughness: 0.38, envMapIntensity: 1 });
  const knit = knitBump();
  const fabric = new THREE.MeshPhysicalMaterial({ color: 0x24242a, roughness: 0.95, bumpMap: knit, bumpScale: 2.2, sheen: 0.6, sheenColor: new THREE.Color("#5b5670"), sheenRoughness: 0.8 });
  const seal = new THREE.MeshPhysicalMaterial({ color: 0x1a1a1f, roughness: 0.92, bumpMap: knit, bumpScale: 1.5, sheen: 0.4, sheenColor: new THREE.Color("#3d3a4a") });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x000000, metalness: 0, roughness: 0.03, clearcoat: 1, clearcoatRoughness: 0.02, transparent: true, opacity: 0.38, envMapIntensity: 2.2, alphaMap: roundedMask(W - 0.02, H - 0.02, RAD - 0.01), alphaTest: 0.5, depthWrite: false });

  const disp = displayMaterial(text);
  g.add(new THREE.Mesh(bend(new THREE.PlaneGeometry(W - 0.16, H - 0.16, 160, 48).translate(0, 0, -0.07)), disp));
  g.add(new THREE.Mesh(bend(new THREE.PlaneGeometry(W, H, 120, 40).translate(0, 0, -0.09)), new THREE.MeshBasicMaterial({ color: 0x000000 })));

  const glassMesh = new THREE.Mesh(bend(new THREE.PlaneGeometry(W - 0.02, H - 0.02, 160, 56).translate(0, 0, 0.004)), glass);
  glassMesh.renderOrder = 2; g.add(glassMesh);
  g.add(new THREE.Mesh(ringGeometry(W + 0.08, H + 0.08, RAD + 0.04, 0.07, 0.34), aluminium));
  const shell = new THREE.Mesh(solidGeometry(W + 0.02, H + 0.02, RAD + 0.01, 0.42, 0.06), darkMetal);
  shell.position.z = -0.34; g.add(shell);
  const sealMesh = new THREE.Mesh(solidGeometry(W - 0.12, H - 0.06, RAD - 0.04, 0.28, 0.1), seal);
  sealMesh.position.z = -0.78; g.add(sealMesh);

  // knitted strap: an open band around the back (the front gap sits inside the headset)
  const strap = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.5, 120, 1, true, 0.62, Math.PI * 2 - 1.24), fabric);
  strap.material.side = THREE.DoubleSide; strap.scale.set(1.17, 1, 1.05); strap.position.set(0, -0.02, -1.25); g.add(strap);
  [-1, 1].forEach((s) => {
    const c = new THREE.Mesh(new THREE.CapsuleGeometry(0.11, 0.34, 8, 24), aluminium);
    c.rotation.x = Math.PI / 2; c.position.set(s * 1.17, -0.02, -0.55); g.add(c);
  });

  const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 0.1, 48), aluminium);
  crown.position.set(0.86, H / 2 + 0.09, -0.22); g.add(crown);
  for (let i = 0; i < 36; i++) {
    const k = new THREE.Mesh(new THREE.BoxGeometry(0.008, 0.08, 0.012), darkMetal);
    const a = (i / 36) * Math.PI * 2; k.position.set(0.86 + Math.cos(a) * 0.077, H / 2 + 0.09, -0.22 + Math.sin(a) * 0.077); k.rotation.y = -a; g.add(k);
  }
  const button = new THREE.Mesh(new THREE.CapsuleGeometry(0.035, 0.22, 6, 16), aluminium);
  button.rotation.z = Math.PI / 2; button.position.set(-0.8, H / 2 + 0.05, -0.22); g.add(button);

  const sensorMat = new THREE.MeshPhysicalMaterial({ color: 0x050505, roughness: 0.1, metalness: 0.5, clearcoat: 1 });
  [-0.62, -0.3, 0.3, 0.62].forEach((x) => {
    const s = new THREE.Mesh(new THREE.CircleGeometry(0.032, 24), sensorMat);
    const a = x / BEND_X;
    s.position.set(Math.sin(a) * (BEND_X - 0.03), -H / 2 + 0.1, Math.cos(a) * (BEND_X - 0.03) - BEND_X); s.rotation.y = a; g.add(s);
  });

  g.position.y = 0.05;
  return { group: g, disp };
}

export const VignetteGrain = {
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898,78.233)))*43758.5453); }
    void main(){ vec4 c = texture2D(tDiffuse, vUv);
      float v = smoothstep(1.15, .35, length(vUv-.5)*1.35);
      c.rgb *= mix(.55, 1., v);
      c.rgb += (h(vUv*vec2(1920.,1080.)+uTime)-.5)*.018;
      gl_FragColor = c; }`,
};

export function mount(section, opts = {}) {
  const canvas = opts.canvas || section.querySelector("canvas");
  const text = opts.text || "iApp Technologies";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;

  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" }); }
  catch (e) { section.classList.add("no-webgl"); return; }
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  scene.environment = studioEnvironment(renderer);
  scene.background = canvasTex(1024, 1024, (g, w, h) => {
    g.fillStyle = "#030305"; g.fillRect(0, 0, w, h);
    let r = g.createRadialGradient(w * 0.5, h * 0.5, 10, w * 0.5, h * 0.5, w * 0.55);
    r.addColorStop(0, "rgba(64,30,110,.55)"); r.addColorStop(0.5, "rgba(30,14,52,.35)"); r.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = r; g.fillRect(0, 0, w, h);
    r = g.createRadialGradient(w * 0.5, h * 0.95, 10, w * 0.5, h * 0.95, w * 0.5);
    r.addColorStop(0, "rgba(140,30,90,.25)"); r.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = r; g.fillRect(0, 0, w, h);
  });

  const camera = new THREE.PerspectiveCamera(26, 1, 0.1, 100);
  const key = new THREE.DirectionalLight(0xffffff, 0.9); key.position.set(-4, 5, 6); scene.add(key);
  const rim = new THREE.DirectionalLight(0xb48cff, 0.9); rim.position.set(5, 2, -5); scene.add(rim);
  const rim2 = new THREE.DirectionalLight(0xff5c9a, 0.6); rim2.position.set(-5, -1, -4); scene.add(rim2);

  const hs = buildHeadset(text);
  const pivot = new THREE.Group(); pivot.add(hs.group); scene.add(pivot);

  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 1.6), new THREE.MeshBasicMaterial({
    transparent: true, depthWrite: false, toneMapped: false,
    map: canvasTex(256, 128, (g, w, h) => { const r = g.createRadialGradient(w / 2, h / 2, 2, w / 2, h / 2, w / 2); r.addColorStop(0, "rgba(0,0,0,.85)"); r.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = r; g.fillRect(0, 0, w, h); }),
  }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.set(0, -1.15, -0.5); scene.add(shadow);

  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(256, 256), 0.32, 0.35, 2.3));
  const grain = new ShaderPass(VignetteGrain); composer.addPass(grain);
  composer.addPass(new OutputPass());

  function resize() {
    const w = Math.max(1, canvas.clientWidth), h = Math.max(1, canvas.clientHeight);
    const dpr = Math.min(window.devicePixelRatio || 1, w < 700 ? 1.5 : 1.75);
    renderer.setPixelRatio(dpr); renderer.setSize(w, h, false);
    composer.setPixelRatio(dpr); composer.setSize(w, h);
    camera.aspect = w / h;
    const dist = camera.aspect < 1 ? 7.6 * Math.pow(1 / camera.aspect, 0.9) : 7.2;
    camera.position.set(0, 1.25, dist);
    camera.lookAt(0, camera.aspect < 1 ? 0.05 : -0.42, 0);
    camera.updateProjectionMatrix();
  }

  let tx = 0, ty = 0, yaw = 0, pitch = 0, vy = 0, vp = 0, lastMove = -1e9;
  const onMove = (e) => {
    const r = canvas.getBoundingClientRect();
    tx = THREE.MathUtils.clamp(((e.clientX - r.left) / r.width) * 2 - 1, -1.2, 1.2);
    ty = THREE.MathUtils.clamp(((e.clientY - r.top) / r.height) * 2 - 1, -1.2, 1.2);
    lastMove = performance.now();
  };
  if (fine) window.addEventListener("pointermove", onMove, { passive: true });
  else section.addEventListener("pointermove", onMove, { passive: true });

  const clock = new THREE.Timer();
  let running = false, raf = 0;
  function frame() {
    raf = 0; clock.update();
    const dt = Math.min(clock.getDelta(), 0.05), t = clock.getElapsed();
    const idle = performance.now() - lastMove > 2600;
    const gx = idle ? Math.sin(t * 0.35) * 0.6 : tx;
    const gy = idle ? Math.sin(t * 0.5) * 0.2 : ty;
    const targetYaw = gx * 0.6, targetPitch = gy * 0.28;
    vy += (targetYaw - yaw) * 34 * dt; vy *= Math.pow(0.0015, dt); yaw += vy * dt;
    vp += (targetPitch - pitch) * 34 * dt; vp *= Math.pow(0.0015, dt); pitch += vp * dt;
    pivot.rotation.set(pitch, yaw, -yaw * 0.06);
    pivot.position.y = Math.sin(t * 0.9) * 0.05;
    shadow.material.opacity = 0.75 - pivot.position.y * 1.5;
    shadow.scale.setScalar(1 - pivot.position.y * 0.6);
    hs.disp.uniforms.uTime.value = t;
    grain.uniforms.uTime.value = t * 60;
    composer.render();
    if (running && !reduce) raf = requestAnimationFrame(frame);
  }
  function start() { if (running) return; running = true; clock.update(); if (!raf) raf = requestAnimationFrame(frame); }
  function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }

  resize();
  if (reduce) { yaw = 0.25; pitch = 0.05; pivot.rotation.set(pitch, yaw, 0); composer.render(); }
  window.addEventListener("resize", () => { resize(); if (!running) composer.render(); });
  if (!opts.manual) {
    new IntersectionObserver((es) => { es[0].isIntersecting && !document.hidden ? start() : stop(); }).observe(section);
    document.addEventListener("visibilitychange", () => { document.hidden ? stop() : start(); });
  }
  const look = (x, y) => { tx = x; ty = y; lastMove = performance.now(); };
  return { scene, start, stop, look, render: () => composer.render() };
}
