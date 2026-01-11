# LinkedIn Bot Poster - macOS Setup Guide

## 🚀 Quick Start

### 1️⃣ Create virtual environment

```bash
cd /path/to/linkedinposter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 2️⃣ Configure `.env` file

Create a `.env` file in the same directory:

```bash
cat > .env << 'EOF'
PERPLEXITY_API_KEY=your_perplexity_key_here
LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here
LINKEDIN_PERSON_URN=urn:li:person:xxxxxxxxxxxxx
PIXABAY_API_KEY=your_pixabay_key_here
EOF
```

**Get your tokens:**
- **Perplexity API**: https://www.perplexity.ai/api
- **LinkedIn Access Token**: https://www.linkedin.com/developers/apps
- **Pixabay API**: https://pixabay.com/api/docs/
- **LinkedIn Person URN**: 
  - Go to linkedin.com/me
  - Open DevTools → Network tab
  - Look for API calls with `"id":"urn:li:person:XXXXX"`

### 3️⃣ Test it from Terminal

```bash
zsh linkedinposter.sh now
```

---

## 📱 macOS Shortcut Integration (IMPORTANT)

### ✅ Correct Setup for Shortcuts.app

1. **Open Shortcuts.app**
2. **Create new Shortcut**
3. **Add action: "Run Shell Script"**
4. **Change Shell to: `zsh`** ⚠️ This is important!
5. **Paste full path:**
```bash
zsh /Users/toni/Documents/GitHub/Personal/linkedinposter/linkedinposter.sh now
```

**Replace `/Users/toni/...` with your actual path. Get it by running:**
```bash
pwd
```
in the linkedinposter directory.

6. **Test the Shortcut by clicking ▶️**

---

## 🛠️ Commands

```bash
# Publish a post immediately
zsh linkedinposter.sh now

# Run daemon (publishes every 3.5 days at 10:00)
zsh linkedinposter.sh daemon

# Show help
zsh linkedinposter.sh help
```

---

## 🐛 Troubleshooting

### Error: "permission denied"
**Solution:** You're probably in the Shortcuts.app. Make sure to:
1. Change Shell to `zsh` in the "Run Shell Script" action
2. Use the full absolute path: `/Users/toni/...`
3. Don't use `./linkedinposter.sh` - use `zsh /full/path/linkedinposter.sh now`

### Virtual environment not found
```bash
cd /path/to/linkedinposter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### `.env` file not found
```bash
cat > .env << 'EOF'
PERPLEXITY_API_KEY=xxx
LINKEDIN_ACCESS_TOKEN=xxx
LINKEDIN_PERSON_URN=urn:li:person:xxx
PIXABAY_API_KEY=xxx
EOF
```

### Script not running from Shortcut
1. ✅ Verify Shell is set to `zsh` (not bash)
2. ✅ Use absolute path: `/Users/toni/Documents/GitHub/Personal/linkedinposter/linkedinposter.sh`
3. ✅ Test in Terminal first: `zsh linkedinposter.sh now`
4. ✅ Check `.env` file exists and has all API keys

### "main.py not found" error
Make sure `main.py` is in the same directory as `linkedinposter.sh`:
```bash
ls -la
# Should show:
# main.py
# linkedinposter.sh
# requirements.txt
# .env
# venv/
```

---

## 📊 File Structure

```
linkedinposter/
├── main.py                 # Main bot script
├── linkedinposter.sh       # macOS runner (NO need to chmod)
├── requirements.txt        # Python dependencies
├── .env                    # API keys (don't commit!)
├── venv/                   # Virtual environment
└── SETUP.md               # This file
```

---

## 🔒 Security Notes

⚠️ **Never commit `.env` to Git:**

```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

---

## 📱 macOS Automation (Advanced)

If you want automatic daily posts (not just from Shortcut):

1. Open **Automator.app**
2. Create new **Calendar Alarm**
3. Set time: **10:00 AM**
4. Add action: **Run Shell Script**
5. Paste:
```bash
zsh /full/path/to/linkedinposter.sh now
```

---

## 📈 Quick Checklist

✅ Virtual environment created (`venv/` folder exists)
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ `.env` file created with all API keys
✅ Tested in Terminal: `zsh linkedinposter.sh now`
✅ Shortcut.app configured with `zsh` shell
✅ Shortcut uses full absolute path
✅ Shortcut tested and working

---

**Questions?** Check the terminal output for detailed logs about post generation, image search, and publishing.
