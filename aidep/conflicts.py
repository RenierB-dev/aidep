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
    },
    {
        "id": "transformers-torch-version",
        "packages": ["transformers", "torch"],
        "description": "Transformers 4.35+ requires PyTorch 2.0+, conflicts with older torch versions",
        "severity": "high",
        "working_versions": {
            "transformers": "4.34.1",
            "torch": "1.13.1"
        },
        "alternative": {
            "transformers": ">=4.35.0",
            "torch": ">=2.0.0"
        },
        "fix": "pip install transformers==4.34.1 torch==1.13.1\nOR upgrade both:\npip install transformers>=4.35.0 torch>=2.0.0"
    },
    {
        "id": "chromadb-sqlite-version",
        "packages": ["chromadb", "pysqlite3-binary"],
        "description": "ChromaDB 0.4.0+ requires pysqlite3-binary on Linux, conflicts with system SQLite",
        "severity": "medium",
        "working_versions": {
            "chromadb": ">=0.4.0",
            "pysqlite3-binary": ">=0.5.0"
        },
        "fix": "pip install chromadb>=0.4.0 pysqlite3-binary>=0.5.0"
    },
    {
        "id": "torch-cuda-version",
        "packages": ["torch", "torchvision"],
        "description": "PyTorch CUDA versions must match between torch and torchvision",
        "severity": "critical",
        "working_versions": {
            "torch": "2.0.0+cu118",
            "torchvision": "0.15.0+cu118"
        },
        "fix": "pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 --index-url https://download.pytorch.org/whl/cu118"
    },
    {
        "id": "fastapi-pydantic-v2",
        "packages": ["fastapi", "pydantic"],
        "description": "FastAPI <0.100 incompatible with Pydantic V2 (2.0+)",
        "severity": "high",
        "working_versions": {
            "fastapi": "0.95.2",
            "pydantic": "1.10.13"
        },
        "alternative": {
            "fastapi": ">=0.100.0",
            "pydantic": ">=2.0.0"
        },
        "fix": "pip install fastapi==0.95.2 pydantic==1.10.13\nOR upgrade both:\npip install fastapi>=0.100.0 pydantic>=2.0.0"
    },
    {
        "id": "pinecone-grpc-version",
        "packages": ["pinecone-client", "grpcio"],
        "description": "Pinecone client 2.x requires grpcio <1.60, conflicts with newer gRPC versions",
        "severity": "medium",
        "working_versions": {
            "pinecone-client": ">=2.0.0,<3.0.0",
            "grpcio": ">=1.50.0,<1.60.0"
        },
        "alternative": {
            "pinecone-client": ">=3.0.0",
            "grpcio": ">=1.60.0"
        },
        "fix": "pip install 'pinecone-client>=2.0.0,<3.0.0' 'grpcio>=1.50.0,<1.60.0'\nOR upgrade both:\npip install pinecone-client>=3.0.0 grpcio>=1.60.0"
    },
    {
        "id": "sentence-transformers-torch",
        "packages": ["sentence-transformers", "torch"],
        "description": "Sentence-Transformers 2.3+ requires PyTorch 1.11+, incompatible with older versions",
        "severity": "medium",
        "working_versions": {
            "sentence-transformers": ">=2.3.0",
            "torch": ">=1.11.0"
        },
        "fix": "pip install sentence-transformers>=2.3.0 torch>=1.11.0"
    },
    {
        "id": "haystack-transformers-version",
        "packages": ["farm-haystack", "transformers"],
        "description": "Haystack 1.x pins specific transformers versions, conflicts with newer releases",
        "severity": "high",
        "working_versions": {
            "farm-haystack": "1.22.0",
            "transformers": ">=4.34.0,<4.37.0"
        },
        "alternative": {
            "farm-haystack": ">=2.0.0",
            "transformers": ">=4.37.0"
        },
        "fix": "pip install farm-haystack==1.22.0 'transformers>=4.34.0,<4.37.0'\nOR upgrade both:\npip install farm-haystack>=2.0.0 transformers>=4.37.0"
    },
    {
        "id": "autogen-openai-version",
        "packages": ["pyautogen", "openai"],
        "description": "AutoGen <0.2.0 incompatible with OpenAI SDK 1.0+",
        "severity": "high",
        "working_versions": {
            "pyautogen": "0.1.14",
            "openai": "0.28.1"
        },
        "alternative": {
            "pyautogen": ">=0.2.0",
            "openai": ">=1.0.0"
        },
        "fix": "pip install pyautogen==0.1.14 openai==0.28.1\nOR upgrade both:\npip install pyautogen>=0.2.0 openai>=1.0.0"
    },
    {
        "id": "guidance-transformers-conflict",
        "packages": ["guidance", "transformers"],
        "description": "Microsoft Guidance 0.0.x has issues with transformers 4.35+ tokenizer changes",
        "severity": "medium",
        "working_versions": {
            "guidance": ">=0.1.0",
            "transformers": ">=4.35.0"
        },
        "fix": "pip install guidance>=0.1.0 transformers>=4.35.0"
    },
    {
        "id": "weaviate-grpc-protobuf",
        "packages": ["weaviate-client", "grpcio", "protobuf"],
        "description": "Weaviate client 3.x requires specific gRPC and protobuf versions",
        "severity": "medium",
        "working_versions": {
            "weaviate-client": ">=3.0.0",
            "grpcio": ">=1.50.0",
            "protobuf": ">=3.20.0,<5.0.0"
        },
        "fix": "pip install weaviate-client>=3.0.0 'grpcio>=1.50.0' 'protobuf>=3.20.0,<5.0.0'"
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
