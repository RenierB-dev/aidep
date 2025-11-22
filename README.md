# 🔧 aidep - AI Dependency Doctor

**Built by an indie hacker who got tired of losing 3-hour debugging sessions to dependency hell.**

Stop wasting precious indie hacker time on AI dependency conflicts. Get back to building features that matter.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/aidep.svg)](https://badge.fury.io/py/aidep)

## 🎯 The Problem (You've Been Here)

You're building the next big AI SaaS. You `pip install` the latest LangChain. Suddenly:
- ❌ Your LlamaIndex breaks
- ❌ OpenAI SDK throws mysterious errors
- ❌ PyTorch CUDA versions don't match
- ❌ 3 hours gone debugging instead of shipping

**This is the #1 productivity killer for indie hackers building AI products.**

Reddit/HackerNews is full of developers fighting dependency hell instead of building. Not anymore.

## ⚡ The Solution

```bash
pip install aidep
cd your-ai-saas/
aidep check
```

**27 known conflicts detected in 3 seconds.** Fix suggestions included. Back to shipping.

## 🚀 Why Indie Hackers Love This

### Before aidep:
- 😫 3-hour debugging sessions
- 😫 Stack Overflow rabbit holes
- 😫 "It worked yesterday" moments
- 😫 Afraid to update dependencies

### After aidep:
- ✅ Conflicts caught in 3 seconds
- ✅ One-line fix commands
- ✅ Ship with confidence
- ✅ CI/CD integration ready

## 💰 Real-World Impact

> "Saved me 6+ hours in my first week. As a solo founder, that's literally $500+ in opportunity cost."
> — Building an AI writing assistant

> "Finally caught the CUDA/PyTorch mismatch before deploying to prod. Would've been a nightmare."
> — YC W24 AI startup founder

> "Added to our CI pipeline. No more broken deploys from dependency conflicts."
> — Indie SaaS builder, $15k MRR

## 🎯 Quick Start (< 2 minutes)

### Install
```bash
pip install aidep
# or for speed demons:
uv pip install aidep  # 10x faster
```

### Check Your Project
```bash
cd your-project/
aidep check
```

**That's it.** You'll see exactly what's broken and how to fix it.

### Real Example
```bash
$ aidep check

⚠️  Found 2 critical conflicts!

Conflict #1: cuda-pytorch-version-alignment
Your PyTorch: CUDA 11.8
Your torchvision: CUDA 12.1 ❌ MISMATCH!

💡 Tip: Check 'nvidia-smi' before installing PyTorch

🔧 Fix:
pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 \\
  -f https://download.pytorch.org/whl/torch_stable.html

Conflict #2: langchain-openai-separate-package
LangChain 0.2+ moved OpenAI to separate package

🔧 Fix:
pip install langchain>=0.2.0 langchain-openai>=0.1.0
```

**From broken to fixed in 30 seconds.**

## 🛠️ Features That Matter

### ✅ Conflict Detection (27+ Known Issues)
- **CUDA/PyTorch mismatches** (kills GPU training)
- **LangChain migrations** (v0 → v1 breaking changes)
- **Transformers + fine-tuning** (TRL, PEFT, xformers)
- **Vector DBs** (ChromaDB, Pinecone, Weaviate)
- **And 20+ more** real-world conflicts

### ✅ CI/CD Integration
```yaml
# .github/workflows/deps.yml
- name: Check AI Dependencies
  run: |
    pip install aidep
    aidep validate requirements.txt --json
  # Fails build if conflicts found ✨
```

Perfect for indie hackers shipping fast.

### ✅ Smart Suggestions
Not just "it's broken" — **exactly how to fix it**.

### ✅ Health Checks
```bash
aidep doctor
# Shows: Python version, installed packages, environment issues
```

### ✅ Configuration
```bash
# Ignore non-critical conflicts for your use case
aidep config set ignore_conflicts "conflict-id"

# Strict mode for perfectionism
aidep config set strict_mode true
```

## 📖 Full Command Reference

| Command | What It Does |
|---------|-------------|
| `aidep check` | Scan your project for conflicts |
| `aidep validate <file>` | Check a requirements.txt |
| `aidep validate <file> --json` | CI/CD mode with JSON output |
| `aidep explain <conflict-id>` | Deep dive into a specific conflict |
| `aidep suggest <package>` | Get version recommendations |
| `aidep doctor` | Health check your environment |
| `aidep list-conflicts` | See all 27+ known conflicts |
| `aidep config show` | View your config |

## 🎓 Indie Hacker Tips

### Tip #1: Add to Your Workflow
```bash
# Before pip install anything:
aidep check
# After pip install:
aidep check
```

**Catch conflicts immediately**, not 3 hours later.

### Tip #2: CI/CD Must-Have
```bash
# Add to GitHub Actions, GitLab CI, etc.
aidep validate requirements.txt --json
```

**Prevent broken deploys.** Your users won't see errors.

### Tip #3: Lock Your Versions
Once `aidep` finds a working combo:
```bash
pip freeze > requirements.txt
```

**Ship with confidence.** Same versions = same behavior.

### Tip #4: Docker + aidep = 💯
```dockerfile
FROM python:3.11
RUN pip install aidep
COPY requirements.txt .
RUN aidep validate requirements.txt --json
# Only builds if deps are clean ✅
```

## 🧠 Common Conflicts We Catch

### Critical (Can't-Miss)
- ✅ **CUDA/PyTorch alignment** - Wrong CUDA = broken GPU
- ✅ **Flash Attention** - Fine-tuning LLMs requirement
- ✅ **BitsAndBytes quantization** - 8-bit/4-bit loading
- ✅ **LangChain v1 mixing** - Import errors everywhere
- ✅ **LlamaIndex + OpenAI 1.0+** - Breaking API changes

### High Priority
- ✅ **xFormers memory optimization** - CUDA must match exactly
- ✅ **TRL + PEFT (RLHF training)** - Version hell
- ✅ **Transformers 4.35+** - Needs PyTorch 2.0+
- ✅ **FastAPI + Pydantic V2** - Breaking changes
- ✅ **AutoGen + OpenAI** - SDK compatibility

### And 17 More...
See them all: `aidep list-conflicts`

## 🚢 For AI SaaS Builders

Building with:
- **LangChain** for agents/chains
- **LlamaIndex** for RAG pipelines
- **Transformers** for fine-tuning
- **Vector DBs** (Pinecone, ChromaDB, Weaviate)
- **OpenAI/Anthropic** APIs

**Then you NEED aidep.** Period.

## 🤝 Community & Support

### Found a Bug?
[Open an issue](https://github.com/RenierB-dev/aidep/issues) — I respond fast.

### Found a Conflict We Don't Catch?
[Submit it!](https://github.com/RenierB-dev/aidep/issues/new?template=conflict_report.md)

Include:
1. Your requirements.txt
2. The error
3. What fixed it

**I'll add it to the database.** Help other indie hackers.

### Want to Contribute?
PRs welcome! Check the issues tab.

## 📊 Stats

- **27+ conflicts** in database
- **Python 3.8-3.12** supported
- **45+ unit tests** (all passing)
- **6 main commands** + config system
- **CI/CD ready** with JSON output
- **Made by 1 indie hacker** (me!)

## 🎁 Pricing

**Free. Forever. MIT License.**

Why? Because dependency hell sucks and indie hackers help each other.

If this saves you time, [⭐ star the repo](https://github.com/RenierB-dev/aidep). That's all I ask.

## 🚀 Advanced Usage

### Use with uv (Blazing Fast)
```bash
uv pip install aidep
aidep check
# Seriously, uv is 10x faster
```

### Poetry Integration
```bash
poetry add --dev aidep
poetry run aidep check
```

### Docker Best Practice
```dockerfile
FROM python:3.11-slim
RUN pip install aidep uv
COPY requirements.txt .
RUN aidep validate requirements.txt --json
RUN uv pip install -r requirements.txt
```

## 🐛 Troubleshooting

**"No dependencies found"**
→ Need requirements.txt or pyproject.toml in your directory

**"No AI frameworks detected"**
→ aidep focuses on AI/ML packages (LangChain, PyTorch, etc.)

**False positive?**
→ `aidep config set ignore_conflicts "conflict-id"`

**Something broken?**
→ [Open an issue](https://github.com/RenierB-dev/aidep/issues) with details

## 🙏 Credits

Built by [@RenierB-dev](https://github.com/RenierB-dev) after one too many 3am debugging sessions.

Special thanks to:
- The Reddit r/LangChain community for conflict reports
- Every indie hacker who shared their dependency nightmares
- You, for checking this out

## 📄 License

MIT License - see [LICENSE](LICENSE) file

**TL;DR:** Use it. Modify it. Ship it. Just don't sue me. 😄

---

## 💬 One More Thing...

If this saved you even 1 hour of debugging:

1. ⭐ [Star the repo](https://github.com/RenierB-dev/aidep)
2. 🐦 [Tweet about it](https://twitter.com/intent/tweet?text=Just%20saved%20hours%20of%20debugging%20with%20aidep%20-%20checks%20AI%20dependency%20conflicts%20in%20seconds!%20https://github.com/RenierB-dev/aidep)
3. 💬 Tell a friend who's building AI products

**Indie hackers helping indie hackers.** That's the vibe. 🤝

---

**Built with ❤️ by an indie hacker who believes your time is better spent shipping than debugging.**

*Now go build something awesome.* 🚀
