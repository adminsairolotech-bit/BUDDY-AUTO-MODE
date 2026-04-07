# 🤖 BUDDY AI - ChatGPT & Codex Browser Automation

## Ye Kya Karta Hai?

Ye agent automatically ChatGPT aur Codex ke beech kaam karta hai:

1. ✅ **Auto-Approve**: "Yes", "Run", "Continue" buttons automatically click karta hai
2. 🔄 **Code Sync**: Codex se code uthata hai aur ChatGPT pe review ke liye bhejta hai
3. 💬 **Response Copy**: ChatGPT ka response automatically clipboard pe copy karta hai
4. 🖥️ **Desktop Support**: ChatGPT Desktop app bhi support karta hai

---

## 🚀 Installation (Windows)

### Step 1: Python Install Karo
```
Download: https://www.python.org/downloads/
✅ "Add Python to PATH" check karo installation mein
```

### Step 2: Dependencies Install Karo
```bash
cd desktop_agent
pip install -r requirements.txt
```

### Step 3: Chrome Driver Install Karo (Agar Chrome use karte ho)
```bash
pip install webdriver-manager
```
Ya manually download: https://chromedriver.chromium.org/downloads

### Step 4 (Optional): Tesseract OCR Install Karo (Better button detection ke liye)
```
Download: https://github.com/UB-Mannheim/tesseract/wiki
Install karo aur path set karo
```

---

## 🎮 Kaise Use Kare?

### Browser Automation:
```bash
python chatgpt_codex_automation.py
```

1. Option 1 select karo (Browser Automation)
2. Browser choose karo (chrome/edge/opera)
3. Automation start ho jayega!

### Desktop App Automation:
```bash
python chatgpt_codex_automation.py
```

1. Option 2 select karo (Desktop App)
2. ChatGPT Desktop app open karo
3. Automation start ho jayega!

---

## ⚙️ Configuration

`chatgpt_codex_automation.py` mein ye settings change kar sakte ho:

```python
self.config = {
    "check_interval": 2,        # Kitne seconds mein check kare
    "auto_approve": True,       # Auto-approve on/off
    "copy_code_to_chatgpt": True,  # Code sync on/off
    "monitor_codex": True,      # Codex monitor on/off
}

# Approval keywords (ye buttons auto-click honge)
self.approval_keywords = ["yes", "run", "continue", "approve", "confirm", "execute", "ok"]
```

---

## 🔧 Troubleshooting

### Browser nahi khul raha?
- Chrome/Edge latest version install karo
- webdriver-manager install karo: `pip install webdriver-manager`

### Buttons detect nahi ho rahe?
- Tesseract OCR install karo
- Screen zoom 100% pe rakho
- Window maximize rakho

### Login required hai?
- Pehle manually login kar lo
- Browser profile save hoga

---

## 🛡️ Safety Notes

- Ye agent aapke browser/desktop ko control karta hai
- Sirf trusted websites pe use karo
- Sensitive data pe use mat karo
- Ctrl+C se kisi bhi waqt stop kar sakte ho

---

## 📞 Support

Issues? BUDDY AI dashboard pe report karo ya GitHub pe issue create karo.

**Happy Automating! 🚀**
