# Changelog

All notable changes to aidep will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
