# 🔧 aidep - AI Dependency Doctor

**Stop wasting hours on AI dependency hell.**

Automatically detect and fix LangChain, LlamaIndex, and OpenAI version conflicts in under 60 seconds.

## 🚀 Quick Start

```bash
pip install aidep

# Scan your project
aidep check

# Get compatible versions
aidep suggest langchain

# Validate requirements file
aidep validate requirements.txt
```

## 💡 Why aidep?

AI frameworks change fast. LangChain 0.3 breaks LlamaIndex 0.10. OpenAI SDK updates break everything. You spend hours debugging `ModuleNotFoundError` and cryptic pip conflicts.

**aidep knows which versions work together** so you don't waste time.

## 🎯 Features

- ✅ Scan requirements.txt for AI framework conflicts
- ✅ Database of 20+ known LangChain/LlamaIndex/OpenAI incompatibilities
- ✅ Suggest working version combinations
- ✅ Works with pip, uv, poetry, conda
- ✅ Handles alpha/beta/rc version parsing
- ✅ Comprehensive test coverage

## 📦 Installation

```bash
pip install aidep
```

Or with uv (10x faster):
```bash
uv pip install aidep
```

## 🔍 Usage

### Check your current project
```bash
aidep check
```

### Suggest compatible versions
```bash
aidep suggest langchain
aidep suggest llama-index
aidep suggest openai
```

### Validate a requirements file
```bash
aidep validate requirements.txt
```

## 🤝 Contributing

Built by [@RenierB-dev](https://github.com/RenierB-dev)

Found a conflict we don't detect? [Open an issue](https://github.com/RenierB-dev/aidep/issues)!

## 📄 License

MIT License - see LICENSE file for details

---

**Made with ❤️ by developers who are tired of dependency hell**
