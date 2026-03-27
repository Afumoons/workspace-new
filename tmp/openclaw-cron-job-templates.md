# OpenClaw Cron Job Templates (Ready-to-Use)

Template ini adalah versi siap-pakai untuk job `cron.add` OpenClaw ketika Afu memberi task besar/kompleks yang lebih cocok dikerjakan secara bertahap.

Prinsip default:
- gunakan `payload.kind: "agentTurn"`
- gunakan `sessionTarget: "isolated"`
- gunakan `delivery.mode: "announce"` kecuali memang harus diam
- checkpoint/progress tetap disimpan di file workspace
- jangan pakai job otomatis untuk aksi destruktif, live trading, publish, pembayaran, atau third-party action tanpa approval eksplisit

---

## 1) TEMPLATE JOB: RISET BESAR

### Kapan dipakai
- market research
- competitor research
- technology deep dive
- due diligence
- ongoing thesis building

### Job skeleton
```json
{
  "name": "Large Research - <topic>",
  "schedule": {
    "kind": "every",
    "everyMs": 3600000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Continue the research task for Afu. First read the current research files in tmp/research/<slug>/ including plan.md, sources.md, notes.md, synthesis.md, and questions-open.md. Execute only the next highest-value research step. Update the files before finishing. If blocked, write the blocker and the exact decision needed. Then produce a concise milestone update for Afu.",
    "thinking": "medium",
    "timeoutSeconds": 900
  },
  "delivery": {
    "mode": "announce"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Recommended folders/files
- `tmp/research/<slug>/plan.md`
- `tmp/research/<slug>/sources.md`
- `tmp/research/<slug>/notes.md`
- `tmp/research/<slug>/synthesis.md`
- `tmp/research/<slug>/questions-open.md`

### Good cadence
- fast-moving topic: every 30–60 min
- standard deep research: every 2–4 h
- long-horizon thesis: 1–2x per day

### Example use
- “Pantau dan bangun thesis AI agent economy sampai jadi memo keputusan.”
- “Riset mendalam peluang bisnis yang bisa dibangun dari skill dan infra yang kita punya.”

---

## 2) TEMPLATE JOB: PROYEK CODING BESAR

### Kapan dipakai
- build feature besar
- multi-step bugfix
- refactor lintas file
- scaffolding modul/sistem
- migrasi bertahap

### Job skeleton
```json
{
  "name": "Large Build - <project-or-feature>",
  "schedule": {
    "kind": "every",
    "everyMs": 5400000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Continue the coding task for Afu. First read tmp/build/<slug>/plan.md, todo.md, progress-log.md, test-log.md, and handoff.md if present. Work only on the next milestone with the highest leverage and lowest avoidable risk. Make incremental changes, verify them, update the logs/checkpoints, and end with a concise progress update including files changed, tests run, result, blockers, and exact next step.",
    "thinking": "medium",
    "timeoutSeconds": 1200
  },
  "delivery": {
    "mode": "announce"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Recommended folders/files
- `tmp/build/<slug>/plan.md`
- `tmp/build/<slug>/architecture-notes.md`
- `tmp/build/<slug>/todo.md`
- `tmp/build/<slug>/progress-log.md`
- `tmp/build/<slug>/test-log.md`
- `tmp/build/<slug>/handoff.md`

### Good cadence
- active implementation burst: every 60–90 min
- heavier tasks with validation: every 2–3 h
- maintenance/refactor loop: 1–2x per day

### Example use
- “Bangun dashboard baru bertahap sampai usable.”
- “Refactor modul order management tanpa merusak flow existing.”

---

## 3) TEMPLATE JOB: MONITORING / AUTOMATION BERULANG

### Kapan dipakai
- market monitoring
- system health monitoring
- recurring checks
- watchlist / alerting
- signal loop / review loop

### Job skeleton
```json
{
  "name": "Monitoring - <topic>",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run the recurring monitoring task for Afu. First read tmp/monitor/<slug>/config.md, thresholds.md, state.json, events.md, and summary.md if present. Check only the defined signals, compare them with prior state, avoid noisy reporting, and update state before finishing. If there is no meaningful change, either stay quiet or write an internal checkpoint depending on task design. If a threshold is hit, produce a concise alert with the trigger, why it matters, confidence, urgency, and recommended next action.",
    "thinking": "low",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "announce"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Recommended folders/files
- `tmp/monitor/<slug>/config.md`
- `tmp/monitor/<slug>/thresholds.md`
- `tmp/monitor/<slug>/state.json`
- `tmp/monitor/<slug>/events.md`
- `tmp/monitor/<slug>/summary.md`

### Good cadence
- high-sensitivity monitoring: 15–30 min
- normal monitoring: 1–4 h
- low-priority recurring review: daily

### Example use
- “Pantau pasangan market tertentu dan kabari hanya kalau ada perubahan penting.”
- “Cek health proyek/infra secara periodik dan ringkas kalau ada issue.”

---

## 4) TEMPLATE JOB: SATU KALI BESAR (ONE-SHOT FOLLOW-THROUGH)

Gunakan ini kalau task besar tidak perlu looping permanen, tapi terlalu besar untuk satu turn dan lebih baik dijalankan dalam job terisolasi yang bisa fokus penuh.

### Job skeleton
```json
{
  "name": "One-Shot Large Task - <task-name>",
  "schedule": {
    "kind": "at",
    "at": "2026-03-27T10:30:00+07:00"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Execute the large task for Afu using the existing plan/checkpoint files. First read the relevant tmp working files. Complete the highest-priority phase you can safely finish in this run. Update progress logs before ending. If fully done, provide a concise completion handoff. If partially done, provide a milestone update and exact next step.",
    "thinking": "medium",
    "timeoutSeconds": 1800
  },
  "delivery": {
    "mode": "announce"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

### Kapan dipakai
- task besar tapi finite
- deep work batch
- scheduled follow-through nanti malam/pagi
- execution burst yang tidak perlu recurring forever

---

## 5) TEMPLATE JOB: REMINDER / CHECKPOINT DECISION

Gunakan ini untuk minta keputusan Afu di waktu tertentu setelah task besar berjalan.

### Job skeleton (systemEvent)
```json
{
  "name": "Decision Reminder - <task-name>",
  "schedule": {
    "kind": "at",
    "at": "2026-03-27T18:00:00+07:00"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "Reminder: this is a checkpoint for the large task '<task-name>'. We reached a decision point and need your input on: <decision-needed>. Review the latest progress summary/checkpoint files and choose the next direction."
  },
  "delivery": {
    "mode": "none"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

### Kapan dipakai
- decision gate
- approval gate
- remind review at a specific hour
- force a re-sync with Afu after autonomous progress

---

## Practical Build Pattern
Untuk task besar, default pola implementasi yang sebaiknya dipakai:

1. Buat folder kerja di `tmp/`
2. Tulis `plan.md`
3. Tulis `todo.md` / `questions-open.md` / `thresholds.md` sesuai tipe task
4. Tambahkan cron job dari template yang cocok
5. Biarkan job jalan bertahap
6. Review hasil dan ubah cadence bila terlalu lambat / terlalu noisy
7. Hapus/disable job saat objective selesai

---

## Fast Fill Variables
Sebelum `cron.add`, isi variabel ini:
- `<slug>` = nama folder kerja singkat, mis. `ai-agent-research`
- `<topic>` = topik riset/monitor
- `<project-or-feature>` = nama proyek atau fitur
- `<task-name>` = nama task untuk one-shot/reminder
- `<decision-needed>` = keputusan spesifik yang dibutuhkan dari Afu

---

## Rule of Thumb: Schedule Choice
- `every 15–30 min` → hanya untuk monitoring sensitif
- `every 60–180 min` → default terbaik untuk banyak task besar
- `daily` → untuk review yang tidak urgent
- `at <timestamp>` → untuk one-shot burst atau reminder tepat waktu

---

## Rule of Thumb: Delivery Choice
- `announce` → default, kalau Afu memang ingin update progres
- `none` → kalau job hanya internal/checkpoint dan tidak perlu notifikasi chat
- `webhook` → hanya kalau memang diminta integrasi sistem eksternal

---

## Rule of Thumb: Session Target
- `isolated` → default terbaik untuk task besar otomatis
- `current` → hanya kalau wajib lanjut di thread/sesi yang sama
- `main` + `systemEvent` → untuk reminder/checkpoint yang memang harus muncul sebagai pengingat utama
