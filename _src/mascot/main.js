// "Meet our AI" mascot: a glossy robot llama in neon goggles that follows the cursor.
// Built with three.js and bundled to /assets/mascot.js (see package.json). Everything is drawn in code.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

const NEON = new THREE.Color("#ff3d7f");
const VIOLET = new THREE.Color("#7c3aed");

function glowTexture(word) {
  const c = document.createElement("canvas");
  c.width = 2048; c.height = 1024;
  const g = c.getContext("2d");
  const r = g.createRadialGradient(1024, 760, 40, 1024, 760, 900);
  r.addColorStop(0, "rgba(110,16,80,0.75)");
  r.addColorStop(0.45, "rgba(60,10,55,0.4)");
  r.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = "#000"; g.fillRect(0, 0, 2048, 1024);
  g.fillStyle = r; g.fillRect(0, 0, 2048, 1024);
  // faint watermark word behind the character
  g.font = "400 430px 'Anton SC', 'Archivo', sans-serif";
  g.textAlign = "center"; g.textBaseline = "middle";
  const tg = g.createRadialGradient(1024, 560, 50, 1024, 560, 1100);
  tg.addColorStop(0, "rgba(142,127,148,0.02)");
  tg.addColorStop(0.7, "rgba(142,127,148,0.16)");
  g.fillStyle = tg; g.fillText(word, 1024, 560);
  // dot grid
  g.fillStyle = "rgba(255,255,255,0.06)";
  for (let y = 12; y < 1024; y += 32) for (let x = 12; x < 2048; x += 32) g.fillRect(x, y, 2, 2);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function visorTexture(text) {
  const c = document.createElement("canvas");
  c.width = 1536; c.height = 384;
  const g = c.getContext("2d");
  const draw = () => {
    g.clearRect(0, 0, c.width, c.height);
    g.textAlign = "center"; g.textBaseline = "middle";
    g.font = "800 150px 'Archivo', 'Arial Black', sans-serif";
    g.shadowColor = "#ff2d75"; g.shadowBlur = 36;
    g.fillStyle = "#ffd6e6"; g.fillText(text, 768, 200);
    g.shadowBlur = 8; g.fillStyle = "#ffffff"; g.fillText(text, 768, 200);
    tex.needsUpdate = true;
  };
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  draw();
  if (document.fonts) document.fonts.load("800 150px Archivo").then(draw, () => {});
  return tex;
}

function roundedRectCurve(w, h, r, z) {
  const pts = [], seg = 14, hw = w / 2 - r, hh = h / 2 - r;
  const corners = [[hw, hh, 0], [-hw, hh, Math.PI / 2], [-hw, -hh, Math.PI], [hw, -hh, Math.PI * 1.5]];
  for (const [cx, cy, a0] of corners)
    for (let i = 0; i <= seg; i++) {
      const a = a0 + (i / seg) * (Math.PI / 2);
      pts.push(new THREE.Vector3(cx + Math.cos(a) * r, cy + Math.sin(a) * r, z));
    }
  return new THREE.CatmullRomCurve3(pts, true, "centripetal");
}

function badgeTexture() {
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const g = c.getContext("2d");
  g.fillStyle = "#ffffff"; g.beginPath(); g.roundRect(8, 8, 240, 240, 64); g.fill();
  g.fillStyle = "#14171d"; g.font = "800 170px 'Archivo', 'Arial Black', sans-serif";
  g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("i", 128, 140);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

function buildMascot(text) {
  const pearl = new THREE.MeshPhysicalMaterial({ color: 0xf2ecf4, roughness: 0.42, clearcoat: 1, clearcoatRoughness: 0.18, sheen: 0.6, sheenColor: new THREE.Color("#ffb3d6"), sheenRoughness: 0.5 });
  const muzzleMat = new THREE.MeshPhysicalMaterial({ color: 0xd8cfe6, roughness: 0.5, clearcoat: 0.6, clearcoatRoughness: 0.3 });
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x1b1420, roughness: 0.6 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x040307, roughness: 0.22, metalness: 0.1, clearcoat: 1, clearcoatRoughness: 0.08, envMapIntensity: 0.45 });
  const strapMat = new THREE.MeshStandardMaterial({ color: 0x3a2433, roughness: 0.55, metalness: 0.2 });
  const jacket = new THREE.MeshPhysicalMaterial({ color: 0x3a1d3d, roughness: 0.75, sheen: 1, sheenColor: new THREE.Color("#ff6aa8"), sheenRoughness: 0.45 });
  const neon = new THREE.MeshBasicMaterial({ color: NEON.clone().multiplyScalar(3.2), toneMapped: false });
  const neonCore = new THREE.MeshBasicMaterial({ color: new THREE.Color("#ffc2d9").multiplyScalar(1.8), toneMapped: false });
  const innerEar = new THREE.MeshStandardMaterial({ color: 0xff9cc0, roughness: 0.5, emissive: 0xff3d7f, emissiveIntensity: 0.45 });

  const root = new THREE.Group();
  // body
  const torso = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), jacket);
  torso.scale.set(1.75, 1.05, 1.05); torso.position.set(0, -2.15, -0.1); root.add(torso);
  const collar = new THREE.Mesh(new THREE.TorusGeometry(0.56, 0.16, 24, 64), jacket);
  collar.rotation.x = Math.PI / 2; collar.position.set(0, -1.18, 0.02); root.add(collar);
  const badge = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.34, 0.06, 4, 0.08), new THREE.MeshStandardMaterial({ map: badgeTexture(), roughness: 0.4 }));
  badge.position.set(0.86, -1.62, 0.86); badge.rotation.set(-0.35, 0.55, 0); root.add(badge);

  // neck (pivot for the head sits at its top)
  const neckGroup = new THREE.Group(); neckGroup.position.set(0, -1.2, 0); root.add(neckGroup);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 1.5, 48), pearl);
  neck.position.y = 0.6; neckGroup.add(neck);

  const head = new THREE.Group(); head.position.set(0, 1.3, 0); neckGroup.add(head);
  const skull = new THREE.Mesh(new THREE.SphereGeometry(1, 72, 56), pearl);
  skull.scale.set(1.04, 0.96, 0.98); skull.position.y = 0.55; head.add(skull);
  // fluffy tuft
  [[0, 1.48, 0.15, 0.3], [-0.24, 1.42, 0.05, 0.24], [0.25, 1.43, 0.02, 0.25], [-0.08, 1.4, 0.38, 0.22], [0.14, 1.36, 0.42, 0.2]].forEach(([x, y, z, r]) => {
    const s = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 24), pearl); s.position.set(x, y, z); head.add(s);
  });
  // muzzle, nose and smile
  const muzzle = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 36), muzzleMat);
  muzzle.scale.set(0.56, 0.42, 0.5); muzzle.position.set(0, -0.2, 0.72); head.add(muzzle);
  [-0.12, 0.12].forEach((x) => { const n = new THREE.Mesh(new THREE.SphereGeometry(0.055, 16, 12), darkMat); n.scale.set(1.3, 0.7, 0.6); n.position.set(x, -0.06, 1.18); head.add(n); });
  const smile = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.022, 8, 32, Math.PI * 0.8), darkMat);
  smile.rotation.z = Math.PI + Math.PI * 0.1; smile.position.set(0, -0.26, 1.16); head.add(smile);

  // ears (they wiggle a little)
  const ears = [-1, 1].map((sx) => {
    const pivot = new THREE.Group(); pivot.position.set(sx * 0.6, 1.25, -0.08); pivot.rotation.z = -sx * 0.45; head.add(pivot);
    const ear = new THREE.Mesh(new THREE.CapsuleGeometry(0.19, 0.62, 10, 24), pearl);
    ear.scale.z = 0.55; ear.position.y = 0.42; pivot.add(ear);
    const inner = new THREE.Mesh(new THREE.CapsuleGeometry(0.11, 0.48, 8, 20), innerEar);
    inner.scale.z = 0.4; inner.position.set(0, 0.42, 0.07); pivot.add(inner);
    return { pivot, sx };
  });

  // goggles
  const visor = new THREE.Group(); visor.position.set(0, 0.68, 0.74); head.add(visor);
  const strap = new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.075, 16, 96), strapMat);
  strap.rotation.x = Math.PI / 2; strap.scale.set(1.05, 1.0, 1); strap.position.set(0, 0.68, 0); head.add(strap);
  const housing = new THREE.Mesh(new RoundedBoxGeometry(2.0, 0.78, 0.7, 6, 0.28), strapMat);
  housing.position.z = -0.12; housing.scale.z = 1.25; visor.add(housing);
  const lens = new THREE.Mesh(new RoundedBoxGeometry(1.86, 0.66, 0.7, 6, 0.24), glass);
  lens.position.z = 0.02; visor.add(lens);
  const zFront = 0.02 + 0.35;
  const tube = new THREE.Mesh(new THREE.TubeGeometry(roundedRectCurve(1.86, 0.66, 0.24, zFront + 0.005), 200, 0.046, 14, true), neon);
  visor.add(tube);
  const core = new THREE.Mesh(new THREE.TubeGeometry(roundedRectCurve(1.86, 0.66, 0.24, zFront + 0.04), 200, 0.009, 8, true), neonCore);
  visor.add(core);
  const textMat = new THREE.MeshBasicMaterial({ map: visorTexture(text), transparent: true, toneMapped: false, depthWrite: false });
  textMat.color.setScalar(1.6);
  const label = new THREE.Mesh(new THREE.PlaneGeometry(1.62, 0.405), textMat);
  label.position.z = zFront + 0.012; visor.add(label);
  const scanMat = new THREE.MeshBasicMaterial({ color: NEON.clone().multiplyScalar(1.4), transparent: true, opacity: 0, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending });
  const scan = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 0.56), scanMat);
  scan.position.z = zFront + 0.02; visor.add(scan);

  return { root, neckGroup, head, ears, torso, textMat, scan, scanMat };
}

