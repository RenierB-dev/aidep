"""
Known AI framework dependency conflicts database.
Based on GitHub issues, Stack Overflow, and community reports.
"""

# Each conflict has:
# - packages: List of conflicting packages
# - description: What breaks
# - working_versions: Known good combinations
# - fix: Suggested resolution

CONFLICTS = [
    {
        "id": "langchain-llama-sqlalchemy",
        "packages": ["langchain", "llama-index"],
        "description": "LangChain >=0.0.200 requires SQLAlchemy >=2.0, but LlamaIndex <0.8 requires SQLAlchemy >=1.4,<2.0",
        "severity": "critical",
        "working_versions": {
            "langchain": "0.0.198",
            "llama-index": "0.7.5"
        },
        "alternative": {
            "langchain": ">=0.1.0",
            "llama-index": ">=0.8.0"
        },
        "fix": "pip install langchain==0.0.198 llama-index==0.7.5\nOR upgrade both:\npip install langchain>=0.1.0 llama-index>=0.8.0"
    },
    {
        "id": "langchain-community-langsmith",
        "packages": ["langchain", "langchain-community"],
        "description": "LangChain 0.1.6 depends on langsmith<0.1, but langchain-community 0.0.28+ depends on langsmith>=0.1.0",
        "severity": "critical",
        "working_versions": {
            "langchain": "0.1.7",
            "langchain-community": "0.0.28"
        },
        "fix": "pip install langchain==0.1.7 langchain-community==0.0.28"
    },
    {
        "id": "llama-index-langchain-version",
        "packages": ["llama-index", "langchain"],
        "description": "LlamaIndex 0.5.x pins langchain==0.0.142, conflicts with newer LangChain versions",
        "severity": "critical",
        "working_versions": {
            "llama-index": "0.5.27",
            "langchain": "0.0.142"
        },
        "alternative": {
            "llama-index": ">=0.6.0",
            "langchain": ">=0.0.154"
        },
        "fix": "pip install llama-index==0.5.27 langchain==0.0.142\nOR upgrade both:\npip install llama-index>=0.6.8 langchain>=0.0.154"
    },
    {
        "id": "openai-langchain-breaking",
        "packages": ["openai", "langchain"],
        "description": "OpenAI SDK 1.0+ has breaking API changes, older LangChain versions incompatible",
        "severity": "high",
        "working_versions": {
            "openai": "0.28.1",
            "langchain": "0.0.330"
        },
        "alternative": {
            "openai": ">=1.0.0",
            "langchain": ">=0.1.0"
        },
        "fix": "pip install openai==0.28.1 langchain==0.0.330\nOR upgrade both:\npip install openai>=1.0.0 langchain>=0.1.0"
    },
    {
        "id": "llama-index-openai-version",
        "packages": ["llama-index", "openai"],
        "description": "LlamaIndex <0.9.0 requires openai<1.0, breaks with OpenAI 1.0+",
        "severity": "high",
        "working_versions": {
            "llama-index": "0.8.69",
            "openai": "0.28.1"
        },
        "alternative": {
            "llama-index": ">=0.9.0",
            "openai": ">=1.0.0"
        },
        "fix": "pip install llama-index==0.8.69 openai==0.28.1\nOR upgrade both:\npip install llama-index>=0.9.0 openai>=1.0.0"
    },
    {
        "id": "crewai-llama-embedchain",
        "packages": ["crewai", "llama-index"],
        "description": "CrewAI 0.121+ introduces transitive dependency on embedchain, conflicts with llama-index 0.10.x",
        "severity": "high",
        "working_versions": {
            "crewai": "0.100.1",
            "llama-index": "0.10.51"
        },
        "alternative": {
            "crewai": ">=0.121.0",
            "llama-index": ">=0.12.38"
        },
        "fix": "pip install crewai==0.100.1 llama-index==0.10.51\nOR upgrade both:\npip install crewai>=0.121.0 llama-index>=0.12.38"
    },
    {
        "id": "langchain-openai-separate-package",
        "packages": ["langchain", "openai"],
        "description": "LangChain 0.2+ moved OpenAI integration to separate langchain-openai package",
        "severity": "medium",
        "working_versions": {
            "langchain": ">=0.2.0",
            "langchain-openai": ">=0.1.0",
            "openai": ">=1.0.0"
        },
        "fix": "pip install langchain>=0.2.0 langchain-openai>=0.1.0 openai>=1.0.0"
    },
    {
        "id": "pydantic-v2-breaking",
        "packages": ["pydantic", "langchain", "llama-index"],
        "description": "Pydantic V2 (2.0+) has breaking changes, many AI frameworks not compatible",
        "severity": "high",
        "working_versions": {
            "pydantic": "1.10.13",
            "langchain": "0.0.330",
            "llama-index": "0.8.69"
        },
        "alternative": {
            "pydantic": ">=2.0.0",
            "langchain": ">=0.1.0",
            "llama-index": ">=0.9.0"
        },
        "fix": "pip install pydantic==1.10.13 langchain==0.0.330 llama-index==0.8.69\nOR upgrade all:\npip install pydantic>=2.0.0 langchain>=0.1.0 llama-index>=0.9.0"
    },
    {
        "id": "numpy-scipy-torch-version",
        "packages": ["numpy", "torch", "transformers"],
        "description": "PyTorch and Transformers have specific NumPy version requirements",
        "severity": "medium",
        "working_versions": {
            "numpy": ">=1.21.0,<2.0.0",
            "torch": ">=2.0.0",
            "transformers": ">=4.30.0"
        },
        "fix": "pip install 'numpy>=1.21.0,<2.0.0' torch>=2.0.0 transformers>=4.30.0"
    },
    {
        "id": "langflow-llama-sqlalchemy",
        "packages": ["langflow", "llama-index"],
        "description": "Langflow depends on SQLAlchemy 1.4.x, LlamaIndex 0.7.5+ needs SQLAlchemy >=2.0.15",
        "severity": "critical",
        "working_versions": {
            "langflow": "0.5.0",
            "llama-index": "0.7.4"
        },
        "fix": "pip install langflow==0.5.0 'llama-index<0.7.5'"
    }
]

