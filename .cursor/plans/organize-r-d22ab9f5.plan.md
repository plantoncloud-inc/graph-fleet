<!-- d22ab9f5-e3c4-43d2-97eb-acc2c21f682e e4c2ec0f-c63f-4541-a2f5-c726f5fcad40 -->
# Organize RDS Manifest Generator Documentation

## Overview

Move all documentation markdown files and the examples folder from `src/agents/rds_manifest_generator/` into a new `docs/` subdirectory to improve organization and reduce file count in the main agent directory.

## File Structure Changes

### Create new directory

- `src/agents/rds_manifest_generator/docs/`

### Files to move into docs/

1. `DEMO_SCENARIOS.md`
2. `DEVELOPER_GUIDE.md`
3. `INTEGRATION.md`
4. `PHASE1_COMPLETE.md`
5. `PHASE2_COMPLETE.md`
6. `PHASE2_SUMMARY.md`
7. `PHASE3_COMPLETE.md`
8. `PHASE4_COMPLETE.md`
9. `QUICKSTART.md`
10. `README.md`
11. `USER_GUIDE.md`
12. `examples/` (entire directory with all YAML files)

### Files to keep at root

- `__init__.py`
- `agent.py`
- `graph.py`
- `state.py`
- `schema/` (directory)
- `tools/` (directory)

## Result

After reorganization, the `rds_manifest_generator` directory will have:

- Core Python files at the root level
- All documentation consolidated in `docs/` subdirectory
- Cleaner, more maintainable directory structure

### To-dos

- [ ] Create docs/ directory inside rds_manifest_generator
- [ ] Move all 11 markdown documentation files to docs/
- [ ] Move examples/ directory to docs/examples/