export function mount(section, opts = {}) {
  const canvas = section.querySelector("canvas");
  const text = opts.text || "iApp Technologies";
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;

  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" }); }
  catch (e) { section.classList.add("no-webgl"); return; }
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.32;

  const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 100);

  const bgMat = new THREE.MeshBasicMaterial({ map: glowTexture(opts.watermark || "INTELLIGENCE"), toneMapped: false, depthWrite: false });
  const bg = new THREE.Mesh(new THREE.PlaneGeometry(36, 18), bgMat);
  bg.position.set(0, 0.6, -6); scene.add(bg);

  const key = new THREE.DirectionalLight(0xfff4ee, 1.5); key.position.set(-3, 4, 6); scene.add(key);
  const rimL = new THREE.DirectionalLight(NEON, 2.6); rimL.position.set(-5, 2, -4); scene.add(rimL);
  const rimR = new THREE.DirectionalLight(VIOLET, 2.4); rimR.position.set(5, 3, -4); scene.add(rimR);
  const fill = new THREE.PointLight(0xff4d8d, 2.2, 8, 2); fill.position.set(0, -1.2, 3.2); scene.add(fill);
  scene.add(new THREE.HemisphereLight(0x8a7fb8, 0x2a0a1e, 0.25));

  const m = buildMascot(text);
  scene.add(m.root);

  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.75, 0.4, 1.15);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());

  function resize() {
    const r = canvas.getBoundingClientRect();
    const w = Math.max(1, r.width), h = Math.max(1, r.height);
    const dpr = Math.min(window.devicePixelRatio || 1, w < 700 ? 1.5 : 1.75);
    renderer.setPixelRatio(dpr); renderer.setSize(w, h, false);
    composer.setPixelRatio(dpr); composer.setSize(w, h);
    camera.aspect = w / h;
    // keep the whole head in frame on narrow screens
    const need = camera.aspect < 0.9 ? 10.5 * Math.pow(0.9 / camera.aspect, 0.85) : 10.5;
    camera.position.set(0, 0.55, need);
    camera.lookAt(0, camera.aspect < 0.9 ? 0.35 : 0.15, 0);
    camera.updateProjectionMatrix();
  }

  // springy follow
  let tx = 0, ty = 0, yaw = 0, pitch = 0, vy = 0, vp = 0, lastMove = -1e9, earV = 0, earA = 0;
  const onMove = (e) => {
    const r = canvas.getBoundingClientRect();
    tx = THREE.MathUtils.clamp(((e.clientX - r.left) / r.width) * 2 - 1, -1.2, 1.2);
    ty = THREE.MathUtils.clamp(((e.clientY - r.top) / r.height) * 2 - 1.1, -1.2, 1.2);
    lastMove = performance.now();
  };
  if (fine) window.addEventListener("pointermove", onMove, { passive: true });
  else section.addEventListener("pointermove", onMove, { passive: true });

  const clock = new THREE.Timer();
  let running = false, raf = 0, nextBlink = 3, nextScan = 1.5;
  function frame() {
    raf = 0;
    clock.update(); const dt = Math.min(clock.getDelta(), 0.05), t = clock.getElapsed();
    const idle = performance.now() - lastMove > 2600;
    const gx = idle ? Math.sin(t * 0.45) * 0.55 + Math.sin(t * 1.3) * 0.08 : tx;
    const gy = idle ? Math.sin(t * 0.7) * 0.18 : ty;
    const targetYaw = gx * 0.62, targetPitch = gy * 0.32;
    vy += (targetYaw - yaw) * 60 * dt; vy *= Math.pow(0.0006, dt); yaw += vy * dt;
    vp += (targetPitch - pitch) * 60 * dt; vp *= Math.pow(0.0006, dt); pitch += vp * dt;
    m.head.rotation.set(pitch * 0.8, yaw * 0.75, -yaw * 0.08);
    m.neckGroup.rotation.set(pitch * 0.25, yaw * 0.3, -yaw * 0.04);
    m.root.rotation.y = yaw * 0.12;
    m.torso.scale.y = 1.05 + Math.sin(t * 1.6) * 0.012;
    // ears lag behind the head turn
    earV += ((-vy * 0.05) - earA) * 30 * dt; earV *= Math.pow(0.02, dt); earA += earV * dt;
    m.ears.forEach(({ pivot, sx }) => { pivot.rotation.z = -sx * 0.45 + earA + Math.sin(t * 2 + sx) * 0.03; });
    // visor blink and scan line
    let glow = 1;
    if (t > nextBlink) { const k = (t - nextBlink) / 0.18; glow = k < 1 ? 0.35 + 0.65 * Math.abs(1 - 2 * k) : 1; if (k >= 1) nextBlink = t + 3.5 + Math.random() * 3; }
    m.textMat.color.setScalar(1.6 * glow);
    if (t > nextScan) { const k = (t - nextScan) / 1.1; if (k < 1) { m.scan.position.x = -0.85 + 1.7 * k; m.scanMat.opacity = Math.sin(k * Math.PI) * 0.55; } else { m.scanMat.opacity = 0; nextScan = t + 2.8; } }
    composer.render();
    if (running && !reduce) raf = requestAnimationFrame(frame);
  }
  function start() { if (running) return; running = true; clock.update(); if (!raf) raf = requestAnimationFrame(frame); }
  function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }

  resize();
  if (reduce) { tx = 0.35; ty = -0.05; yaw = 0.2; pitch = -0.02; composer.render(); frame(); }
  window.addEventListener("resize", () => { resize(); if (!running) composer.render(); });
  new IntersectionObserver((es) => { es[0].isIntersecting && !document.hidden ? start() : stop(); }).observe(section);
  document.addEventListener("visibilitychange", () => { document.hidden ? stop() : start(); });
  section.classList.add("live");
  return { scene, mascot: m, render: () => composer.render() };
}
