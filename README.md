# 🔧 aidep - AI Dependency Doctor

**Stop wasting hours on AI dependency hell.**

Automatically detect and fix LangChain, LlamaIndex, PyTorch, and other AI framework conflicts in under 60 seconds.

## 🚀 Quick Start

```bash
pip install aidep

# Check your project
cd your-ai-project/
aidep check

# Validate requirements file
aidep validate requirements.txt

# Get fix suggestions
aidep suggest langchain
```

## 💡 Why aidep?

AI frameworks change fast. LangChain 0.3 breaks LlamaIndex 0.10. OpenAI SDK updates break everything. PyTorch CUDA versions must match exactly. You spend hours debugging `ModuleNotFoundError` and cryptic pip conflicts.

**aidep knows which versions work together** so you don't waste time.

## 🎯 Features

- ✅ Scan requirements.txt for AI framework conflicts
- ✅ **30+ known conflicts** including CUDA/PyTorch, LangChain, transformers, and more
- ✅ Suggest working version combinations
- ✅ **CI/CD integration** with JSON output
- ✅ Health checks for your development environment
- ✅ Handles alpha/beta/rc version parsing
- ✅ Configuration system for customization
- ✅ Works with pip, uv, poetry, conda

## 📦 Installation

```bash
pip install aidep
```

Or with uv (10x faster):
```bash
uv pip install aidep
```

## 🔍 Usage

### Check Your Project
```bash
aidep check
```

Scans your project and identifies conflicts in your AI framework dependencies.

### Validate Requirements File
```bash
aidep validate requirements.txt
```

### CI/CD Integration
```bash
# Add to your CI pipeline
aidep validate requirements.txt --json
# Exits with code 1 if conflicts found
```

Example GitHub Actions workflow:
```yaml
- name: Check AI Dependencies
  run: |
    pip install aidep
    aidep validate requirements.txt --json
```

### Get Fix Suggestions
```bash
aidep suggest langchain
```

### Explain a Conflict
```bash
aidep explain langchain-openai-separate-package
```

### Health Check
```bash
aidep doctor
```

Checks Python version, installed packages, and environment setup.

### List All Conflicts
```bash
aidep list-conflicts
```

### Configuration
```bash
# Ignore specific conflicts
aidep config set ignore_conflicts "conflict-id-1,conflict-id-2"

# Enable strict mode (warn on ALL potential conflicts)
aidep config set strict_mode true

# Show current config
aidep config show
```

## 🔥 Real-World Examples

### Example 1: Caught Before 3 Hours of Debugging
```bash
$ aidep check

⚠️  Found 2 potential conflicts!

Conflict #1: langchain-openai-separate-package
Severity: MEDIUM
LangChain 0.2+ moved OpenAI integration to separate package

Your packages:
  • langchain: ==0.0.330
  • openai: ==1.0.0

💡 Suggested fix:
┌─────────────────────────────────────────┐
│ pip install langchain>=0.2.0            │
│ langchain-openai>=0.1.0 openai>=1.0.0   │
└─────────────────────────────────────────┘

💡 Tip: LangChain v1 (0.1+) is recommended for new projects.
```

### Example 2: CUDA Version Mismatch
```bash
$ aidep check

⚠️  Critical: cuda-pytorch-version-alignment
Your PyTorch is compiled for CUDA 11.8 but you're trying to use CUDA 12.1 packages

Affected packages:
  • torch: ==2.0.0+cu118
  • torchvision: ==0.16.0+cu121  ❌ Mismatch!

💡 Tip: Check your CUDA version with 'nvidia-smi' before installing PyTorch

💡 Suggested fix:
┌─────────────────────────────────────────────────────────────────┐
│ # For CUDA 11.8:                                                │
│ pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 \\     │
│   -f https://download.pytorch.org/whl/torch_stable.html         │
└─────────────────────────────────────────────────────────────────┘
```

### Example 3: Fine-Tuning Package Conflicts
```bash
$ aidep validate requirements.txt

❌ Validation failed!

Found 1 potential conflict(s).

• TRL (Transformer Reinforcement Learning) requires specific PEFT and
  Transformers versions for RLHF training

💡 Tip: When fine-tuning models, lock all training package versions in requirements.txt
```

## 📖 Common Conflicts We Catch

