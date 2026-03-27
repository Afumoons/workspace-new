# Cron Task Templates

Tiga template ini dipakai saat Afu memberi tugas yang besar/kompleks dan lebih tepat dikerjakan dengan pendekatan cron-driven, bertahap, dan tahan context loss.

---

## 1) TEMPLATE: RISET BESAR

### Kapan dipakai
Gunakan template ini jika task mencakup:
- riset banyak sumber
- komparasi opsi
- analisis bertahap
- pemantauan topik / market / kompetitor / teknologi
- penyusunan synthesis/report yang tidak realistis selesai dalam satu prompt

### Struktur intake
- **Nama task:**
- **Pertanyaan inti yang harus dijawab:**
- **Output akhir yang diinginkan:**
- **Batasan sumber / domain:**
- **Tingkat kedalaman:** quick / standard / deep
- **Risiko bias / hal yang harus dihindari:**
- **Deadline / cadence:**
- **Apa yang harus dipastikan dengan Afu sebelum lanjut:**

### Pola eksekusi
1. Definisikan pertanyaan riset dan scope.
2. Pecah jadi sub-pertanyaan.
3. Tentukan file kerja/checkpoint.
4. Jalankan cron untuk mengerjakan bagian-bagian riset secara bertahap.
5. Setiap putaran, update synthesis ringkas.
6. Setelah cukup bukti, buat conclusion + recommendation.

### File yang disarankan
- `tmp/research/<slug>/plan.md`
- `tmp/research/<slug>/sources.md`
- `tmp/research/<slug>/notes.md`
- `tmp/research/<slug>/synthesis.md`
- `tmp/research/<slug>/questions-open.md`

### Template prompt cron
"Continue the research task for Afu. First read the current research plan, source notes, synthesis, and open questions for this topic. Execute only the next highest-value research step. Add concrete evidence, update synthesis, and keep claims tied to sources. If the answer quality is still weak, refine the open questions instead of forcing conclusions. End with: what was learned, confidence level, and exact next research step."

### Template update ke Afu
- **Topik:** <nama topik>
- **Progress:** <berapa jauh>
- **Temuan penting:**
  - ...
  - ...
- **Yang belum jelas:**
  - ...
- **Next step:** ...
- **Confidence:** low / medium / high

### Kondisi selesai
Selesai jika:
- pertanyaan inti sudah terjawab cukup baik
- evidence cukup untuk rekomendasi
- uncertainty yang tersisa sudah dijelaskan jelas
- hasil akhir bisa dipakai untuk keputusan nyata

---

## 2) TEMPLATE: PROYEK CODING BESAR

### Kapan dipakai
Gunakan template ini jika task mencakup:
- build feature besar
- refactor multi-file
- sistem baru / modul baru
- debugging kompleks lintas komponen
- migrasi, redesign, atau integrasi yang tidak masuk akal dikerjakan one-shot

### Struktur intake
- **Nama proyek/task:**
- **Tujuan bisnis/fungsional:**
- **Definition of done:**
- **Repo/path yang relevan:**
- **Constraint teknis:**
- **Risiko regresi:**
- **Apa yang boleh diubah / tidak boleh diubah:**
- **Test strategy:**
- **Approval points yang mungkin dibutuhkan:**

### Pola eksekusi
1. Audit codebase/area kerja.
2. Tulis plan milestone.
3. Buat checkpoint file + working notes.
4. Eksekusi per milestone via cron/job bertahap.
5. Setelah tiap milestone: test, catat hasil, koreksi.
6. Akhiri dengan ringkasan perubahan, dampak, dan next actions.

### File yang disarankan
- `tmp/build/<slug>/plan.md`
- `tmp/build/<slug>/architecture-notes.md`
- `tmp/build/<slug>/todo.md`
- `tmp/build/<slug>/progress-log.md`
- `tmp/build/<slug>/test-log.md`
- `tmp/build/<slug>/handoff.md`

