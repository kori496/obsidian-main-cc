"""Analiza el audio de un video: BPM aproximado, energia por tramos y la mejor ventana de 15 s.
Uso: python3 -I analyze.py <audio.wav mono 22050 Hz> <salida.npy>
Genera un .npy con columnas [t, flux, rms] (flux = flujo espectral, rms = volumen).
Preparar el wav:  ffmpeg -i video -vn -ac 1 -ar 22050 base.wav -y
"""
import numpy as np, scipy.io.wavfile as wf, sys
sr,a=wf.read(sys.argv[1]); a=a.astype(np.float32)/32768
hop=512; n=2048
frames=np.lib.stride_tricks.sliding_window_view(a,n)[::hop]*np.hanning(n)
spec=np.abs(np.fft.rfft(frames,axis=1))
logs=np.log1p(10*spec)
flux=np.maximum(0,np.diff(logs,axis=0)).sum(1); flux=np.r_[0,flux]
rms=np.sqrt((frames**2).mean(1))
fps=sr/hop; t=np.arange(len(rms))/fps
# tempo via autocorrelation of flux
f=flux-flux.mean(); ac=np.correlate(f,f,'full')[len(f)-1:]
lags=np.arange(len(ac)); bpms=60*fps/np.maximum(lags,1)
m=(bpms>70)&(bpms<180); L=lags[m][np.argmax(ac[m])]; bpm=60*fps/L
print("BPM approx",round(bpm,1))
# per-second energy
for s in range(0,int(t[-1]),3):
    sel=(t>=s)&(t<s+3); print(f"{s:3d}s rms={rms[sel].mean():.3f} flux={flux[sel].mean():.1f}")
# best 15s window
W=int(15*fps); score=np.convolve(rms/rms.max()+flux/flux.max(),np.ones(W),'valid')
i=np.argmax(score); print("best window start",round(i/fps,2))
np.save(sys.argv[2],np.c_[t,flux,rms])
