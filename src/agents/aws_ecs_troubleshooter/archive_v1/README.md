# Archived v1 Implementation

**Archived Date**: 2025-09-23  
**Reason**: Migrated to v2 implementation using deep-agents patterns  

## Archived Files

### agent.py
- Original agent implementation
- Used gather_planton_context from context_tools
- Replaced by: `agent_v2.py`

### instructions.py
- Original instruction constants and prompts
- Constants moved to: `instructions_v2.py`
- Replaced by: `instructions_v2.py`

### context_tools.py
- Original context gathering implementation
- Used Planton Cloud API directly
- Replaced by: MCP wrappers in `tools/mcp_wrappers/`

### graph.py
- Original graph implementation
- Used traditional LangGraph patterns
- Replaced by: `graph_v2.py` (now promoted to `graph.py`)

## Migration Notes

The v2 implementation improves on v1 by:
1. Using file-based MCP wrappers for better observability
2. LLM-driven tool selection in context phase
3. More modular sub-agent architecture
4. Better separation of concerns

## References

- New implementation: `agent_v2.py`, `instructions_v2.py`, `graph_v2.py`
- Migration guide: `docs/deep_agents_migration.md`
- Context sub-agent architecture: `docs/context_subagent_architecture.md`
