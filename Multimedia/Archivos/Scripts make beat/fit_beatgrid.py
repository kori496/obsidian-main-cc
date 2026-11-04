"""Ajusta la cuadricula de pulsos (BPM exacto + fase del primer golpe) sobre el .npy de analyze.py.
Uso: python3 -I fit_beatgrid.py <env.npy> [bpm_min bpm_max] [t_ini t_fin]
Ejemplos usados: tramo despues del drop 88.8-104 s con BPM 148-156 (video horizontal);
                 todo el audio con BPM 149-154 (video vertical .mov).
"""
import sys
import numpy as np
d = np.load(sys.argv[1]); t, f, r = d.T
bmin = float(sys.argv[2]) if len(sys.argv) > 2 else 148
bmax = float(sys.argv[3]) if len(sys.argv) > 3 else 156
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0
t1 = float(sys.argv[5]) if len(sys.argv) > 5 else t[-1]
m = (t > t0) & (t < t1); tt = t[m]; ff = f[m]
best = None
for bpm in np.arange(bmin, bmax, 0.02):
    P = 60 / bpm
    for ph in np.arange(0, P, 0.004):
        g = np.arange(t0 + ph, t1, P)
        idx = np.searchsorted(tt, g); idx = idx[idx < len(tt)]
        s = ff[idx].mean()
        if best is None or s > best[0]: best = (s, bpm, t0 + ph)
print('bpm %.2f  primer golpe %.3f s' % (best[1], best[2]))
P = 60 / best[1]
# cual de los 4 tiempos es el 1 del compas (el que mas flux tiene)
sc = [ff[np.clip(np.searchsorted(tt, np.arange(best[2] + k * P, t1, 4 * P)), 0, len(tt) - 1)].mean() for k in range(4)]
print('puntaje por tiempo del compas', [round(x) for x in sc])
