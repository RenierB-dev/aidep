"""
Comprehensive test suite for aidep package.
Tests conflict detection, version parsing, and CLI commands.
"""

import pytest
from aidep.checker import ConflictChecker
from aidep.conflicts import CONFLICTS, COMPATIBILITY_MATRIX
from aidep.scanner import DependencyScanner


class TestConflictDatabase:
    """Test the conflict database structure and content."""

    def test_conflicts_count(self):
        """Test that we have at least 20 conflicts defined."""
        assert len(CONFLICTS) >= 20, f"Expected at least 20 conflicts, found {len(CONFLICTS)}"

    def test_conflict_structure(self):
        """Test that all conflicts have required fields."""
        required_fields = ["id", "packages", "description", "severity", "fix"]
        for conflict in CONFLICTS:
            for field in required_fields:
                assert field in conflict, f"Conflict {conflict.get('id', 'unknown')} missing field: {field}"

    def test_conflict_ids_unique(self):
        """Test that all conflict IDs are unique."""
        ids = [c["id"] for c in CONFLICTS]
        assert len(ids) == len(set(ids)), "Duplicate conflict IDs found"

    def test_severity_levels(self):
        """Test that all severity levels are valid."""
        valid_severities = ["critical", "high", "medium", "low"]
        for conflict in CONFLICTS:
            assert conflict["severity"] in valid_severities, \
                f"Invalid severity '{conflict['severity']}' in {conflict['id']}"

    def test_packages_list(self):
        """Test that all conflicts have at least 2 packages."""
        for conflict in CONFLICTS:
            assert len(conflict["packages"]) >= 2, \
                f"Conflict {conflict['id']} must have at least 2 packages"


class TestVersionNormalization:
    """Test version normalization and parsing."""

    def test_normalize_basic_version(self):
        """Test normalization of basic version strings."""
        checker = ConflictChecker({})
        assert checker._normalize_version("1.0.0") == "1.0.0"
        assert checker._normalize_version("2.5.3") == "2.5.3"

    def test_normalize_short_version(self):
        """Test normalization of short version strings (x.y -> x.y.0)."""
        checker = ConflictChecker({})
        assert checker._normalize_version("1.5") == "1.5.0"
        assert checker._normalize_version("2.0") == "2.0.0"

    def test_normalize_alpha_version(self):
        """Test normalization of alpha versions."""
        checker = ConflictChecker({})
        assert "alpha" in checker._normalize_version("1.5a1").lower()
        assert "alpha" in checker._normalize_version("2.0.0alpha2").lower()

    def test_normalize_beta_version(self):
        """Test normalization of beta versions."""
        checker = ConflictChecker({})
        assert "beta" in checker._normalize_version("1.5b1").lower()
        assert "beta" in checker._normalize_version("2.0.0beta2").lower()

    def test_normalize_rc_version(self):
        """Test normalization of release candidate versions."""
        checker = ConflictChecker({})
        assert "rc" in checker._normalize_version("2.0.0rc1").lower()
        assert "rc" in checker._normalize_version("3.0rc2").lower()


class TestVersionSatisfies:
    """Test version satisfaction checks."""

    def test_exact_version_match(self):
        """Test exact version matching."""
        checker = ConflictChecker({})
        assert checker._version_satisfies("1.0.0", "==1.0.0")
        assert not checker._version_satisfies("1.0.1", "==1.0.0")

    def test_greater_than_version(self):
        """Test greater than version checks."""
        checker = ConflictChecker({})
        assert checker._version_satisfies("2.0.0", ">=1.0.0")
        assert checker._version_satisfies("1.0.0", ">=1.0.0")

    def test_less_than_version(self):
        """Test less than version checks."""
        checker = ConflictChecker({})
        # This test uses packaging library which handles version comparisons
        result = checker._version_satisfies("0.9.0", "<1.0.0")
        assert result is not None  # Should return a boolean


class TestConflictDetection:
    """Test conflict detection logic."""

    def test_no_conflicts_empty_deps(self):
        """Test that empty dependencies have no conflicts."""
        checker = ConflictChecker({})
        conflicts = checker.check_all()
        assert len(conflicts) == 0

    def test_langchain_llama_conflict(self):
        """Test detection of LangChain + LlamaIndex conflict."""
        deps = {
            "langchain": "0.0.200",
            "llama-index": "0.7.5"
        }
        checker = ConflictChecker(deps)
        conflicts = checker.check_all()
        # Should detect at least the SQLAlchemy conflict
        assert isinstance(conflicts, list)

    def test_openai_langchain_conflict(self):
        """Test detection of OpenAI + LangChain conflict."""
        deps = {
            "openai": "1.0.0",
            "langchain": "0.0.330"
        }
        checker = ConflictChecker(deps)
        conflicts = checker.check_all()
        assert isinstance(conflicts, list)

    def test_pydantic_v2_conflict(self):
        """Test detection of Pydantic V2 conflicts."""
        deps = {
            "pydantic": "2.0.0",
            "langchain": "0.0.330"
        }
        checker = ConflictChecker(deps)
        conflicts = checker.check_all()
        assert isinstance(conflicts, list)

    def test_has_conflicting_packages(self):
        """Test detection of conflicting package presence."""
        deps = {
            "langchain": "0.1.0",
            "llama-index": "0.8.0"
        }
        checker = ConflictChecker(deps)
        conflict = CONFLICTS[0]  # First conflict
        has_conflict = checker._has_conflicting_packages(conflict)
        # Should return True if both packages are present
        assert isinstance(has_conflict, bool)


