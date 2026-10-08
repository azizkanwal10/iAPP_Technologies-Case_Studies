// "Meet our AI", version 2: a furred giraffe in iApp goggles that follows the cursor.
// The head and neck shape, coat colour and fur length are pre-baked by giraffe-mesh.mjs into /assets/giraffe.bin.
// Fur is drawn with the shell method: the surface is redrawn in many thin layers, and each layer keeps only the
// pixels that sit on a hair strand, so thousands of tapered hairs appear with soft, light-catching edges.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { bend, ringGeometry, solidGeometry, canvasTex, roundedMask, brushedRoughness, studioEnvironment, displayMaterial, VignetteGrain } from "./main.js";

const NECK_BASE = new THREE.Vector3(0, -4.6, -1.45);
const JOINT = new THREE.Vector3(0, -0.45, -0.5);

async function readGiraffe(url) {
  const buf = await (await fetch(url)).arrayBuffer();
  const h = new Uint32Array(buf, 0, 4), nv = h[1], ni = h[2], big = h[3];
  const pad = (n) => n + ((4 - (n % 4)) % 4);
  let o = 16;
  const pos = new Int16Array(buf, o, nv * 3); o = pad(o + nv * 6);
  const nrm = new Int8Array(buf, o, nv * 3); o = pad(o + nv * 3);
  const ao = new Uint8Array(buf, o, nv); o = pad(o + nv);
  const col = new Uint8Array(buf, o, nv * 3); o = pad(o + nv * 3);
  const fur = new Uint8Array(buf, o, nv); o = pad(o + nv);
  const idx = big ? new Uint32Array(buf, o, ni) : new Uint16Array(buf, o, ni);
  const g = new THREE.InstancedBufferGeometry();
  const P = new Float32Array(nv * 3); for (let i = 0; i < nv * 3; i++) P[i] = (pos[i] * 5) / 32767;
  g.setAttribute("position", new THREE.BufferAttribute(P, 3));
  g.setAttribute("normal", new THREE.BufferAttribute(nrm, 3, true));
  g.setAttribute("ao", new THREE.BufferAttribute(ao, 1, true));
  g.setAttribute("coat", new THREE.BufferAttribute(col, 3, true));
  g.setAttribute("fur", new THREE.BufferAttribute(fur, 1, true));
  g.setIndex(new THREE.BufferAttribute(idx, 1));
  g.computeBoundingSphere();
  return g;
}

