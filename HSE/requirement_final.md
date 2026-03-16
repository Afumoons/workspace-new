# HSE / K3 Mobile System – Functional Requirements & Price Estimate

## 1. Project Overview

Perusahaan ingin membangun **sistem HSE / K3 berbasis mobile** yang dapat
mendukung aktivitas Health, Safety & Environment secara terintegrasi:

- Dokumentasi dan otorisasi pekerjaan berisiko.
- Manajemen SOP dan sistem manajemen terintegrasi.
- Pelaporan insiden, bahaya, dan aktivitas berisiko tinggi.
- Analitik dan dashboard untuk tracking KPI HSE.
- LMS internal untuk pelatihan HSE.
- Gamifikasi dan sistem membership (My Card) untuk meningkatkan engagement.

Aplikasi dapat dikembangkan dalam dua bentuk:

1. **PWA (Progressive Web App)** yang diakses via browser mobile namun dapat
   di-install seperti aplikasi.
2. **Aplikasi mobile native/hybrid** dengan output **APK** (Android),
   memungkinkan akses fitur yang lebih dalam terhadap perangkat.

Dokumen ini merangkum requirement fungsional utama dan memberikan estimasi
biaya pengembangan untuk masing-masing pendekatan (PWA vs Mobile App).

---

## 2. User Roles & Authentication

### 2.1. Role & Login

- **User Organization** (internal perusahaan):
  - Login menggunakan akun terdaftar (email/username + password) atau SSO
    (opsional, tergantung integrasi).
  - Akses modul sesuai hak akses (role-based access control / membership tier).

- **User Public** (peserta pelatihan publik / eksternal):
  - Login via **Google OAuth** (Sign in with Google).
  - Akses modul terbatas (misalnya LMS publik, beberapa materi edukasi,
    atau blog/artikel).

### 2.2. RBAC & Membership (My Card)

- Sistem **role-based access control (RBAC)** dengan lapisan gamifikasi
  membership, contohnya: `Basic → Standard → Advance → Expert`.
- Halaman **"My Card"** berfungsi sebagai **Digital Membership Card**:
  - Field contoh:
    - Nama
    - ID Member
    - Membership Tier (mis. Advance)
    - Valid Thru
    - QR Code (untuk verifikasi identitas & hak akses)
  - Membership tier memengaruhi fitur mana yang **unlocked** (misalnya
    modul Permit to Work, SOP, IMS, Incident Report, dsb.).

---

## 3. Modul Utama & Fitur

### 3.1. Blog / Artikel

- User (admin/editor) dapat membuat, mengedit, dan mempublikasikan artikel
  terkait K3 / HSE.
- User publik dan internal dapat membaca artikel yang dipublikasikan.
- Kategori/tag artikel, pencarian basic.

### 3.2. Sistem Notifikasi

- Notifikasi in-app + (opsional) push notification ketika:
  - Arsip kerja / dokumen baru ditambahkan.
  - SOP baru atau update SOP.
  - Ada laporan insiden / hazard yang membutuhkan tindakan.
  - Assignment baru masuk ke user ("Assign to Me").
- Notifikasi dikelola dengan kategori (operasional, training, reminder, dsb.).

### 3.3. Permit to Work

- Formulir digital untuk **izin kerja berisiko tinggi**:
  - Lokasi pekerjaan.
  - Jenis pekerjaan & kategori risiko.
  - Tim/individu yang terlibat.
  - Waktu mulai & selesai.
  - Checklist persyaratan (APD, izin khusus, isolasi energi, dsb.).
- Alur approval ("Assign to Me"):
  - Status: Draft → Submitted → Need Approval → Approved / Rejected.
  - Daftar tugas yang perlu di-approve oleh role tertentu.
- Fitur:
  - **Report**: daftar semua Permit to Work, filter by status, tanggal, zona, dsb.
  - **Tracking analysis**:
    - Bar chart statistik zona.
    - Total zona.
    - Total kategori pekerjaan.
    - Donut chart status (Approved/Rejected/On Progress).
  - **Download template / export** (PDF/Excel) untuk arsip.

### 3.4. Manage SOP (Standard Operating Procedure)

- Modul manajemen SOP berbasis digital:
  - CRUD dokumen SOP (judul, deskripsi, versi, status aktif/non-aktif).
  - Upload lampiran (PDF, gambar, dsb.).