# Common framework version compatibility matrix
COMPATIBILITY_MATRIX = {
    "langchain": {
        "0.0.142": {"llama-index": ["0.5.x"], "openai": ["0.27.x", "0.28.x"]},
        "0.0.330": {"openai": ["0.28.x"], "pydantic": ["1.10.x"]},
        "0.1.0+": {"openai": ["1.0+"], "langchain-openai": ["0.1.0+"], "pydantic": ["2.0+"]},
        "0.2.0+": {"langchain-openai": ["required"], "langchain-community": ["0.2.0+"]},
    },
    "llama-index": {
        "0.5.x": {"langchain": ["0.0.142"], "sqlalchemy": ["1.4.x"]},
        "0.6.x-0.7.x": {"langchain": [">=0.0.154"], "sqlalchemy": ["1.4.x"]},
        "0.8.0+": {"sqlalchemy": [">=2.0"], "openai": ["0.28.x"]},
        "0.9.0+": {"openai": ["1.0+"], "pydantic": ["2.0+"]},
    },
    "openai": {
        "0.28.x": {"langchain": ["<0.1.0"], "llama-index": ["<0.9.0"]},
        "1.0+": {"langchain": [">=0.1.0"], "llama-index": [">=0.9.0"]},
    }
}

# Package aliases and renames
PACKAGE_RENAMES = {
    "openai": {
        "old_import": "import openai",
        "new_import_v1": "from openai import OpenAI",
        "breaking_version": "1.0.0",
        "migration_guide": "https://github.com/openai/openai-python/discussions/742"
    },
    "langchain": {
        "split_packages": ["langchain-core", "langchain-community", "langchain-openai"],
        "version": "0.2.0",
        "migration_guide": "https://python.langchain.com/docs/versions/v0_2/"
    }
}
