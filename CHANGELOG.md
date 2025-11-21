# Changelog

All notable changes to aidep will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-21

### 🚀 Major Release - World-Class Enhancements

This release transforms aidep into a production-ready tool based on real user feedback from Reddit AI/ML developers.

### Added

#### New CLI Commands
- **`aidep doctor`** - Health check command for AI development environment
  - Checks Python version
  - Shows installed AI packages and versions
  - Provides environment diagnostics
- **`aidep explain <conflict-id>`** - Detailed conflict explanations
  - Shows full description, severity, affected packages
  - Displays working and alternative versions
  - Provides detailed fix instructions
- **`aidep config`** - Configuration management system
  - `aidep config show` - Display current configuration
  - `aidep config set <key> <value>` - Set configuration values
  - Support for ignoring conflicts, strict mode, output formats
- **`--json` flag for `validate` command** - CI/CD integration
  - Machine-readable JSON output
  - Exit code 1 on conflicts for pipeline failures
  - Perfect for GitHub Actions, GitLab CI, etc.

#### New Conflicts (7 critical additions) - Total now 27+
- **CUDA/PyTorch Conflicts** (5 new):
  - `cuda-pytorch-version-alignment` - CUDA toolkit must match PyTorch CUDA version
  - `flash-attention-cuda-requirements` - Flash Attention needs CUDA 11.6+ and PyTorch 2.0+
  - `xformers-torch-cuda-alignment` - xFormers must match PyTorch CUDA version exactly
  - `trl-peft-transformers-alignment` - TRL (RLHF training) version requirements
  - `bitsandbytes-cuda-requirement` - BitsAndBytes quantization needs CUDA-enabled PyTorch
- **LangChain Migration Conflicts** (2 new):
  - `langchain-v1-classic-mixing` - Mixing LangChain classic (0.0.x) with v1 (0.1.x+)
  - `langchain-deprecated-integrations` - LangChain moved integrations to separate packages

#### Enhanced Features
- **Configuration System** (new `config.py` module)
  - Persistent configuration in `~/.aidep/config.json`
  - Options: `check_cuda_versions`, `strict_mode`, `ignore_conflicts`, `output_format`
  - User-customizable behavior
- **Better Error Messages with Contextual Tips**
  - Helpful tips based on conflict type
  - CUDA-specific guidance
  - LangChain migration recommendations
  - Fine-tuning best practices
- **CUDA Version Detection**
  - New `_extract_cuda_version()` method
  - Detects CUDA version from PyTorch specs (e.g., +cu118, +cu121)
- **Expanded AI Framework Support**
  - Added 15+ new packages to scanner: `flash-attn`, `xformers`, `trl`, `peft`, `bitsandbytes`, `pyautogen`, etc.

### Changed
- Updated CLI version to **0.2.0**
- Enhanced `validate` command with `--json` flag for CI/CD
- Improved conflict display with helpful tips
- Expanded README with real-world examples and comprehensive documentation
- Better error messages in `ConflictChecker._evaluate_conflict()`

### Documentation
- **Comprehensive README rewrite** with:
  - Real-world debugging examples
  - CI/CD integration examples (GitHub Actions)
  - Complete command reference table
  - Troubleshooting section
  - Docker integration example
- **New GitHub Issue Template** (`.github/ISSUE_TEMPLATE/conflict_report.md`)
- Enhanced CHANGELOG with detailed release notes

### Stats for v0.2.0
- **27+ total conflicts** (was 20 in v0.1.1)
- **6 main CLI commands** (was 4)
- **Configuration system** with 5+ settings
- **CI/CD ready** with JSON output

### Migration Notes
- No breaking changes from v0.1.1
- New commands are additive
- Configuration is optional (defaults provided)
- All existing workflows continue to work

## [0.1.1] - 2025-11-21

### Added
- **10 new conflict definitions** expanding database to 20 total conflicts:
  - transformers + torch version conflicts
  - ChromaDB + SQLite dependencies
  - PyTorch CUDA version matching (torch + torchvision)
  - FastAPI + Pydantic V2 compatibility
  - Pinecone client + gRPC version constraints
  - Sentence Transformers + PyTorch requirements
  - Haystack + Transformers version pinning
  - AutoGen + OpenAI SDK compatibility
  - Microsoft Guidance + Transformers tokenizer issues
  - Weaviate client + gRPC/protobuf dependencies
- Enhanced version parsing to handle **alpha/beta/rc versions** (e.g., 2.0.0rc1, 1.5a1)
- `tomli` dependency for Python <3.11 TOML parsing support
- Comprehensive test suite with **20+ tests** covering:
  - Conflict database validation
  - Version normalization and parsing
  - Conflict detection logic
  - Compatibility matrix functionality
  - Edge cases and error handling
- Development dependencies in setup.py extras_require:
  - pytest, pytest-cov for testing
  - black, flake8, mypy for code quality

### Changed
- Updated version to 0.1.1 in setup.py
- Improved `_normalize_version()` method in checker.py to handle pre-release versions
- Enhanced `_version_satisfies()` to use normalized versions for better accuracy
- Removed `anthropic` from core dependencies (not needed for core functionality)

### Fixed
- Better version comparison for packages using alpha/beta/rc suffixes
- More robust version parsing regex patterns

## [0.1.0] - 2025-11-20

### Added
- Initial release of aidep - AI Dependency Doctor
- Core conflict detection for 10 major AI framework conflicts
- CLI commands: check, suggest, validate
- Support for LangChain, LlamaIndex, OpenAI, and related frameworks
- Compatibility matrix for common framework combinations
- Rich console output with colored formatting
- Requirements.txt and pyproject.toml scanning