- Fitur tambahan:
  - **Report**: daftar SOP, filter per area, status, versi.
  - **Tracking analysis**: jumlah SOP per kategori/zona, compliance level.
  - **Assign to Me**: SOP yang butuh review/approval.
  - **Download template**: format baku pembuatan SOP.

### 3.5. Integrated Management System (IMS)

- Sistem manajemen terintegrasi untuk dokumentasi standar, gap analysis,
  dan evidence digital terhadap klausa/standar tertentu.
- Fitur:
  - Penyimpanan dokumen kompliance per klausa/standar.
  - Form gap analysis (current vs required).
  - Upload digital evidence file compliant dengan standar.
  - **Report**, **tracking analysis**, **assign to me**, **download template**
    dengan pola serupa modul SOP.

### 3.6. High Risk Activity

- Modul untuk mencatat dan mengelola aktivitas berisiko tinggi:
  - Daftar aktivitas high-risk, langkah kerja, dan kontrol administratif.
- Fitur:
  - **Report** aktivitas.
  - **Tracking analysis** jumlah dan status mitigasi.
  - **Assign to Me** untuk PIC yang bertanggung jawab.
  - **Download template** HRA.

### 3.7. Incident Report

- Sistem pelaporan insiden real-time berbasis online.
- Tahapan laporan:
  - Preliminary report (laporan awal cepat).
  - Full incident report (detail kronologi, investigasi, tindakan korektif).
- Integrasi:
  - **Google Maps**: pilih / tandai lokasi insiden.
  - Upload foto insiden.
- Fitur:
  - **Report** insiden dengan filter tanggal, jenis, lokasi, severity.
  - **Tracking analysis**: tren insiden, kategori, zona.
  - **Assign to Me** untuk tim investigasi / HSE officer.
  - **Download template** form incident.

### 3.8. JSEA (Job Safety & Environmental Analysis)

- Modul untuk analisis langkah kerja dan risiko lingkungan.
- Fitur standar:
  - Form JSEA: tahapan kerja, hazard, risiko, kontrol.
  - **Report**, **tracking analysis**, **assign to me**, **download template**.

### 3.9. Hazard Report

- Modul untuk pelaporan hazard potensial di lapangan.
- Fitur:
  - Form pelaporan hazard (lokasi, deskripsi, foto, kategori).
  - **Report**, **tracking analysis**, **assign to me**, **download template**.

### 3.10. Inspection Report

- Modul untuk report hasil inspeksi area kerja.
- Fitur:
  - Form inspeksi (checklist, temuan, rekomendasi).
  - **Report**, **tracking analysis**, **assign to me**, **download template**.

### 3.11. Health Record

- Rekam kesehatan karyawan (opsional, tergantung regulasi internal dan
  compliance privasi).
- Fitur dasar:
  - Ringkasan check-up, hasil screening, catatan medical (model agregat,
    bukan EMR penuh).

### 3.12. Zona / Dashboard Zona

- Halaman "Zona" sebagai entry point ke modul-modul HSE:
  - Kartu-kartu modul (Permit to Work, SOP, IMS, High Risk Activity,
    Incident Report, JSEA, Hazard Report, Inspection Report, Health Record).
  - Masing-masing menampilkan jumlah data (misal 3.493 records) dan status.

### 3.13. LMS (Learning Management System)

- Statistik utama:
  - Enrolled, Ongoing, Finished.
- Fitur:
  - **All Courses**: katalog course dengan kategori (Fundamental, Management),
    durasi, jumlah modul, jumlah peserta, tombol Enroll.
  - **My Course**: course yang diikuti user, status progress.
  - **Scheduled Courses**: jadwal kelas/live session.
  - **Hot Courses**: course terpopuler berdasarkan jumlah user.
- Fungsionalitas:
  - Enrollment system.
  - Tracking progress (Enrolled → Ongoing → Finished).
  - Dukungan course on-demand; support kelas terjadwal bisa ditambah.

---

## 4. Non-Functional Requirements (Ringkas)

- **Keamanan**:
  - Secure coding (OWASP best practice).
  - Proteksi endpoint API dengan JWT/role-based access.
- **Performa**:
  - Responsive dan cepat diakses di jaringan mobile.
  - Query database dioptimalkan (indexing, pagination).
- **Scalability**:
  - Desain modular: modul-modul HSE bisa dikembangkan bertahap.
- **Audit trail**:
  - Pencatatan aktivitas penting (create/update/delete, approval, dsb.).

---

## 5. Estimasi Biaya Pengembangan

