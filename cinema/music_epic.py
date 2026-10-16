#!/usr/bin/env python3
"""THE LOBBY - musica motivazionale sintetizzata (nessun brano di terzi).
Uso: python3 music_epic.py uscita.wav [durata_secondi]
120 BPM, Am F C G con arpeggio di piano, archi, basso, cassa, rullante in crescendo,
riser e impatto finale su Do maggiore. Gli stacchi cadono ogni 4 secondi (2 battute)."""
import sys, wave
import numpy as np

SR = 44100
BPM = 120
BEAT = 60 / BPM
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 25.0
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))

def env(n, a, d, s=0.0, rel=None):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / d))
    return e

def piano(m, dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = sum(np.sin(2 * np.pi * f * k * t) * (0.6 ** (k - 1)) for k in range(1, 6))
    return s * env(n, 0.004, 0.35) * 0.22

def pad(ms, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            f = hz(m) * 2 ** (det / 12)
            ph = 2 * np.pi * f * t + rng.uniform(0, 6)
            s += (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph))
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.4).clip(0, 1)
    return s * a * 0.035

def bass(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return s * env(n, 0.005, 0.5, 0.35) * np.minimum(1, (dur - t) / 0.05).clip(0, 1) * 0.30

def kick(g=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) * 0.9 * g

def snare(g=1.0):
    n = int(0.25 * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n) * np.exp(-t * 22)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    return (nz * 0.45 + tone * 0.4) * g

def boom():
    n = int(3.0 * SR); t = np.arange(n) / SR
    f = 32 + 70 * np.exp(-t * 6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    low = np.sin(ph) * np.exp(-t * 1.6)
    nz = rng.standard_normal(n) * np.exp(-t * 5) * 0.35
    return (low + nz) * 0.9

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    # crude rising high-pass by differencing a smoothed copy
    k = 30
    sm = np.convolve(nz, np.ones(k) / k, mode="same")
    hp = nz - sm
    f = 200 + 1800 * (t / dur) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    return (hp * 0.25 + tone) * (t / dur) ** 2.2

# progression: A minor, F, C, G (two beats each = half bar? no: one bar = 4 beats = 2 s)
CH = {"Am": [57, 60, 64], "F": [53, 57, 60], "C": [48, 55, 60, 64], "G": [55, 59, 62]}
ROOT = {"Am": 45, "F": 41, "C": 36, "G": 43}
seq = ["Am", "F", "C", "G", "Am", "F", "C", "G", "F", "G"]   # 10 bars = 20 s
BAR = 4 * BEAT
ARP = [0, 1, 2, 1, 2, 1, 0, 1]   # 8 eighths per bar
for b, ch in enumerate(seq):
    t0 = b * BAR
    notes = CH[ch]
    up = 12 if b >= 6 else 0
    for k in range(8):
        m = notes[ARP[k] % len(notes)] + 12 + up
        add(piano(m), t0 + k * BEAT / 2, 1.0 if b >= 2 else 0.8, pan=0.25 if k % 2 else -0.25)
    if b >= 2:
        add(pad([n + 12 for n in notes], BAR + 0.3), t0, 1.0 if b < 6 else 1.5)
    if b >= 4:
        for k in range(4):
            add(bass(ROOT[ch], BEAT * 0.95), t0 + k * BEAT, 1.0)
    if b >= 4:
        for k in range(4):
            if b < 6 and k % 2: continue
            add(kick(), t0 + k * BEAT, 1.0)
    if b >= 6 and b < 8:
        for k in (1, 3):
            add(snare(), t0 + k * BEAT, 0.8)
# build: bars 8-9 (16-20 s): snare roll accelerating + riser
for k in range(16):
    add(snare(0.35 + 0.5 * k / 16), 16 + k * BEAT / 2)
for k in range(16):
    add(snare(0.5 + 0.5 * k / 16), 18 + k * BEAT / 4)
for k in range(8):
    add(kick(0.8), 16 + k * BEAT)
add(riser(4.0), 16.0, 0.9)
# transitions: soft hits every 4 s
for tt in (4, 8, 12):
    add(boom() * 0.35, tt)
# drop at 20 s: impact + triumphant C major
add(boom(), 20.0, 1.0)
add(pad([60, 64, 67, 72, 76], 5.0), 20.0, 2.2)
for k, m in enumerate([72, 76, 79, 84]):
    add(piano(m, 3.0), 20.0 + k * 0.06, 1.3)
add(bass(36, 4.5), 20.0, 1.2)
for k in (0, 2):
    add(kick(1.0), 20.0 + k * BEAT * 2)

# reverb via FFT convolution with a decaying-noise impulse
def reverb(x, secs=1.8, mix=0.22):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t * 3.2); ir[0] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    m = len(x) + n
    nfft = 1 << (m - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[: len(x)]
    return x * (1 - mix) + y * mix * 0.6
L = reverb(L); R = reverb(R)
# fade in/out, limiter
t = np.arange(N) / SR
fade = np.minimum(1, t / 0.3) * np.clip((DUR - t) / 1.2, 0, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L = np.tanh(L / peak * 1.4) * 0.89; R = np.tanh(R / peak * 1.4) * 0.89
data = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
print("ok", sys.argv[1], DUR, "s")