### Critical Conflicts
- ✅ **CUDA/PyTorch version alignment** - CUDA toolkit must match PyTorch CUDA version
- ✅ **Flash Attention requirements** - Needs specific CUDA 11.6+ and PyTorch versions
- ✅ **BitsAndBytes CUDA requirement** - Quantization requires CUDA-enabled PyTorch
- ✅ **LangChain v1 vs classic mixing** - Import errors and namespace conflicts
- ✅ **LlamaIndex + OpenAI SDK 1.0+** - Breaking API changes

### High Priority Conflicts
- ✅ **xFormers + PyTorch CUDA alignment** - Must match CUDA versions exactly
- ✅ **TRL + PEFT + Transformers** - RLHF training version requirements
- ✅ **Transformers + torch version** - Transformers 4.35+ requires PyTorch 2.0+
- ✅ **FastAPI + Pydantic V2** - FastAPI <0.100 incompatible with Pydantic 2.0+
- ✅ **AutoGen + OpenAI SDK** - AutoGen <0.2.0 breaks with OpenAI 1.0+
- ✅ **Haystack + Transformers** - Version pinning conflicts

### Medium Priority Conflicts
- ✅ **ChromaDB + SQLite** - Linux SQLite dependencies
- ✅ **Pinecone + gRPC** - Version constraints
- ✅ **Sentence Transformers + PyTorch** - Minimum version requirements
- ✅ **Weaviate + gRPC/protobuf** - Specific version requirements
- ✅ And 10+ more...

## ⚙️ Configuration

Customize aidep behavior:

```bash
# Ignore specific conflicts
aidep config set ignore_conflicts "conflict-id-1,conflict-id-2"

# Enable strict mode (warn on ALL potential conflicts)
aidep config set strict_mode true

# Show current config
aidep config show
```

Configuration file location: `~/.aidep/config.json`

Available settings:
- `check_cuda_versions` (bool): Check CUDA version mismatches
- `strict_mode` (bool): Warn on all potential conflicts
- `ignore_conflicts` (list): Conflict IDs to ignore
- `output_format` (string): "rich", "simple", or "json"

## 🤝 Contributing

Found a conflict we don't detect? [Open an issue](https://github.com/RenierB-dev/aidep/issues) with:
1. Your requirements.txt
2. The error you got
3. The working version combination

We'll add it to the database!

### Adding Custom Conflicts

You can also add custom conflicts to your local configuration:

```bash
aidep config set custom_conflicts '[{"id": "my-conflict", "packages": ["pkg1", "pkg2"], ...}]'
```

## 📊 Stats

- **30+ known conflicts** in database
- **Python 3.8-3.12** supported
- **45+ unit tests** (100% passing)
- **6 CLI commands** + configuration
- **CI/CD ready** with JSON output

## 🚀 Advanced Usage

### Use with uv (10x faster)
```bash
uv pip install aidep
aidep check
```

### Integration with Poetry
```bash
poetry add --dev aidep
poetry run aidep check
```

### Docker Integration
```dockerfile
FROM python:3.11
RUN pip install aidep
COPY requirements.txt .
RUN aidep validate requirements.txt --json
```

## 📝 Command Reference

| Command | Description |
|---------|-------------|
| `aidep check` | Scan project for conflicts |
| `aidep validate <file>` | Validate requirements file |
| `aidep validate <file> --json` | JSON output for CI/CD |
| `aidep suggest <package>` | Get version suggestions |
| `aidep explain <conflict-id>` | Explain specific conflict |
| `aidep doctor` | Health check environment |
| `aidep list-conflicts` | List all known conflicts |
| `aidep config show` | Show configuration |
| `aidep config set <key> <value>` | Set config value |

## 🐛 Troubleshooting

### "No dependencies found"
Make sure you have a `requirements.txt` or `pyproject.toml` in your project directory.

### "No AI framework dependencies detected"
aidep focuses on AI/ML frameworks. If you're using other packages, they won't be checked.

### False positives
Use `aidep config set ignore_conflicts "conflict-id"` to ignore specific conflicts.

## 📄 License

MIT License - see LICENSE file for details

---

**Made with ❤️ by developers who are tired of dependency hell**

Built by [@RenierB-dev](https://github.com/RenierB-dev)

🌟 Star us on GitHub if aidep saved you time!