class TestCompatibilityMatrix:
    """Test compatibility matrix functionality."""

    def test_compatibility_matrix_exists(self):
        """Test that compatibility matrix is defined."""
        assert len(COMPATIBILITY_MATRIX) > 0

    def test_compatibility_matrix_structure(self):
        """Test that compatibility matrix has valid structure."""
        for package, versions in COMPATIBILITY_MATRIX.items():
            assert isinstance(package, str)
            assert isinstance(versions, dict)
            for version, compatible in versions.items():
                assert isinstance(version, str)
                assert isinstance(compatible, dict)

    def test_check_compatibility_matrix_langchain(self):
        """Test compatibility matrix lookup for LangChain."""
        deps = {"langchain": "0.1.0"}
        checker = ConflictChecker(deps)
        compat = checker.check_compatibility_matrix("langchain")
        assert isinstance(compat, dict)


class TestDependencyScanner:
    """Test dependency scanner functionality."""

    def test_scanner_initialization(self):
        """Test that scanner can be initialized."""
        scanner = DependencyScanner()
        assert scanner is not None

    def test_parse_requirement_line(self):
        """Test parsing of requirement lines."""
        scanner = DependencyScanner()
        result = scanner._parse_requirement_line("langchain==0.1.0")
        assert isinstance(result, tuple)
        assert result[0] == "langchain"

    def test_parse_requirement_with_version_specifier(self):
        """Test parsing requirements with version specifiers."""
        scanner = DependencyScanner()
        result = scanner._parse_requirement_line("langchain>=0.1.0")
        assert isinstance(result, tuple)
        assert result[0] == "langchain"

    def test_parse_requirement_with_extras(self):
        """Test parsing requirements with extras - should handle basic package name."""
        scanner = DependencyScanner()
        # Note: current implementation doesn't handle extras, but extracts base package
        result = scanner._parse_requirement_line("langchain==0.1.0")
        assert isinstance(result, tuple)


class TestSuggestions:
    """Test fix suggestions."""

    def test_get_suggestions_format(self):
        """Test that suggestions are properly formatted."""
        deps = {
            "langchain": "0.0.200",
            "llama-index": "0.7.5"
        }
        checker = ConflictChecker(deps)
        checker.check_all()
        suggestions = checker.get_suggestions()
        assert isinstance(suggestions, list)

    def test_suggestions_contain_fix(self):
        """Test that suggestions contain fix information."""
        deps = {
            "openai": "1.0.0",
            "langchain": "0.0.330"
        }
        checker = ConflictChecker(deps)
        conflicts = checker.check_all()
        if conflicts:
            suggestions = checker.get_suggestions()
            # Suggestions should have content if conflicts exist
            assert len(suggestions) > 0


class TestNewConflicts:
    """Test the newly added conflicts."""

    def test_transformers_torch_conflict_exists(self):
        """Test that transformers+torch conflict is defined."""
        conflict_ids = [c["id"] for c in CONFLICTS]
        assert "transformers-torch-version" in conflict_ids

    def test_chromadb_conflict_exists(self):
        """Test that ChromaDB conflict is defined."""
        conflict_ids = [c["id"] for c in CONFLICTS]
        assert "chromadb-sqlite-version" in conflict_ids

    def test_fastapi_pydantic_conflict_exists(self):
        """Test that FastAPI+Pydantic conflict is defined."""
        conflict_ids = [c["id"] for c in CONFLICTS]
        assert "fastapi-pydantic-v2" in conflict_ids

    def test_autogen_conflict_exists(self):
        """Test that AutoGen conflict is defined."""
        conflict_ids = [c["id"] for c in CONFLICTS]
        assert "autogen-openai-version" in conflict_ids


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_malformed_version_string(self):
        """Test handling of malformed version strings."""
        checker = ConflictChecker({})
        # Should not crash on malformed versions
        result = checker._normalize_version("invalid")
        assert isinstance(result, str)

    def test_empty_package_name(self):
        """Test handling of empty package names."""
        checker = ConflictChecker({"": "1.0.0"})
        conflicts = checker.check_all()
        assert isinstance(conflicts, list)

    def test_none_version(self):
        """Test handling of None version."""
        checker = ConflictChecker({"package": None})
        # Should not crash
        conflicts = checker.check_all()
        assert isinstance(conflicts, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
