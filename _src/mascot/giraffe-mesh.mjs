// Builds the giraffe head + neck mesh from a signed distance field and writes assets/giraffe.bin.
// Run: node giraffe-mesh.mjs   (from _src/mascot). Output layout is documented in readGiraffe() in giraffe.js.
import { writeFileSync } from "node:fs";

// ---------- SDF primitives ----------
const len = (x, y, z) => Math.sqrt(x * x + y * y + z * z);
function ellipsoid(px, py, pz, rx, ry, rz) {
  const k0 = len(px / rx, py / ry, pz / rz), k1 = len(px / (rx * rx), py / (ry * ry), pz / (rz * rz));
  return k1 === 0 ? -Math.min(rx, ry, rz) : (k0 * (k0 - 1)) / k1;
}
function roundCone(px, py, pz, ax, ay, az, bx, by, bz, r1, r2) {
  // capsule with different radii at each end (iq)
  const bax = bx - ax, bay = by - ay, baz = bz - az, l2 = bax * bax + bay * bay + baz * baz;
  const rr = r1 - r2, a2 = l2 - rr * rr, il2 = 1 / l2;
  const pax = px - ax, pay = py - ay, paz = pz - az;
  const y = pax * bax + pay * bay + paz * baz, z = y - l2;
  const xx = (pax * l2 - bax * y) ** 2 + (pay * l2 - bay * y) ** 2 + (paz * l2 - baz * y) ** 2;
  const y2 = y * y * l2, z2 = z * z * l2, k = Math.sign(rr) * rr * rr * xx;
  if (Math.sign(z) * a2 * z2 > k) return Math.sqrt(xx + z2) * il2 - r2;
  if (Math.sign(y) * a2 * y2 < k) return Math.sqrt(xx + y2) * il2 - r1;
  return (Math.sqrt(xx * a2 * il2) + y * rr) * il2 - r1;
}
const smin = (a, b, k) => { const h = Math.max(k - Math.abs(a - b), 0) / k; return Math.min(a, b) - h * h * k * 0.25; };
const smax = (a, b, k) => -smin(-a, -b, k);
function rotZ(x, y, a) { const c = Math.cos(a), s = Math.sin(a); return [c * x - s * y, s * x + c * y]; }
function rotX(y, z, a) { const c = Math.cos(a), s = Math.sin(a); return [c * y - s * z, s * y + c * z]; }

