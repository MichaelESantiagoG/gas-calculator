# Gas Calculator Enhancement Plan

## Current Baseline
- Single-file Streamlit app with core fill-up calculation in [`main.py`](/Users/michaelsantiago/Documents/GitHub/gas-calculator/main.py).
- Config syntax issue in [`config.toml`](/Users/michaelsantiago/Documents/GitHub/gas-calculator/config.toml) (unterminated quote on line 2).
- Missing `streamlit` dependency in [`requirements.txt`](/Users/michaelsantiago/Documents/GitHub/gas-calculator/requirements.txt).
- No tests, linting, formatting, or CI.

## Goals
1. Improve correctness and reliability.
2. Improve user experience and clarity of inputs/outputs.
3. Make the app maintainable with tests, structure, and automation.
4. Prepare for lightweight production deployment and monitoring.

## Phase 1: Stability and Correctness (High Impact, Low Effort)
### Scope
- Fix `config.toml` parsing issue.
- Add missing runtime dependencies (`streamlit`, optionally pin versions).
- Add input validation and guardrails:
  - `price > 0`
  - `tank_capacity > 0`
  - `current_gas_level <= tank_capacity`
- Normalize unit handling with explicit conversion helpers.
- Improve numeric formatting for currency and volumes.

### Deliverables
- App starts cleanly with `streamlit run main.py`.
- Invalid inputs are blocked or produce clear inline error messages.
- Results are consistently formatted (e.g., `$32.45`, `6.2 gal`).

### Acceptance Criteria
- No runtime errors with typical user flows.
- Config loads without TOML parse errors.
- Fresh install from `requirements.txt` can run app successfully.

## Phase 2: Product UX Improvements (High Impact, Medium Effort)
### Scope
- Support full unit system toggle:
  - US (`gallon`, `mpg`)
  - Metric (`liter`, `L/100km` optional future)
- Add additional outputs:
  - Cost to fill from current level
  - Cost per quarter/half/full tank
  - Distance estimate based on efficiency input
- Improve visual design and readability:
  - clearer labels/help text
  - better chart colors and thresholds (low/medium/high fuel)
  - mobile-friendly layout tuning
- Add “saved presets” for common vehicle tank sizes.

### Deliverables
- Expanded calculator with unit-aware outputs.
- Improved gauge or progress visualization with thresholds.
- Preset selector and reset-to-default action.

### Acceptance Criteria
- Users can complete calculations in either unit system without ambiguity.
- UI remains usable on phone-width screens.
- Output labels are understandable without technical knowledge.

## Phase 3: Code Quality and Maintainability (Medium Impact, Medium Effort)
### Scope
- Refactor app logic into modules:
  - `calculator.py` for business logic
  - `ui.py` (or keep Streamlit views in `main.py` and call pure functions)
- Add unit tests for conversions and cost calculations (`pytest`).
- Add lint/format tooling (`ruff`, `black`) and pre-commit hooks.
- Add basic app-level smoke test.

### Deliverables
- Separated pure functions with test coverage.
- CI workflow for lint + tests on pull requests.

### Acceptance Criteria
- Unit tests cover core formula paths and edge cases.
- CI passes on clean checkout.
- No duplicated calculation logic between UI and backend functions.

## Phase 4: Deployment and Observability (Optional, Medium Effort)
### Scope
- Standardize deployment configuration.
- Add basic telemetry/logging for app failures.
- Add lightweight analytics events for key actions (input changes, calculate).
- Add release notes/versioning strategy.

### Deliverables
- Repeatable deploy process and environment documentation.
- Error visibility for production debugging.

### Acceptance Criteria
- Deployment can be reproduced from documentation.
- Runtime errors are traceable with logs.

## Suggested Execution Order (2-Week Version)
1. Days 1-2: Phase 1 fixes and validation.
2. Days 3-5: Phase 2 UX enhancements.
3. Days 6-8: Refactor + tests.
4. Days 9-10: CI + deployment hardening.

## Risks and Mitigations
- Scope creep on new calculator features.
  - Mitigation: lock Phase 2 to two or three user-visible improvements.
- Unit confusion between liter/gallon calculations.
  - Mitigation: centralize conversion constants and test them.
- Breakage during refactor.
  - Mitigation: add tests before moving logic.

## Immediate Next Actions
1. Fix TOML and dependency issues.
2. Add pure calculation helpers and tests.
3. Ship one UX improvement batch (units + formatting + thresholds).
