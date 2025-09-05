"""Agent Version Control System

Manages versioning of agent configurations, deployments, and rollback capabilities.
Provides semantic versioning, change tracking, and deployment history management.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class VersionType(str, Enum):
    """Version type indicators"""
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"


class ChangeType(str, Enum):
    """Types of changes in a version"""
    CONFIGURATION = "configuration"
    SPECIALIZATION = "specialization"
    DEPLOYMENT = "deployment"
    CREDENTIALS = "credentials"
    INSTRUCTIONS = "instructions"
    DEPENDENCIES = "dependencies"


class AgentVersion(BaseModel):
    """Represents a version of an agent configuration"""
    
    version: str = Field(..., description="Semantic version string (e.g., '1.2.3')")
    agent_id: str = Field(..., description="Agent identifier")
    
    # Version metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[str] = Field(None, description="User who created this version")
    description: Optional[str] = Field(None, description="Version description")
    
    # Configuration data
    config_data: Dict[str, Any] = Field(..., description="Complete agent configuration")
    config_hash: str = Field(..., description="Hash of configuration data")
    
    # Change tracking
    changes: List[ChangeType] = Field(default_factory=list, description="Types of changes in this version")
    previous_version: Optional[str] = Field(None, description="Previous version string")
    
    # Deployment tracking
    deployments: List[str] = Field(default_factory=list, description="Deployment IDs using this version")
    is_deployed: bool = Field(False, description="Whether this version is currently deployed")
    
    # Tags and labels
    tags: List[str] = Field(default_factory=list, description="Version tags")
    is_stable: bool = Field(False, description="Whether this is a stable release")
    is_prerelease: bool = Field(False, description="Whether this is a prerelease")
    
    class Config:
        use_enum_values = True


class VersionComparison(BaseModel):
    """Comparison between two versions"""
    
    from_version: str
    to_version: str
    changes: Dict[str, Any] = Field(default_factory=dict)
    added_fields: List[str] = Field(default_factory=list)
    removed_fields: List[str] = Field(default_factory=list)
    modified_fields: List[str] = Field(default_factory=list)
    change_summary: str = ""


class VersionManager:
    """Manages agent versions and provides version control capabilities"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.versions_dir = self.project_root / "versions"
        self.versions_dir.mkdir(exist_ok=True)
        
        # Version storage
        self.versions: Dict[str, Dict[str, AgentVersion]] = {}  # agent_id -> version -> AgentVersion
        
        # Load existing versions
        self._load_versions()
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists() or (parent / "langgraph.json").exists():
                return parent
        return Path.cwd()
    
    def _load_versions(self):
        """Load existing versions from disk"""
        for agent_dir in self.versions_dir.iterdir():
            if agent_dir.is_dir():
                agent_id = agent_dir.name
                self.versions[agent_id] = {}
                
                versions_file = agent_dir / "versions.json"
                if versions_file.exists():
                    try:
                        with open(versions_file, 'r') as f:
                            data = json.load(f)
                            for version_str, version_data in data.items():
                                self.versions[agent_id][version_str] = AgentVersion(**version_data)
                    except Exception as e:
                        logger.error(f"Failed to load versions for {agent_id}: {e}")
    
    def _save_versions(self, agent_id: str):
        """Save versions for a specific agent"""
        agent_dir = self.versions_dir / agent_id
        agent_dir.mkdir(exist_ok=True)
        
        versions_file = agent_dir / "versions.json"
        try:
            data = {
                version_str: version.dict()
                for version_str, version in self.versions.get(agent_id, {}).items()
            }
            with open(versions_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save versions for {agent_id}: {e}")
    
    def _calculate_config_hash(self, config_data: Dict[str, Any]) -> str:
        """Calculate hash of configuration data"""
        # Sort keys for consistent hashing
        config_str = json.dumps(config_data, sort_keys=True, default=str)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]
    
    def _parse_version(self, version: str) -> tuple[int, int, int, str]:
        """Parse semantic version string"""
        parts = version.split('-', 1)
        version_part = parts[0]
        prerelease = parts[1] if len(parts) > 1 else ""
        
        version_numbers = version_part.split('.')
        major = int(version_numbers[0]) if len(version_numbers) > 0 else 0
        minor = int(version_numbers[1]) if len(version_numbers) > 1 else 0
        patch = int(version_numbers[2]) if len(version_numbers) > 2 else 0
        
        return major, minor, patch, prerelease
    
    def _increment_version(self, current_version: str, version_type: VersionType) -> str:
        """Increment version based on type"""
        major, minor, patch, prerelease = self._parse_version(current_version)
        
        if version_type == VersionType.MAJOR:
            return f"{major + 1}.0.0"
        elif version_type == VersionType.MINOR:
            return f"{major}.{minor + 1}.0"
        elif version_type == VersionType.PATCH:
            return f"{major}.{minor}.{patch + 1}"
        elif version_type == VersionType.PRERELEASE:
            if prerelease:
                # Increment prerelease number
                if prerelease.startswith("alpha"):
                    num = int(prerelease.replace("alpha", "") or "0")
                    return f"{major}.{minor}.{patch}-alpha{num + 1}"
                elif prerelease.startswith("beta"):
                    num = int(prerelease.replace("beta", "") or "0")
                    return f"{major}.{minor}.{patch}-beta{num + 1}"
                else:
                    return f"{major}.{minor}.{patch}-alpha1"
            else:
                return f"{major}.{minor}.{patch}-alpha1"
        
        return current_version
    
    def _detect_changes(self, old_config: Dict[str, Any], new_config: Dict[str, Any]) -> List[ChangeType]:
        """Detect types of changes between configurations"""
        changes = []
        
        # Check for specialization changes
        if old_config.get("specialization") != new_config.get("specialization"):
            changes.append(ChangeType.SPECIALIZATION)
        
        # Check for instruction changes
        old_instructions = old_config.get("custom_instructions", "")
        new_instructions = new_config.get("custom_instructions", "")
        if old_instructions != new_instructions:
            changes.append(ChangeType.INSTRUCTIONS)
        
        # Check for credential changes
        old_creds = old_config.get("configuration", {}).get("credential_id")
        new_creds = new_config.get("configuration", {}).get("credential_id")
        if old_creds != new_creds:
            changes.append(ChangeType.CREDENTIALS)
        
        # Check for deployment configuration changes
        old_deploy = old_config.get("deployment_config", {})
        new_deploy = new_config.get("deployment_config", {})
        if old_deploy != new_deploy:
            changes.append(ChangeType.DEPLOYMENT)
        
        # Check for other configuration changes
        config_keys = set(old_config.keys()) | set(new_config.keys())
        config_keys -= {"custom_instructions", "specialization", "configuration", "deployment_config"}
        
        for key in config_keys:
            if old_config.get(key) != new_config.get(key):
                changes.append(ChangeType.CONFIGURATION)
                break
        
        return changes
    
    def _suggest_version_type(self, changes: List[ChangeType]) -> VersionType:
        """Suggest version increment type based on changes"""
        if ChangeType.SPECIALIZATION in changes:
            return VersionType.MINOR
        elif ChangeType.INSTRUCTIONS in changes or ChangeType.CONFIGURATION in changes:
            return VersionType.MINOR
        elif ChangeType.CREDENTIALS in changes or ChangeType.DEPLOYMENT in changes:
            return VersionType.PATCH
        else:
            return VersionType.PATCH
    
    async def create_version(self, 
                           agent_id: str, 
                           config_data: Dict[str, Any],
                           description: Optional[str] = None,
                           version_type: Optional[VersionType] = None,
                           created_by: Optional[str] = None,
                           tags: Optional[List[str]] = None) -> AgentVersion:
        """Create a new version of an agent configuration"""
        
        # Initialize agent versions if not exists
        if agent_id not in self.versions:
            self.versions[agent_id] = {}
        
        # Calculate configuration hash
        config_hash = self._calculate_config_hash(config_data)
        
        # Check if this exact configuration already exists
        for existing_version in self.versions[agent_id].values():
            if existing_version.config_hash == config_hash:
                logger.info(f"Configuration already exists as version {existing_version.version}")
                return existing_version
        
        # Determine version number
        current_versions = list(self.versions[agent_id].keys())
        if not current_versions:
            # First version
            version_str = "1.0.0"
            previous_version = None
            changes = [ChangeType.CONFIGURATION]
        else:
            # Get latest version
            latest_version = max(current_versions, key=lambda v: self._parse_version(v))
            latest_config = self.versions[agent_id][latest_version].config_data
            
            # Detect changes
            changes = self._detect_changes(latest_config, config_data)
            
            # Determine version increment
            if version_type is None:
                version_type = self._suggest_version_type(changes)
            
            version_str = self._increment_version(latest_version, version_type)
            previous_version = latest_version
        
        # Create version object
        version = AgentVersion(
            version=version_str,
            agent_id=agent_id,
            description=description,
            config_data=config_data,
            config_hash=config_hash,
            changes=changes,
            previous_version=previous_version,
            created_by=created_by,
            tags=tags or [],
            is_prerelease=version_type == VersionType.PRERELEASE
        )
        
        # Store version
        self.versions[agent_id][version_str] = version
        self._save_versions(agent_id)
        
        logger.info(f"Created version {version_str} for agent {agent_id}")
        return version
    
    def get_version(self, agent_id: str, version: str) -> Optional[AgentVersion]:
        """Get a specific version of an agent"""
        return self.versions.get(agent_id, {}).get(version)
    
    def get_latest_version(self, agent_id: str) -> Optional[AgentVersion]:
        """Get the latest version of an agent"""
        if agent_id not in self.versions or not self.versions[agent_id]:
            return None
        
        versions = list(self.versions[agent_id].keys())
        latest_version = max(versions, key=lambda v: self._parse_version(v))
        return self.versions[agent_id][latest_version]
    
    def list_versions(self, agent_id: str, include_prerelease: bool = True) -> List[AgentVersion]:
        """List all versions of an agent"""
        if agent_id not in self.versions:
            return []
        
        versions = list(self.versions[agent_id].values())
        
        if not include_prerelease:
            versions = [v for v in versions if not v.is_prerelease]
        
        # Sort by version (newest first)
        versions.sort(key=lambda v: self._parse_version(v.version), reverse=True)
        return versions
    
    def compare_versions(self, agent_id: str, from_version: str, to_version: str) -> VersionComparison:
        """Compare two versions of an agent"""
        from_ver = self.get_version(agent_id, from_version)
        to_ver = self.get_version(agent_id, to_version)
        
        if not from_ver or not to_ver:
            raise ValueError("One or both versions not found")
        
        from_config = from_ver.config_data
        to_config = to_ver.config_data
        
        # Find differences
        all_keys = set(from_config.keys()) | set(to_config.keys())
        added_fields = []
        removed_fields = []
        modified_fields = []
        changes = {}
        
        for key in all_keys:
            if key not in from_config:
                added_fields.append(key)
                changes[key] = {"added": to_config[key]}
            elif key not in to_config:
                removed_fields.append(key)
                changes[key] = {"removed": from_config[key]}
            elif from_config[key] != to_config[key]:
                modified_fields.append(key)
                changes[key] = {
                    "from": from_config[key],
                    "to": to_config[key]
                }
        
        # Generate summary
        summary_parts = []
        if added_fields:
            summary_parts.append(f"Added {len(added_fields)} field(s)")
        if removed_fields:
            summary_parts.append(f"Removed {len(removed_fields)} field(s)")
        if modified_fields:
            summary_parts.append(f"Modified {len(modified_fields)} field(s)")
        
        change_summary = ", ".join(summary_parts) if summary_parts else "No changes"
        
        return VersionComparison(
            from_version=from_version,
            to_version=to_version,
            changes=changes,
            added_fields=added_fields,
            removed_fields=removed_fields,
            modified_fields=modified_fields,
            change_summary=change_summary
        )
    
    def tag_version(self, agent_id: str, version: str, tag: str) -> bool:
        """Add a tag to a version"""
        ver = self.get_version(agent_id, version)
        if not ver:
            return False
        
        if tag not in ver.tags:
            ver.tags.append(tag)
            self._save_versions(agent_id)
        
        return True
    
    def mark_stable(self, agent_id: str, version: str) -> bool:
        """Mark a version as stable"""
        ver = self.get_version(agent_id, version)
        if not ver:
            return False
        
        ver.is_stable = True
        ver.is_prerelease = False
        self._save_versions(agent_id)
        return True
    
    def get_stable_versions(self, agent_id: str) -> List[AgentVersion]:
        """Get all stable versions of an agent"""
        versions = self.list_versions(agent_id, include_prerelease=False)
        return [v for v in versions if v.is_stable]
    
    def rollback_to_version(self, agent_id: str, target_version: str) -> Optional[AgentVersion]:
        """Create a rollback version based on a previous version"""
        target_ver = self.get_version(agent_id, target_version)
        if not target_ver:
            return None
        
        # Create new version with rollback configuration
        rollback_config = target_ver.config_data.copy()
        rollback_config["_rollback_from"] = target_version
        
        return await self.create_version(
            agent_id=agent_id,
            config_data=rollback_config,
            description=f"Rollback to version {target_version}",
            version_type=VersionType.PATCH,
            tags=["rollback"]
        )
    
    def get_version_history(self, agent_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get version history with change information"""
        versions = self.list_versions(agent_id)
        
        if limit:
            versions = versions[:limit]
        
        history = []
        for i, version in enumerate(versions):
            entry = {
                "version": version.version,
                "created_at": version.created_at,
                "description": version.description,
                "changes": version.changes,
                "is_stable": version.is_stable,
                "is_prerelease": version.is_prerelease,
                "tags": version.tags,
                "deployments": len(version.deployments)
            }
            
            # Add comparison with previous version
            if i < len(versions) - 1:
                prev_version = versions[i + 1]
                try:
                    comparison = self.compare_versions(
                        agent_id, prev_version.version, version.version
                    )
                    entry["changes_summary"] = comparison.change_summary
                except:
                    entry["changes_summary"] = "Unable to compare"
            
            history.append(entry)
        
        return history
    
    def cleanup_old_versions(self, agent_id: str, keep_count: int = 10, keep_stable: bool = True):
        """Clean up old versions, keeping only the most recent ones"""
        versions = self.list_versions(agent_id)
        
        if len(versions) <= keep_count:
            return
        
        # Sort versions (oldest first for deletion)
        versions.sort(key=lambda v: self._parse_version(v.version))
        
        to_delete = []
        kept_count = 0
        
        # Keep stable versions if requested
        if keep_stable:
            for version in reversed(versions):
                if version.is_stable or kept_count < keep_count:
                    kept_count += 1
                else:
                    to_delete.append(version.version)
        else:
            # Keep only the most recent versions
            for version in versions[:-keep_count]:
                to_delete.append(version.version)
        
        # Delete old versions
        for version_str in to_delete:
            if version_str in self.versions[agent_id]:
                del self.versions[agent_id][version_str]
                logger.info(f"Deleted old version {version_str} for agent {agent_id}")
        
        if to_delete:
            self._save_versions(agent_id)
    
    def export_version(self, agent_id: str, version: str, export_path: Path) -> bool:
        """Export a version configuration to a file"""
        ver = self.get_version(agent_id, version)
        if not ver:
            return False
        
        try:
            export_data = {
                "agent_id": agent_id,
                "version": ver.version,
                "created_at": ver.created_at.isoformat(),
                "description": ver.description,
                "config_data": ver.config_data,
                "tags": ver.tags,
                "is_stable": ver.is_stable
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            return True
        except Exception as e:
            logger.error(f"Failed to export version {version}: {e}")
            return False
    
    def import_version(self, import_path: Path) -> Optional[AgentVersion]:
        """Import a version configuration from a file"""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            
            return await self.create_version(
                agent_id=data["agent_id"],
                config_data=data["config_data"],
                description=data.get("description"),
                tags=data.get("tags", [])
            )
        except Exception as e:
            logger.error(f"Failed to import version from {import_path}: {e}")
            return None