// Face points toward +z, forehead up (+y), muzzle down. Neck leaves from the back of the jaw.
export function sdf(x, y, z) {
  const ax = Math.abs(x);
  // skull and long face
  let d = ellipsoid(x, y - 0.5, z + 0.08, 0.6, 0.58, 0.6);
  d = smin(d, ellipsoid(x, y - 0.0, z - 0.1, 0.39, 0.92, 0.42), 0.35);
  // muzzle, nostrils, lips
  d = smin(d, ellipsoid(x, y + 0.88, z - 0.24, 0.44, 0.38, 0.42), 0.3);
  d = smin(d, ellipsoid(ax - 0.17, y + 0.88, z - 0.55, 0.17, 0.12, 0.13), 0.12);
  d = smax(d, -ellipsoid(ax - 0.19, y + 0.91, z - 0.67, 0.075, 0.042, 0.08), 0.035);
  d = smin(d, ellipsoid(x, y + 1.08, z - 0.38, 0.36, 0.12, 0.2), 0.1);
  d = smax(d, -ellipsoid(x, y + 1.17, z - 0.5, 0.3, 0.025, 0.12), 0.025);   // mouth line
  d = smin(d, ellipsoid(x, y + 1.22, z - 0.22, 0.28, 0.13, 0.22), 0.1);
  // cheeks, brows, eye bulges and the forehead lump
  d = smin(d, ellipsoid(ax - 0.3, y + 0.25, z + 0.05, 0.22, 0.38, 0.3), 0.2);
  d = smin(d, ellipsoid(ax - 0.33, y - 0.44, z - 0.3, 0.22, 0.1, 0.15), 0.12);
  d = smin(d, ellipsoid(ax - 0.48, y - 0.3, z - 0.18, 0.18, 0.16, 0.16), 0.1);
  d = smin(d, ellipsoid(x, y - 0.52, z - 0.37, 0.14, 0.2, 0.1), 0.15);
  // ossicones with knobbed tips
  for (const s of [-1, 1]) {
    d = smin(d, roundCone(x, y, z, s * 0.22, 0.9, -0.12, s * 0.29, 1.52, -0.26, 0.16, 0.12), 0.16);
    d = smin(d, ellipsoid(x - s * 0.295, y - 1.56, z + 0.27, 0.165, 0.15, 0.165), 0.07);
  }
  // ears: thin leaves angled out, cupped on the front
  for (const s of [-1, 1]) {
    let ex = x - s * 0.78, ey = y - 0.66, ez = z + 0.2;
    [ex, ey] = rotZ(ex, ey, s * 0.22);
    [ey, ez] = rotX(ey, ez, -0.25);
    let e = ellipsoid(ex - s * 0.08, ey, ez, 0.44, 0.17, 0.08);
    e = smax(e, -ellipsoid(ex - s * 0.12, ey, ez - 0.075, 0.33, 0.11, 0.05), 0.03);
    d = smin(d, e, 0.16);
  }
  // neck
  d = smin(d, roundCone(x, y, z, 0, -0.45, -0.5, 0, -4.6, -1.45, 0.36, 0.5), 0.4);
  return d;
}

// ---------- surface nets ----------
const S = 0.03, X0 = -1.55, Y0 = -4.4, Z0 = -1.75, NX = Math.ceil(3.1 / S), NY = Math.ceil(6.45 / S), NZ = Math.ceil(2.6 / S);
const idx = (i, j, k) => i + NX * (j + NY * k);
const F = new Float32Array(NX * NY * NZ);
for (let k = 0; k < NZ; k++) for (let j = 0; j < NY; j++) for (let i = 0; i < NX; i++) F[idx(i, j, k)] = sdf(X0 + i * S, Y0 + j * S, Z0 + k * S);

const vid = new Int32Array(NX * NY * NZ).fill(-1), P = [];
const corners = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]];
const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
for (let k = 0; k < NZ - 1; k++) for (let j = 0; j < NY - 1; j++) for (let i = 0; i < NX - 1; i++) {
  const v = corners.map(([a, b, c]) => F[idx(i + a, j + b, k + c)]);
  let neg = 0; for (const q of v) if (q < 0) neg++;
  if (neg === 0 || neg === 8) continue;
  let sx = 0, sy = 0, sz = 0, n = 0;
  for (const [a, b] of edges) {
    if ((v[a] < 0) === (v[b] < 0)) continue;
    const t = v[a] / (v[a] - v[b]), ca = corners[a], cb = corners[b];
    sx += ca[0] + (cb[0] - ca[0]) * t; sy += ca[1] + (cb[1] - ca[1]) * t; sz += ca[2] + (cb[2] - ca[2]) * t; n++;
  }
  vid[idx(i, j, k)] = P.length / 3;
  P.push(X0 + (i + sx / n) * S, Y0 + (j + sy / n) * S, Z0 + (k + sz / n) * S);
}
const I = [];
const quad = (a, b, c, d, flip) => { if (a < 0 || b < 0 || c < 0 || d < 0) return; if (flip) I.push(a, c, b, a, d, c); else I.push(a, b, c, a, c, d); };
for (let k = 1; k < NZ - 1; k++) for (let j = 1; j < NY - 1; j++) for (let i = 1; i < NX - 1; i++) {
  const f0 = F[idx(i, j, k)] < 0;
  if (f0 !== (F[idx(i + 1, j, k)] < 0)) quad(vid[idx(i, j - 1, k - 1)], vid[idx(i, j, k - 1)], vid[idx(i, j, k)], vid[idx(i, j - 1, k)], !f0);
  if (f0 !== (F[idx(i, j + 1, k)] < 0)) quad(vid[idx(i - 1, j, k - 1)], vid[idx(i - 1, j, k)], vid[idx(i, j, k)], vid[idx(i, j, k - 1)], !f0);
  if (f0 !== (F[idx(i, j, k + 1)] < 0)) quad(vid[idx(i - 1, j - 1, k)], vid[idx(i, j - 1, k)], vid[idx(i, j, k)], vid[idx(i - 1, j, k)], !f0);
}

