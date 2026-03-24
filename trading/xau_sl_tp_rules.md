# XAUUSD – SL & TP Rules (Afu + Clio Nova)

## Konteks Strategi
- Pair: XAUUSD
- Timeframe utama setup: H1 (regime) + M30 (setup) (+ M15/M5/M1 untuk timing)
- Filter arah:
  - H1: posisi harga terhadap awan Ichimoku
    - Di bawah awan → bias SELL
    - Di atas awan → bias BUY
- Setup contoh utama: **fake breakout** terhadap awan di M30
  - Harga sempat break berlawanan arah (keluar awan), lalu kembali ke sisi trend (re-entry ke dalam/bawah awan)
  - Konfirmasi: Stoch, RSI, OsMA (minimal 2–3 confluence)

## Aturan Stop Loss (SL)

1. SL selalu berbasis struktur, bukan angka random
   - SELL:
     - Level invalidasi = **top fake breakout** (highest high dari swing yang nembus awan)
     - `SL = high_fake_breakout + buffer`
   - BUY:
     - Level invalidasi = **bottom fake breakdown** (lowest low dari swing yang nembus awan)
     - `SL = low_fake_breakdown - buffer`

2. Buffer SL (anti spike, tetap hemat)
   - Buffer diambil dari volatilitas timeframe setup (misal M30):
     - `buffer ≈ 0.3–0.5 × ATR(M30)`
   - Ide: cukup jauh di luar swing + noise normal, tapi tidak berlebihan sehingga merusak RR.

3. Max SL (khusus XAU, orientasi M30/M15)
   - Untuk setup M30/H1:
     - `max_SL_distance ≈ 15$` dari entry ke SL
   - Untuk entry M15:
     - `max_SL_distance ≈ 10$`
   - Jika struktur invalidasi + buffer melebihi batas ini **dan** membuat RR ke target wajar jelek → trade di-skip.
   - Prinsip: "Kalau ideku butuh SL lebih dari X$, berarti entry-ku jelek atau market belum kasih spot ideal → lebih baik nunggu."

## Aturan Take Profit (TP)

1. TP utama selalu di level struktural wajar
   - SELL:
     - **TP1** = swing low signifikan terakhir di M30
     - **TP2 (opsional)** = area FVG / support berikutnya di bawah
   - BUY:
     - **TP1** = swing high signifikan terakhir di M30
     - **TP2 (opsional)** = area FVG / resistance berikutnya di atas

2. RR minimum
   - Hitung jarak:
     - `risk_price = |Entry - SL|`
     - `reward_price_TP1 = |Entry - TP1|`
   - Hitung RR:
     - `RR1 = reward_price_TP1 / risk_price`
   - Aturan:
     - Default hukum: `RR_min_default = 1 : 2`
     - Boleh `RR ≈ 1 : 1.5` hanya jika setup A+ (multi-confluence, level sangat bersih, biasanya reversion cepat).
     - Jika `RR1 < 1.5` → trade auto skip.
     - Jika `1.5 ≤ RR1 < 2` → boleh **hanya** jika setup A+.
     - Jika `RR1 ≥ 2` → hijau, boleh diambil (kalau syarat lain oke).

3. Extended target (TP2)
   - Hitung juga `RR2 = |Entry - TP2| / risk_price`.
   - Skenario ideal:
     - TP1 sekitar 1–1.5R (boleh partial close),
     - TP2 di 2–3R (swing/FVG berikutnya yang masih logis secara struktur).
   - Jika `RR1 < 1.5` tapi `RR2 ≥ 2` dan TP2 berada di level struktural kuat (misal FVG besar / S/R jelas), bisa dipertimbangkan **dengan disiplin**.

## Rumus & Checklist Praktis Sebelum Entry

1. Tentukan:
   - `Entry = E`
   - `SL = S` (berdasarkan struktur invalidasi + buffer ATR)
   - `TP_struktural = T1` (swing low/high wajar searah posisi)

2. Hitung:
   - `risk_price = |E - S|`
   - `reward_price = |E - T1|`
   - `RR = reward_price / risk_price`

3. Keputusan:
   - Jika `RR < 1.5` → **jangan entry**.
   - Jika `1.5 ≤ RR < 2` → entry **hanya jika** setup A+ (H1 searah, level bersih, fake breakout jelas, indikator kompak).
   - Jika `RR ≥ 2` → **oke**, lanjut (selama rule lain terpenuhi).

4. Optional trade management:
   - Saat price mencapai ±1–1.5R:
     - Boleh partial close (misal 50%) dan/atau geser SL → BE / +0.2R.
   - Sisanya diarahkan ke TP akhir (TP1/TP2) sesuai struktur.

## Catatan Untuk Engine Nanti

- Hard rule EA:
  - `if RR(entry, SL, TP1) < 1.5 → no trade`.
- Konfigurasi yang bisa diatur:
  - `RR_min_default = 2.0`
  - `RR_min_aggressive = 1.5`
  - `max_SL_distance_M30 = 15$`
  - `max_SL_distance_M15 = 10$`
- SL logic:
  - selalu di `structure_invalid + k * ATR`.
- TP logic:
  - TP1 = swing, TP2 = FVG/level lanjutan.

Dokumen ini adalah snapshot ide Afu + Clio Nova per Maret 2026 untuk XAU SL/TP; bisa diupdate kalau nanti ada refinement dari data/experience baru.