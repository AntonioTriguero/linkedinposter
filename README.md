# 🚀 LinkedIn Bot Poster - Antonio Triguero

**Automated AI-powered LinkedIn posting bot that generates executive-level content with contextually relevant images.**

> Posts every 3.5 days at 10:00 AM or on-demand. Executive-level insights. Zero grammar/spelling errors. Perfectly matched images.

---

## ✨ Features

### 📝 Content Generation
- **Executive-level posts** (600-800 characters)
- **Zero grammar/spelling errors** - LLM verification before publishing
- **Business-focused perspective** - ROI, strategy, unit economics
- **Multi-criteria paragraph breaks** - Intelligent formatting
- **50% news + 50% strategic topics** - Mix of timely + evergreen

### 🖼️ Intelligent Image Search
- **Multi-keyword analysis** - Detects 50+ contextual keywords
- **Smart prioritization** - Economics > Strategy > People > Tech
- **Pixabay integration** - Free, high-quality images
- **Contextual alignment** - Images match post content, not generic

### 🔗 LinkedIn Publishing
- **Automatic posting** - Posts with image + formatted text
- **LinkedIn API integration** - Native publishing (no IFTTT)
- **Error handling** - Graceful fallbacks

### ⚙️ Execution Options
- **Scheduled daemon** - Every 3.5 days at 10:00 AM
- **Immediate mode** - Generate & publish now
- **macOS Shortcut integration** - One-click publishing

---

## 🎯 Content Topics

### AI & Business Impact
- IA agéntica adoption in 2026
- Tech talent as bottleneck
- Automation paradox (less code, more architects)
- AI experiments → AI-driven revenue

### Team & Culture
- Engineering culture at scale (100+ people)
- Specialists vs. generalists
- Remote-first engineering
- Retaining senior engineers

### Product & Strategy
- Fast iteration vs. stable architecture
- Data-driven decision making
- Build vs. buy economics
- Open source as competitive advantage

### Infrastructure & Scale
- Serverless, containers, or VMs trade-offs
- Database selection impact
- Cost optimization as discipline
- Scaling inflection points

### Security & Reliability
- Security from day one
- Chaos engineering for startups
- Downtime costs
- Privacy as differentiator

---

## 🏗️ Architecture

```
linkedinposter/
├── main.py                 # Core bot logic
├── linkedinposter.sh       # macOS shell runner
├── requirements.txt        # Python dependencies
├── .env                    # API keys (confidential)
├── venv/                   # Python virtual environment
├── SETUP.md               # Installation guide
└── README.md              # This file
```

### Tech Stack
- **Python 3.9+**
- **Perplexity API** - Content generation + grammar checking
- **LinkedIn API v2** - Native posting
- **Pixabay API** - Image search
- **Schedule** - Daemon scheduling
- **Requests** - HTTP client

---

## 📊 Pipeline Flow

```
1. SELECT TOPIC
   ├─ 50% Recent news (news API search)
   └─ 50% Strategic topics (predefined list)

2. GENERATE POST
   ├─ Search context/news
   ├─ Generate 600-800 char post
   ├─ Format with intelligent paragraphs
   └─ Verify grammar & spelling

3. ANALYZE CONTENT
   ├─ Extract 50+ keyword patterns
   ├─ Prioritize by relevance (economics first)
   └─ Build image search query

4. FIND IMAGE
   ├─ Query Pixabay with context
   ├─ Select from 15 results
   └─ Register with LinkedIn API

5. PUBLISH
   ├─ Upload image to LinkedIn
   ├─ Post content + image
   └─ Log successful publish
```

---

## 🚀 Quick Start

### Prerequisites
- macOS (tested on macOS 12+)
- Python 3.9+
- API keys: Perplexity, LinkedIn, Pixabay

### 1️⃣ Clone & Setup

```bash
cd /path/to/linkedinposter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 2️⃣ Configure Credentials

```bash
cat > .env << 'EOF'
PERPLEXITY_API_KEY=your_key_here
LINKEDIN_ACCESS_TOKEN=your_token_here
LINKEDIN_PERSON_URN=urn:li:person:xxxxx
PIXABAY_API_KEY=your_key_here
EOF
```

### 3️⃣ Test

```bash
zsh linkedinposter.sh now
```

### 4️⃣ Automate with macOS Shortcut

See [SETUP.md](SETUP.md) for Shortcuts.app integration

---

## 📱 Usage

### Terminal
```bash
# Publish immediately
zsh linkedinposter.sh now

# Run scheduled daemon
zsh linkedinposter.sh daemon