// project vertices onto the surface, then take normals and ambient occlusion from the field
const nv = P.length / 3, N = new Float32Array(nv * 3), AO = new Uint8Array(nv), e = 0.004;
const grad = (x, y, z) => {
  const gx = sdf(x + e, y, z) - sdf(x - e, y, z), gy = sdf(x, y + e, z) - sdf(x, y - e, z), gz = sdf(x, y, z + e) - sdf(x, y, z - e);
  const l = len(gx, gy, gz) || 1; return [gx / l, gy / l, gz / l];
};
for (let v = 0; v < nv; v++) {
  let x = P[v * 3], y = P[v * 3 + 1], z = P[v * 3 + 2];
  for (let it = 0; it < 2; it++) { const d0 = sdf(x, y, z), [gx, gy, gz] = grad(x, y, z); x -= gx * d0; y -= gy * d0; z -= gz * d0; }
  P[v * 3] = x; P[v * 3 + 1] = y; P[v * 3 + 2] = z;
  const [nx, ny, nz] = grad(x, y, z); N[v * 3] = nx; N[v * 3 + 1] = ny; N[v * 3 + 2] = nz;
  let occ = 0, w = 1;
  for (let s = 1; s <= 5; s++) { const h = 0.045 * s; occ += w * (h - sdf(x + nx * h, y + ny * h, z + nz * h)); w *= 0.6; }
  AO[v] = Math.round(Math.max(0, Math.min(1, 1 - occ * 3.2)) * 255);
}

