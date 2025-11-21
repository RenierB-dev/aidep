"""
Conflict detection module.
Checks dependencies against known conflict database.
"""

from typing import Dict, List, Tuple
from packaging.version import parse as parse_version, Version
from packaging.specifiers import SpecifierSet
import re

from .conflicts import CONFLICTS, COMPATIBILITY_MATRIX


class ConflictChecker:
    """Detects dependency conflicts in AI frameworks."""
    
    def __init__(self, dependencies: Dict[str, str]):
        self.dependencies = dependencies
        self.conflicts_found = []
        
    def check_all(self) -> List[Dict]:
        """Check all known conflicts."""
        for conflict in CONFLICTS:
            if self._has_conflicting_packages(conflict):
                conflict_result = self._evaluate_conflict(conflict)
                if conflict_result:
                    self.conflicts_found.append(conflict_result)
        
        return self.conflicts_found
    
    def _has_conflicting_packages(self, conflict: Dict) -> bool:
        """Check if project has the packages mentioned in conflict."""
        conflict_packages = set(pkg.lower() for pkg in conflict['packages'])
        project_packages = set(self.dependencies.keys())
        
        # Check if at least 2 of the conflicting packages are present
        overlap = conflict_packages & project_packages
        return len(overlap) >= 2
    
    def _evaluate_conflict(self, conflict: Dict) -> Dict:
        """Evaluate if this conflict applies to current versions."""
        affected_packages = {}
        
        for pkg_name in conflict['packages']:
            pkg_lower = pkg_name.lower()
            if pkg_lower in self.dependencies:
                affected_packages[pkg_name] = self.dependencies[pkg_lower]
        
        # Check if versions fall into conflict range
        is_conflicting = self._check_if_conflicting(
            affected_packages,
            conflict.get('working_versions', {}),
            conflict.get('alternative', {})
        )
        
        if is_conflicting:
            return {
                'id': conflict['id'],
                'description': conflict['description'],
                'severity': conflict['severity'],
                'affected_packages': affected_packages,
                'working_versions': conflict.get('working_versions', {}),
                'alternative': conflict.get('alternative', {}),
                'fix': conflict['fix']
            }
        
        return None
    
    def _check_if_conflicting(self, current: Dict[str, str], 
                             working: Dict[str, str], 
                             alternative: Dict[str, str]) -> bool:
        """
        Check if current versions are outside working versions.
        Returns True if there's a potential conflict.
        """
        # If no version specs provided, assume it might conflict
        if not current:
            return False
        
        # Simple heuristic: if we have version specs, check if they're
        # different from known working versions
        for pkg, spec in current.items():
            pkg_lower = pkg.lower()
            
            # Extract version number if present (including alpha/beta/rc)
            version_match = re.search(r'(\d+\.\d+\.\d+(?:[a-zA-Z]+\d*)?|\d+\.\d+)', spec)
            if not version_match:
                # No specific version pinned, might be okay
                continue

            current_version = self._normalize_version(version_match.group(1))
            
            # Check against working versions
            if pkg_lower in working:
                working_spec = working[pkg_lower]
                if not self._version_satisfies(current_version, working_spec):
                    # Check if it matches alternative
                    if pkg_lower in alternative:
                        alt_spec = alternative[pkg_lower]
                        if not self._version_satisfies(current_version, alt_spec):
                            return True
                    else:
                        return True
        
        return False
    
    def _normalize_version(self, version: str) -> str:
        """
        Normalize version string to handle alpha/beta/rc versions.
        Examples: 2.0.0rc1 -> 2.0.0-rc1, 1.5a1 -> 1.5.0-alpha1
        """
        # Handle short versions with suffixes (1.5a1 -> 1.5.0a1)
        short_with_suffix = re.match(r'^(\d+\.\d+)([a-zA-Z]+\d*)$', version)
        if short_with_suffix:
            base, suffix = short_with_suffix.groups()
            version = f"{base}.0{suffix}"

        # Handle short versions (1.5 -> 1.5.0)
        if re.match(r'^\d+\.\d+$', version):
            version = version + '.0'

        # Handle alpha/beta/rc suffixes
        # Match patterns like: 2.0.0rc1, 1.5.0a1, 3.0.0beta2
        match = re.match(r'^(\d+\.\d+\.\d+)([a-zA-Z]+)(\d*)$', version)
        if match:
            base, suffix, num = match.groups()
            # Normalize suffix to lowercase
            suffix_map = {
                'a': 'alpha', 'alpha': 'alpha',
                'b': 'beta', 'beta': 'beta',
                'rc': 'rc', 'c': 'rc',
            }
            normalized_suffix = suffix_map.get(suffix.lower(), suffix.lower())
            version = f"{base}-{normalized_suffix}{num}"

        return version

    def _version_satisfies(self, version: str, spec: str) -> bool:
        """Check if version satisfies specification."""
        try:
            version = self._normalize_version(version)

            # Handle exact version
            if '==' in spec:
                spec_version = self._normalize_version(spec.replace('==', '').strip())
                return version == spec_version

            # Handle version ranges using packaging library
            if '>=' in spec or '<' in spec or '>' in spec or '<=' in spec:
                try:
                    spec_set = SpecifierSet(spec)
                    # Try with and without normalization
                    version_obj = parse_version(version)
                    return version_obj in spec_set
                except Exception:
                    # Fallback to string comparison
                    return True

            # Handle x.x.x format
            if re.match(r'^\d+\.\d+', spec):
                return version.startswith(spec.split('.')[0])

            return True
        except Exception:
            return True
    
    def get_suggestions(self) -> List[str]:
        """Get fix suggestions for found conflicts."""
        suggestions = []
        
        for conflict in self.conflicts_found:
            suggestions.append(f"\n🔧 Fix for: {conflict['description']}")
            suggestions.append(f"Severity: {conflict['severity'].upper()}")
            suggestions.append(f"\n{conflict['fix']}")
        
        return suggestions
    
    def check_compatibility_matrix(self, package: str) -> Dict:
        """Check compatibility matrix for a specific package."""
        package_lower = package.lower()
        
        if package_lower not in COMPATIBILITY_MATRIX:
            return {}
        
        current_version = self.dependencies.get(package_lower, '')
        version_match = re.search(r'(\d+\.\d+)', current_version)
        
        if not version_match:
            return {}
        
        version = version_match.group(1)
        matrix = COMPATIBILITY_MATRIX[package_lower]
        
        # Find matching version range in matrix
        for version_range, compatible_packages in matrix.items():
            if self._version_in_range(version, version_range):
                return compatible_packages
        
        return {}
    
    def _version_in_range(self, version: str, version_range: str) -> bool:
        """Check if version is in range (e.g., '0.1.0' in '0.1.0+')."""
        try:
            # Handle x.x.x format
            if version_range.endswith('.x'):
                base = version_range[:-2]
                return version.startswith(base)
            
            # Handle x.x.x+ format
            if version_range.endswith('+'):
                base = version_range[:-1]
                ver = parse_version(version)
                base_ver = parse_version(base)
                return ver >= base_ver
            
            # Exact match
            return version == version_range
        except Exception:
            return False
