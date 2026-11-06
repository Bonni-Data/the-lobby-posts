#!/usr/bin/env python3
"""THE LOBBY - trascrive un audio (intervista radio, podcast) per scegliere le citazioni di Andrea.

Gira solo nella GitHub Action «Trascrivi audio» (.github/workflows/audio.yml): scarica l'audio indicato nel lavoro
jobs/audio/<nome>.json {"url": "https://...mp3", "clips": [[inizio_s, fine_s], ...]}, lo trascrive in italiano con
faster-whisper e salva la trascrizione con i tempi come artifact della Action (NON nel repository, che è pubblico).
Con "clips" ritaglia anche i pezzi indicati in clip_<n>.m4a, per montare un video con la voce di Andrea.
"""
import json
import os
import subprocess
import sys


def main(job_path, out_dir):
    job = json.load(open(job_path, encoding="utf-8"))
    url = job["url"]
    if not url.startswith("https://"):
        sys.exit("solo indirizzi https")
    os.makedirs(out_dir, exist_ok=True)
    audio = os.path.join(out_dir, "audio.mp3")
    subprocess.run(["curl", "-fsSL", "--max-filesize", "300000000", "-o", audio, url], check=True)
    for i, (a, b) in enumerate(job.get("clips", []), 1):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-to", str(b), "-i", audio,
                        "-c:a", "aac", "-b:a", "160k", os.path.join(out_dir, f"clip_{i}.m4a")], check=True)
    if job.get("transcribe", True):
        import numpy as np
        from faster_whisper import WhisperModel
        pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", audio, "-ar", "16000", "-ac", "1", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        samples = np.frombuffer(pcm, dtype=np.float32)
        model = WhisperModel(job.get("model", "medium"), device="cpu", compute_type="int8")
        segs, info = model.transcribe(samples, language="it", vad_filter=True, beam_size=5)
        lines = []
        with open(os.path.join(out_dir, "trascrizione.txt"), "w", encoding="utf-8") as f:
            for s in segs:
                m, sec = divmod(s.start, 60)
                line = f"[{int(m):02d}:{sec:05.2f} | {s.start:.1f}-{s.end:.1f}] {s.text.strip()}"
                lines.append(line)
                f.write(line + "\n")
        print(f"durata {info.duration:.0f} s, {len(lines)} segmenti")
    if not job.get("keep_audio"):
        os.remove(audio)


if __name__ == "__main__":
    main(*sys.argv[1:])