// ---------- coat: colour and fur length per vertex ----------
const fract = (v) => v - Math.floor(v);
const hash3 = (x, y, z) => fract(Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453);
function voronoi(x, y, z) {
  const ix = Math.floor(x), iy = Math.floor(y), iz = Math.floor(z);
  let f1 = 9, f2 = 9, id = 0;
  for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) for (let c = -1; c <= 1; c++) {
    const cx = ix + a, cy = iy + b, cz = iz + c;
    const px = cx + 0.15 + 0.7 * hash3(cx, cy, cz), py = cy + 0.15 + 0.7 * hash3(cy, cz, cx), pz = cz + 0.15 + 0.7 * hash3(cz, cx, cy);
    const d = len(x - px, y - py, z - pz);
    if (d < f1) { f2 = f1; f1 = d; id = hash3(cx + 3.1, cy + 7.7, cz + 1.3); } else if (d < f2) f2 = d;
  }
  return [f1, f2, id];
}
const mix3 = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const sstep = (e0, e1, x) => { const t = Math.max(0, Math.min(1, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t); };
const CREAM = [0.92, 0.84, 0.69], TAN = [0.8, 0.6, 0.38], MUZZLE = [0.86, 0.76, 0.62], DARK = [0.16, 0.1, 0.06];
const COL = new Uint8Array(nv * 3), FUR = new Uint8Array(nv);
for (let v = 0; v < nv; v++) {
  const x = P[v * 3], y = P[v * 3 + 1], z = P[v * 3 + 2], ax = Math.abs(x);
  const neck = sstep(-0.55, -1.25, y) * sstep(0.05, -0.35, z);        // 1 on the neck
  const face = 1 - neck;
  const muzzle = sstep(-0.55, -0.9, y) * sstep(-0.15, 0.15, z) * face;
  const ossTip = sstep(1.32, 1.48, y);
  const ossShaft = sstep(0.95, 1.1, y) * (1 - ossTip) * sstep(0.45, 0.3, ax);
  const ear = sstep(0.62, 0.78, ax) * sstep(0.2, 0.45, y);
  const mane = neck * sstep(-0.25, -0.55, z - (-0.5 + (y + 0.45) * 0.23)) * sstep(0.18, 0.05, ax);
  // reticulated patches: big on the neck, small and lighter on the face
  const sc = 2.4 + face * 2.6;
  const [f1, f2, id] = voronoi(x * sc + 11.3, y * sc * 0.85 + 4.1, z * sc + 7.9);
  const inside = sstep(0.07, 0.16 + face * 0.04, f2 - f1);
  const patchCol = mix3([0.34, 0.16, 0.06], [0.5, 0.27, 0.1], id);
  let c = mix3(CREAM, patchCol, inside * (neck * 0.95 + face * 0.7));
  c = mix3(c, [0.47, 0.29, 0.14], face * 0.72);                 // warmer, browner face
  c = mix3(c, [0.48, 0.27, 0.11], face * sstep(0.2, 0.35, z) * sstep(0.1, 0.4, y) * sstep(0.22, 0.05, ax) * 0.8); // darker forehead stripe
  c = mix3(c, MUZZLE, muzzle * 0.7);
  const nose = sstep(0.32, 0.12, len(ax - 0.18, y + 0.9, (z - 0.6) * 0.8)) * muzzle;
  c = mix3(c, [0.3, 0.2, 0.15], nose * 0.6);
  c = mix3(c, CREAM, ossShaft * 0.6);
  c = mix3(c, DARK, ossTip);
  c = mix3(c, mix3(CREAM, [0.95, 0.9, 0.82], 0.5), ear * sstep(-0.05, 0.1, N[v * 3 + 2]) * 0.7);
  c = mix3(c, [0.3, 0.17, 0.08], mane * 0.85);
  COL[v * 3] = c[0] * 255; COL[v * 3 + 1] = c[1] * 255; COL[v * 3 + 2] = c[2] * 255;
  let f = 0.42 * face + 0.95 * neck;
  f = f * (1 - muzzle * 0.55) * (1 - nose * 0.5);
  f = Math.max(f, ossTip * 2.6, mane * 2.4);
  f *= 1 - ear * 0.4;
  FUR[v] = Math.min(255, Math.round(f * 80));
}

// ---------- write: header | Int16 positions | Int8 normals | Uint8 AO | Uint8 RGB | Uint8 fur | Uint16/Uint32 indices ----------
const SCALE = 5 / 32767; // positions are within +-5 units
const big = nv > 65535;
const posQ = new Int16Array(nv * 3); for (let i = 0; i < nv * 3; i++) posQ[i] = Math.round(P[i] / SCALE);
const nrmQ = new Int8Array(nv * 3); for (let i = 0; i < nv * 3; i++) nrmQ[i] = Math.round(N[i] * 127);
const idxA = big ? new Uint32Array(I) : new Uint16Array(I);
const head = new Uint32Array([0x47524631, nv, I.length, big ? 1 : 0]);
const pad = (n) => (4 - (n % 4)) % 4;
const parts = [head, posQ, nrmQ, AO, COL, FUR], bufs = [];
let total = 0;
for (const p of parts) { const b = Buffer.from(p.buffer, p.byteOffset, p.byteLength); bufs.push(b, Buffer.alloc(pad(b.length))); total += b.length + pad(b.length); }
bufs.push(Buffer.from(idxA.buffer));
writeFileSync(new URL("../../assets/giraffe.bin", import.meta.url), Buffer.concat(bufs));
console.log(`grid ${NX}x${NY}x${NZ}, vertices ${nv}, triangles ${I.length / 3}, bytes ${total + idxA.byteLength}`);