### Template prompt cron
"Continue the coding task for Afu. First read the task plan, current progress log, todo list, and latest test log. Work only on the next milestone that gives the highest leverage with the lowest avoidable risk. Make changes incrementally, verify them, and record what changed plus any regressions or uncertainties. If blocked by ambiguity, stop cleanly and write the smallest decision Afu needs to make. End with: files changed, tests run, result, and exact next step."

### Template update ke Afu
- **Task:** <nama task>
- **Milestone sekarang:** <milestone>
- **Progress:**
  - selesai: ...
  - sedang jalan: ...
- **File/area terdampak:** ...
- **Test status:** pass / partial / blocked
- **Risk note:** ...
- **Next step:** ...

### Kondisi selesai
Selesai jika:
- definition of done terpenuhi
- perubahan utama sudah diuji semampunya
- blocker/risk residual terdokumentasi
- ada handoff ringkas yang usable

---

## 3) TEMPLATE: MONITORING / AUTOMATION BERULANG

### Kapan dipakai
Gunakan template ini jika task mencakup:
- pemantauan harga / market / news / signal
- pengecekan sistem berkala
- pengumpulan data periodik
- watchlist, alerting, atau recurring review
- automation loop yang memang harus hidup terus

### Struktur intake
- **Nama monitor/automation:**
- **Apa yang dipantau / dijalankan:**
- **Tujuan operasional:**
- **Frekuensi ideal:**
- **Threshold / trigger penting:**
- **Apa yang dianggap noise:**
- **Aksi saat trigger:**
- **Apa yang butuh approval dulu:**
- **Format laporan/alert:**

### Pola eksekusi
1. Tentukan sinyal vs noise.
2. Tentukan cadence cron yang efisien.
3. Simpan state terakhir agar tidak spam.
4. Saat cron jalan, hanya kirim update jika ada perubahan penting.
5. Review threshold secara berkala jika terlalu sensitif / terlalu longgar.

### File yang disarankan
- `tmp/monitor/<slug>/config.md`
- `tmp/monitor/<slug>/state.json`
- `tmp/monitor/<slug>/events.md`
- `tmp/monitor/<slug>/summary.md`
- `tmp/monitor/<slug>/thresholds.md`

### Template prompt cron
"Run the recurring monitoring task for Afu. First read the current config, prior state, thresholds, and recent events. Check only the defined signals, compare against prior state, and avoid noisy reporting. If nothing materially changed, stay quiet or log internally depending on the task design. If a threshold is hit, produce a concise alert with the exact trigger, why it matters, confidence, and the recommended next action. Update state before finishing."

### Template update ke Afu
- **Monitor:** <nama monitor>
- **Status:** normal / alert / review-needed
- **Trigger:** ...
- **Apa yang berubah:** ...
- **Kenapa ini penting:** ...
- **Aksi yang disarankan:** ...
- **Urgensi:** low / medium / high

### Kondisi sehat
Loop dianggap sehat jika:
- tidak spam
- state tersimpan rapi
- alert hanya muncul saat ada perubahan yang meaningful
- threshold dapat dijelaskan secara operasional

---

## Rule of Thumb Pemilihan Template
- Kalau fokusnya **mencari jawaban/insight** → pakai **Riset Besar**
- Kalau fokusnya **membangun/memperbaiki sistem atau code** → pakai **Proyek Coding Besar**
- Kalau fokusnya **memantau sesuatu secara terus-menerus** → pakai **Monitoring/Automation Berulang**

## Default Decision Rule
Jika sebuah task besar punya kombinasi beberapa tipe:
- mulai dari template dominan
- lalu gabungkan elemen template lain seperlunya
- contoh:
  - research + monitor → mulai dari riset, lanjut monitor
  - coding + monitor → build dulu, lalu pasang monitor
  - research + coding → riset decision layer dulu, lalu eksekusi build layer
