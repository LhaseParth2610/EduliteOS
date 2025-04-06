
# 🐧 EduLite OS

**EduLite OS** is a lightweight, Debian-based Linux operating system tailored for educational use, especially on **low-end hardware (≤1GB RAM)**. It comes pre-installed with essential offline learning tools, teacher dashboards, and Python educational apps — all optimized for speed and simplicity.

---

## ✨ Features

- 🚀 **Runs on Low-End PCs** (≤2GB RAM)
- 🎓 **Offline Learning Tools** (No internet required)
- 🐍 **Custom Python Apps** for interactive learning
- 💡 **Simple, Colorful UI** using LXQt
- ⚡ **Optimized with ZRAM** and minimal services

---

## 🛠️ Tech Stack

| Component           | Details                             |
|--------------------|--------------------------------------|
| Base OS            | Debian                              |
| Desktop Environment| LXQt                                 |
| Package Manager    | `apt`                                |
| Performance Boost  | ZRAM, systemd tweaks                 |
| Offline Tools      |Custom Python,educational apps,Kolibri|

---

## 📂 Directory Structure

```bash
/usr/local/share/edu_apps/          # Python apps and dashboards  
/usr/local/bin/myapps/              # Launcher symlinks (added to PATH)  
/usr/share/applications/edu-os/     # Custom .desktop files  
```

---
---

## 💾 Installation Steps

1. 🔗 **Download ISO from the Official Website**  
   Visit: [https://edulite-os.github.io](https://edulite-os.github.io)

2. 💿 **Create Bootable USB**  
   Use tools like **Rufus (Windows)** or **balenaEtcher (Linux/Mac)** to flash the ISO to a USB drive.

3. 💻 **Boot & Install EduLite OS**  
   - Insert the USB stick into the system  
   - Boot from USB via BIOS/UEFI  
   - Follow the simple installation wizard  

4. ✅ You're ready to learn!

---


---

## 📸 Screenshots

> _Coming soon..._

---

## 📈 Roadmap

- [x] Offline Learning Modules  
- [x] Teacher Control Panel  
- [x] Low RAM Optimization
- [x] Exam Mode 
- [ ] Voice Interface *(future scope)*  
- [ ] AI Chatbot *(future scope)*

---

## 🤝 Contributing

We welcome PRs! Please follow the contribution guidelines in `CONTRIBUTING.md`.

---

## 📜 License

EduLite OS is released under the **MIT License**. See `LICENSE` file for details.

---

## ❤️ Special Thanks

To the open-source Linux and education community for their support and inspiration.

EOF