# Show help
zsh linkedinposter.sh help
```

### macOS Shortcuts
1. Open **Shortcuts.app**
2. Create new shortcut
3. Add "Run Shell Script" (set shell to `zsh`)
4. Paste: `zsh /full/path/linkedinposter.sh now`
5. Run to test

### macOS Automation (Advanced)
1. Open **Automator.app**
2. Create **Calendar Alarm** at 10:00 AM
3. Add "Run Shell Script": `zsh /full/path/linkedinposter.sh now`

---

## 🔑 Getting API Keys

### Perplexity API
1. Visit https://www.perplexity.ai/api
2. Sign in / Create account
3. Create new API key
4. Copy to `.env` as `PERPLEXITY_API_KEY`

### LinkedIn API
1. Visit https://www.linkedin.com/developers/apps
2. Create new app
3. Get **Access Token** (personal use) → `LINKEDIN_ACCESS_TOKEN`
4. Get **Person URN** from API calls → `LINKEDIN_PERSON_URN`

### Pixabay API
1. Visit https://pixabay.com/api/docs/
2. Sign in / Create account
3. Get API key
4. Copy to `.env` as `PIXABAY_API_KEY`

---

## 📈 Post Quality Standards

✅ **Grammar & Spelling**
- LLM-verified before publishing
- Zero tolerance for errors
- Native Spanish (no Spanglish)

✅ **Content Quality**
- 600-800 characters
- 1-2 business case examples
- Reflective closing question
- 3-4 relevant hashtags

✅ **Image Quality**
- Business/professional context
- Landscape orientation
- High resolution (from Pixabay)
- Semantically aligned with post

---

## 🔧 Configuration

### Topics
Modify `TOPICS` list in `main.py` to customize content themes.

### Frequency
Change scheduled frequency in `main.py`:
```python
schedule.every(3.5).days.at("10:00").do(generar_y_publicar)
```

### Image Search
Keywords auto-detected from post content using 50+ patterns. Edit `keyword_patterns` dict to customize.

---

## 📊 Logs & Monitoring

Each run outputs detailed logs:
```
[2026-01-11 14:18:02] Generando post: TEMA ESTRATÉGICO
🔍 Buscando contexto...
✅ Contexto obtenido
✍️ Generando post...
✏️ Corrigiendo ortografía...
✅ Texto corregido correctamente
🔎 Análisis contextual del contenido...
   ✓ Detectado: 'coste'
   ✓ Detectado: 'margin'
   📊 Múltiples contextos detectados (4), priorizando...
🔍 Buscando imagen para: 'cost optimization'...
✅ Imagen encontrada
📤 Publicando en LinkedIn...
✅ ¡Publicado!
```

---

## 💰 Costs

| Service | Cost | Usage |
|---------|------|-------|
| **Perplexity API** | $0.03/post | Generation + grammar check |
| **LinkedIn API** | Free | Direct posting |
| **Pixabay API** | Free | Image search |
| **Total/post** | **$0.03** | |
| **Total/month** | **~$2.70** | 90 posts/month |

---

## 🐛 Troubleshooting

### Permission Denied in Shortcuts
→ Use `zsh` shell explicitly: `zsh /path/to/linkedinposter.sh now`

### Virtual Environment Not Found
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### .env File Not Found
Create `.env` in project root with all required keys.

### Image Search Returns Nothing
Check image query is not too specific. Keywords auto-detected from post content.

### Post Has Grammar Errors
Re-run immediately: `zsh linkedinposter.sh now`. LLM verifies all posts.

---

## 🔒 Security

⚠️ **Never commit `.env` to Git:**
```bash
echo ".env" >> .gitignore
git commit -m "Add .env to gitignore"
```

All API keys stay local. No external logging.

---

## 📝 Content Examples

### Example 1: Cost Optimization
```
El coste es una disciplina de ingeniería porque modela el sistema, 
no solo el Excel. Igual que con performance, la decisión clave no es 
"cuánto gastamos", sino "qué estamos comprando en margen, velocidad 
y foco de producto".

Ejemplo 1: una startup de SaaS recorta infra sin tocar producto, 
ahorra un 20%, pero degrada experiencia y el churn sube...
```

### Example 2: Team Culture
```
Building engineering cultures that scale beyond 100 people isn't 
about processes—it's about clarity. When you have 5 engineers, 
context flows naturally. At 100+, context becomes your limiting factor.

The question isn't "how do we manage more people"—it's "how do we 
maintain ownership and decision-making velocity as we grow?"
```

---

## 🤝 Contributing

This is a personal bot for Antonio Triguero's LinkedIn strategy. For modifications:

1. Test locally: `zsh linkedinposter.sh now`
2. Verify grammar output
3. Check image relevance
4. Only commit to your own fork

---

## 📞 Support

For issues or questions:
1. Check [SETUP.md](SETUP.md) troubleshooting
2. Review logs output (very detailed)
3. Verify `.env` has all API keys
4. Test in Terminal before Shortcuts

---

## 📄 License

Personal use only. Not for commercial distribution.

---

## 🎯 Roadmap

- [ ] Analytics dashboard (posts, engagement, followers)
- [ ] A/B testing (different topics/tones)
- [ ] Image caching (avoid re-downloading)
- [ ] Engagement tracking (likes, comments)
- [ ] Web interface for configuration
- [ ] Multi-account support
- [ ] Custom hashtag strategy

---

**Created for:** Antonio Triguero  
**Purpose:** Automated executive-level LinkedIn presence  
**Last Updated:** January 11, 2026

---

Made with ❤️ using Perplexity API + LinkedIn API v2
