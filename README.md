# 🎬 TikTok Scripts Generator

Create engaging, ready-to-record scripts for **TikTok, Instagram Reels, and YouTube Shorts**.

A polished, beginner-friendly web app built with Python and Streamlit. Describe your idea, choose a target audience and style, and generate a hook, spoken script, captions, shot suggestions, hashtags, and a call to action.

## ✨ Features

- Topic-to-script generation with a strong opening hook
- Multiple languages, niches, and writing tones
- Video lengths from 15 to 90 seconds
- Adjustable spoken-script character target
- Optional captions, shot list, hashtags, and CTA
- Editable output with `.txt` and `.md` downloads
- API key loaded from environment variables or Streamlit Secrets
- Dark, responsive interface
- Prompt helpers covered by basic unit tests

## 🖥️ Preview

Run the app locally to view the interface.

## 🚀 Run locally

### Requirements
- Python 3.10 or newer
- An API key for a model available through the OpenAI API

### 1. Download the repository

```bash
git clone https://github.com/YOUR-USERNAME/tiktok-scripts-generator.git
cd tiktok-scripts-generator
```

Or download the repository as a ZIP from GitHub and extract it.

### 2. Create a virtual environment (recommended)

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Copy `.env.example` to `.env` and replace the placeholder:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The `.env` file is ignored by Git. **Never commit your API key.**

Alternatively, set `OPENAI_API_KEY` in your shell environment or Streamlit Secrets.

### 5. Start the app

```bash
streamlit run app.py
```

Open the local URL shown in your terminal, usually `http://localhost:8501`.

## ☁️ Deploy with Streamlit Community Cloud

1. Push this repository to your GitHub account.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
3. Create an app and select `app.py` as the entry point.
4. Open the app settings and add a secret:

```toml
OPENAI_API_KEY = "your_api_key_here"
OPENAI_MODEL = "gpt-4.1-mini"
```

5. Deploy the app.

Hosting may offer a free tier, but AI API usage is separate and may cost money. Availability and pricing depend on the provider and your account.

## 🧪 Run tests

```bash
python -m unittest discover -s tests -v
```

## 🔐 Privacy and security

- Prompts are sent to the configured AI provider to generate a script.
- Do not enter passwords, sensitive personal information, or confidential material.
- API keys should be stored in environment variables or Streamlit Secrets.
- Never commit `.env` or `.streamlit/secrets.toml`.
- The app does not include a server-side script history or analytics tracker.

## 🗺️ Roadmap

- [ ] Generate multiple script variations
- [ ] Export subtitles as SRT
- [ ] Add saved script history (opt-in)
- [ ] Add CapCut-friendly formatting
- [ ] Add more niche-specific templates
- [ ] Add a prompt-only mode that does not require an API key

## 🤝 Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT. See [LICENSE](LICENSE).

---

Made for creators. Built with Python. 🎥