> Catatan: Angka di bawah ini adalah estimasi kasar untuk membantu budgeting.
> Nilai aktual dapat disesuaikan dengan detail teknis final, jumlah integrasi,
> dan tingkat polishing UI/UX yang diinginkan.

### 5.1. Estimasi Biaya – PWA (Progressive Web App)

PWA memanfaatkan stack web (Laravel/Node + front-end modern) dan di-deploy
sebagai aplikasi web yang dapat di-install di browser mobile.

**Estimasi kisaran biaya pengembangan PWA:**

- Kisaran: **Rp 70.000.000 – 100.000.000**

**Per modul (kisaran, all-in termasuk integrasi & basic UI):**

- Core & Auth (login 2 tipe, Google login, RBAC, My Card):
  - ± **Rp 15.000.000 – 20.000.000**
- Blog & Notifikasi:
  - ± **Rp 7.000.000 – 10.000.000**
- Permit to Work (form, workflow approval, reporting, analytics):
  - ± **Rp 12.000.000 – 18.000.000**
- Manage SOP:
  - ± **Rp 8.000.000 – 12.000.000**
- IMS (Integrated Management System):
  - ± **Rp 10.000.000 – 15.000.000**
- High Risk Activity:
  - ± **Rp 8.000.000 – 12.000.000**
- Incident Report (termasuk integrasi Google Maps & upload foto):
  - ± **Rp 12.000.000 – 18.000.000**
- JSEA:
  - ± **Rp 8.000.000 – 12.000.000**
- Hazard Report:
  - ± **Rp 7.000.000 – 10.000.000**
- Inspection Report & Health Record (basic):
  - ± **Rp 10.000.000 – 15.000.000**
- LMS (catalog, enrollment, progress tracking, hot courses):
  - ± **Rp 15.000.000 – 20.000.000**

Total jika semua modul diambil dalam 1 paket PWA biasanya akan dinegosiasikan
sebagai **project bundle** agar lebih efisien (bukan penjumlahan kaku per modul).

### 5.2. Estimasi Biaya – Mobile App (APK Android)

Aplikasi mobile (misalnya Flutter/React Native) akan memberikan pengalaman yang
lebih native dan potensi akses lebih dalam ke fitur perangkat, dengan biaya
pengembangan dan testing yang sedikit lebih tinggi.

**Estimasi kisaran biaya pengembangan mobile app (APK Android):**

- Kisaran: **Rp 90.000.000 – 130.000.000**

**Per modul (kisaran, di luar backend/API jika backend dihitung terpisah):**

- Core & Auth (login 2 tipe, Google login, RBAC, My Card UI):
  - ± **Rp 20.000.000 – 25.000.000**
- Blog & Notifikasi (in-app + push notif):
  - ± **Rp 10.000.000 – 15.000.000**
- Permit to Work (UI form, workflow, status):
  - ± **Rp 15.000.000 – 20.000.000**
- Manage SOP (list, detail, download/view dokumen):
  - ± **Rp 10.000.000 – 15.000.000**
- IMS:
  - ± **Rp 12.000.000 – 18.000.000**
- High Risk Activity:
  - ± **Rp 10.000.000 – 15.000.000**
- Incident Report (maps + foto via kamera/gallery):
  - ± **Rp 18.000.000 – 25.000.000**
- JSEA:
  - ± **Rp 10.000.000 – 15.000.000**
- Hazard Report:
  - ± **Rp 9.000.000 – 13.000.000**
- Inspection Report & Health Record:
  - ± **Rp 12.000.000 – 18.000.000**
- LMS mobile (course list, enrollment, progress, hot courses):
  - ± **Rp 18.000.000 – 25.000.000**

Sama seperti PWA, pada praktiknya modul-modul ini akan dikemas sebagai paket
proyek dengan harga bundle agar lebih kompetitif.

---

## 6. Catatan Tambahan

- Estimasi belum termasuk:
  - Biaya infrastruktur (server/hosting, domain, SSL, cloud services).
  - Biaya lisensi pihak ketiga (misalnya layanan Digital Signature seperti Privy,
    jika nanti ingin diintegrasikan juga di sistem ini).
  - Integrasi dengan sistem perusahaan lain (ERP, HRIS, dsb.).
- Estimasi dapat disesuaikan setelah:
  - Diskusi detail flow per modul.
  - Keputusan final mengenai level polishing UI/UX, animasi, dan branding.

Dokumen ini dapat digunakan sebagai **draft professional requirement** dan
basis diskusi awal harga dengan klien, baik untuk opsi PWA maupun aplikasi
mobile (APK Android).