function furMaterial(layers) {
  return new THREE.ShaderMaterial({
    uniforms: {
      uLayers: { value: layers }, uFurLen: { value: 0.03 }, uDensity: { value: 118 },
      uRn: { value: new THREE.Matrix3() }, uRh: { value: new THREE.Matrix3() }, uB: { value: NECK_BASE }, uJ: { value: JOINT },
      uKeyDir: { value: new THREE.Vector3(-0.45, 0.75, 0.5).normalize() }, uKeyCol: { value: new THREE.Color(1.35, 1.24, 1.12) },
      uFillDir: { value: new THREE.Vector3(0.7, 0.1, 0.6).normalize() }, uFillCol: { value: new THREE.Color(0.22, 0.18, 0.3) },
      uRimDir: { value: new THREE.Vector3(0.2, 0.4, -1).normalize() }, uRimCol: { value: new THREE.Color(1.1, 0.55, 0.85) },
      uAmb: { value: new THREE.Color(0.12, 0.1, 0.11) }, uWind: { value: 0 },
    },
    vertexShader: /* glsl */ `
      attribute float layer; attribute float ao; attribute vec3 coat; attribute float fur;
      uniform float uLayers, uFurLen, uWind; uniform mat3 uRn, uRh; uniform vec3 uB, uJ;
      varying vec3 vBase, vBaseN, vN, vComb, vWorld, vCoat; varying float vH, vAo, vFur;
      void main(){
        float h = layer / uLayers;
        vec3 p = position, n = normalize(normal);
        float L = uFurLen * fur * 3.2;
        // hair lies downwards along the surface; tufts on the ossicones stand up
        vec3 down = mix(vec3(0., -1., .18), vec3(0., 1., 0.), smoothstep(1.3, 1.45, p.y));
        vec3 comb = normalize(down - n * dot(down, n) + 1e-4);
        vec3 q = p + n * h * L + comb * h * h * L * 0.85 + vec3(sin(uWind + p.y * 3.) * .15, -.25, 0.) * h * h * L;
        // two-joint pose: neck pivots at its base, head pivots at the top of the neck
        float w = clamp(max(smoothstep(-.35, .05, p.z), smoothstep(-1.1, -.35, p.y)), 0., 1.);
        vec3 q1 = uB + uRn * (q - uB), q2 = uB + uRn * ((uJ - uB) + uRh * (q - uJ));
        vec3 fp = mix(q1, q2, w);
        vec3 n1 = uRn * n, n2 = uRn * (uRh * n), c1 = uRn * comb, c2 = uRn * (uRh * comb);
        vN = normalize(mat3(modelMatrix) * normalize(mix(n1, n2, w)));
        vComb = normalize(mat3(modelMatrix) * normalize(mix(c1, c2, w)));
        vBase = p; vBaseN = n; vH = h; vAo = ao; vCoat = coat; vFur = fur;
        vec4 wp = modelMatrix * vec4(fp, 1.); vWorld = wp.xyz;
        gl_Position = projectionMatrix * viewMatrix * wp;
      }`,
    fragmentShader: /* glsl */ `
      uniform float uDensity; uniform vec3 uKeyDir, uKeyCol, uFillDir, uFillCol, uRimDir, uRimCol, uAmb;
      varying vec3 vBase, vBaseN, vN, vComb, vWorld, vCoat; varying float vH, vAo, vFur;
      float hash(vec3 p){ p = fract(p * .3183099 + .1); p *= 17.; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
      void main(){
        float strand = 1.;
        if (vH > 0.001) {
          // strand grid in surface space: denser where the coat is short
          float dens = uDensity * mix(1.35, 1., clamp(vFur * 1.4, 0., 1.));
          vec3 g = vBase * dens, cell = floor(g), f = fract(g) - .5;
          float rnd = hash(cell), rnd2 = hash(cell + 17.31);
          f -= (vec3(rnd2, hash(cell + 3.7), hash(cell + 9.1)) - .5) * .5;
          float d = length(f - vBaseN * dot(f, vBaseN));
          float top = .45 + .55 * rnd;
          if (vH > top || vFur < .02) discard;
          float rad = .48 * (1. - vH / top);
          if (d > rad) discard;
          strand = .9 + .2 * rnd2;
        }
        vec3 N = normalize(vN), T = normalize(vComb), V = normalize(cameraPosition - vWorld);
        vec3 base = vCoat * strand;
        float rootShade = mix(.45, 1., pow(vH, .6));
        float occ = mix(.25, 1., vAo);
        vec3 col = base * rootShade * occ;
        // wrapped diffuse for soft fur, Kajiya-Kay highlight along the hair, and a coloured rim
        float dk = clamp((dot(N, uKeyDir) + .12) / 1.12, 0., 1.);
        float df = clamp((dot(N, uFillDir) + .5) / 1.5, 0., 1.);
        vec3 H = normalize(uKeyDir + V);
        float th = dot(T, H), spec = pow(sqrt(max(0., 1. - th * th)), 90.) * .28 * vH;
        float th2 = dot(T, normalize(uKeyDir + V + N * .25)), spec2 = pow(sqrt(max(0., 1. - th2 * th2)), 18.) * .1 * vH;
        float rim = pow(1. - max(dot(N, V), 0.), 3.) * max(dot(N, uRimDir) * .5 + .5, 0.);
        vec3 lit = col * (uAmb + uKeyCol * dk + uFillCol * df) + uKeyCol * (spec + spec2 * base) + uRimCol * rim * (.25 + .75 * vH) * base * 1.6;
        gl_FragColor = vec4(lit, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
  });
}

function buildGoggles(text) {
  const g = new THREE.Group();
  const GW = 1.56, GH = 0.46, GR = 0.2, BX = 1.05, BY = 3.5;
  const aluminium = new THREE.MeshPhysicalMaterial({ color: 0xd7d9de, metalness: 1, roughness: 0.58, roughnessMap: brushedRoughness(), anisotropy: 0.4, anisotropyRotation: Math.PI / 2, envMapIntensity: 0.32 });
  const darkMetal = new THREE.MeshPhysicalMaterial({ color: 0x24252a, metalness: 1, roughness: 0.4 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x000000, roughness: 0.06, clearcoat: 1, clearcoatRoughness: 0.05, transparent: true, opacity: 0.3, envMapIntensity: 0.9, alphaMap: roundedMask(GW - 0.02, GH - 0.02, GR - 0.01), alphaTest: 0.5, depthWrite: false });
  const disp = displayMaterial(text, "");
  g.add(new THREE.Mesh(bend(new THREE.PlaneGeometry(GW - 0.1, GH - 0.1, 120, 30).translate(0, 0, -0.05), BX, BY), disp));
  g.add(new THREE.Mesh(bend(new THREE.PlaneGeometry(GW, GH, 100, 24).translate(0, 0, -0.065), BX, BY), new THREE.MeshBasicMaterial({ color: 0 })));
  const gm = new THREE.Mesh(bend(new THREE.PlaneGeometry(GW - 0.02, GH - 0.02, 120, 30).translate(0, 0, 0.003), BX, BY), glass); gm.renderOrder = 2; g.add(gm);
  g.add(new THREE.Mesh(ringGeometry(GW + 0.06, GH + 0.06, GR + 0.03, 0.055, 0.2, 0.014, BX, BY), aluminium));
  const shell = new THREE.Mesh(solidGeometry(GW, GH, GR, 0.16, 0.03, BX, BY), darkMetal); shell.position.z = -0.2; g.add(shell);
  // elastic strap around the head
  const strap = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.13, 96, 1, true, 1.0, Math.PI * 2 - 2.0), new THREE.MeshStandardMaterial({ color: 0x1d1d22, roughness: 0.85, side: THREE.DoubleSide }));
  strap.scale.set(0.7, 1, 0.74); strap.position.set(0, 0, -0.78); g.add(strap);
  return { group: g, disp };
}

export async function mount(section, opts = {}) {
  const canvas = opts.canvas || section.querySelector("canvas");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const small = Math.min(innerWidth, innerHeight) < 700;

  let renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" }); }
  catch (e) { section.classList.add("no-webgl"); return; }
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  scene.environment = studioEnvironment(renderer);
  scene.background = canvasTex(1024, 1024, (g, w, h) => {
    g.fillStyle = "#040304"; g.fillRect(0, 0, w, h);
    let r = g.createRadialGradient(w * 0.5, h * 0.42, 10, w * 0.5, h * 0.42, w * 0.6);
    r.addColorStop(0, "rgba(58,40,52,.7)"); r.addColorStop(0.55, "rgba(24,16,26,.4)"); r.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = r; g.fillRect(0, 0, w, h);
  });
  const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 100);

  const layers = small ? 14 : 26;
  const geo = await readGiraffe(opts.mesh || "/assets/giraffe.bin");
  geo.setAttribute("layer", new THREE.InstancedBufferAttribute(new Float32Array([...Array(layers + 1).keys()]), 1));
  geo.instanceCount = layers + 1;
  const furMat = furMaterial(layers);
  const giraffe = new THREE.Mesh(geo, furMat);
  giraffe.frustumCulled = false;
  scene.add(giraffe);

  // goggles ride on the same two joints as the head
  const neckPivot = new THREE.Group(); neckPivot.position.copy(NECK_BASE); scene.add(neckPivot);
  const headPivot = new THREE.Group(); headPivot.position.copy(JOINT).sub(NECK_BASE); neckPivot.add(headPivot);
  const gog = buildGoggles(opts.text || "iApp Technologies");
  gog.group.position.set(0, 0.3, 0.8).sub(JOINT); headPivot.add(gog.group);

  const key = new THREE.DirectionalLight(0xffffff, 0.9); key.position.set(-4, 5, 6); scene.add(key);
  const rim = new THREE.DirectionalLight(0xb48cff, 0.8); rim.position.set(5, 2, -5); scene.add(rim);

  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(256, 256), 0.1, 0.25, 3.2));
  const grain = new ShaderPass(VignetteGrain); composer.addPass(grain);
  composer.addPass(new OutputPass());

  function resize() {
    const w = Math.max(1, canvas.clientWidth), h = Math.max(1, canvas.clientHeight);
    const dpr = Math.min(window.devicePixelRatio || 1, w < 700 ? 1.5 : 1.75);
    renderer.setPixelRatio(dpr); renderer.setSize(w, h, false);
    composer.setPixelRatio(dpr); composer.setSize(w, h);
    camera.aspect = w / h;
    const dist = camera.aspect < 1 ? 8.6 * Math.pow(1 / camera.aspect, 0.85) : 9.8;
    camera.position.set(0, 0.9, dist);
    camera.lookAt(0, camera.aspect < 1 ? 0.15 : -0.05, 0);
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

  const eN = new THREE.Euler(), eH = new THREE.Euler(), m4 = new THREE.Matrix4();
  function pose(t) {
    eN.set(pitch * 0.18, yaw * 0.3, -yaw * 0.04); eH.set(pitch * 0.85, yaw * 0.8, -yaw * 0.1);
    neckPivot.rotation.copy(eN); headPivot.rotation.copy(eH);
    furMat.uniforms.uRn.value.setFromMatrix4(m4.makeRotationFromEuler(eN));
    furMat.uniforms.uRh.value.setFromMatrix4(m4.makeRotationFromEuler(eH));
    furMat.uniforms.uWind.value = t * 0.8;
  }

  const clock = new THREE.Timer();
  let running = false, raf = 0;
  function frame() {
    raf = 0; clock.update();
    const dt = Math.min(clock.getDelta(), 0.05), t = clock.getElapsed();
    const idle = performance.now() - lastMove > 2600;
    const gx = idle ? Math.sin(t * 0.35) * 0.55 : tx;
    const gy = idle ? Math.sin(t * 0.5) * 0.18 : ty;
    vy += (gx * 0.62 - yaw) * 30 * dt; vy *= Math.pow(0.002, dt); yaw += vy * dt;
    vp += (gy * 0.3 - pitch) * 30 * dt; vp *= Math.pow(0.002, dt); pitch += vp * dt;
    pose(t);
    gog.disp.uniforms.uTime.value = t;
    grain.uniforms.uTime.value = t * 60;
    composer.render();
    if (running && !reduce) raf = requestAnimationFrame(frame);
  }
  function start() { if (running) return; running = true; clock.update(); if (!raf) raf = requestAnimationFrame(frame); }
  function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }

  resize();
  if (reduce) { yaw = 0.22; pitch = 0.04; pose(0); composer.render(); }
  window.addEventListener("resize", () => { resize(); if (!running) composer.render(); });
  if (!opts.manual) {
    new IntersectionObserver((es) => { es[0].isIntersecting && !document.hidden ? start() : stop(); }).observe(section);
    document.addEventListener("visibilitychange", () => { document.hidden ? stop() : start(); });
  }
  const look = (x, y) => { tx = x; ty = y; lastMove = performance.now(); };
  const setText = (t) => { gog.disp.userData.setText(t, ""); if (!running) composer.render(); };
  return { scene, start, stop, look, setText, render: () => composer.render() };
}
