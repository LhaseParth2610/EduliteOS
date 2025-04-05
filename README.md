# EduOS - Lightweight Linux for Education 📚🖥️

EduOS is a fast, Debian-based Linux distribution designed for **low-end hardware (≤1GB RAM)**, with a focus on **offline learning**, **teacher-friendly tools**, and **performance**.

---

## ✨ Features

- 🧠 Preinstalled Python learning apps (Thonny, Math Quiz)
- 🌐 Offline Wikipedia & Khan Academy via Kiwix
- 🧑‍🏫 Teacher Dashboard for student monitoring
- 🚀 Ultra-low RAM usage (~220MB idle)
- 💾 One-click USB deployment
- 🧊 ZRAM-based memory compression

---

## 📦 System Requirements

- RAM: **512MB minimum**, 1GB recommended  
- CPU: Any x86_64 processor (Pentium 4 and above)  
- Storage: **8GB** minimum (32GB recommended for offline content)

---

## 🔧 Installation

### For Schools (USB Method)
```bash
sudo dd if=eduos.iso of=/dev/sdX bs=4M status=progress
