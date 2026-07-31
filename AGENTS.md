# AGENTS.md — aioswitcher

## Project

aioswitcher is a Python 3.12+ async library for integrating with Switcher smart switches and outlets (power plugs, wall switches, curtain motor controllers, thermostat controllers, water heater controllers). It uses `uv` for dependency management and `pytest` with strict asyncio mode for testing.

## AI Policy

This project has an [AI policy](AI_POLICY.md). Always read it and ensure all suggestions, code, and contributions comply. If any behavior seems to conflict with the policy, warn the user and ask for guidance.

## Client Projects

aioswitcher is a dependency for two major projects — always consider them when making changes, especially breaking ones.

1. **Home Assistant ([switcher_kis integration](https://www.home-assistant.io/integrations/switcher_kis/))** — the primary client. It uses the Bridge for device discovery and the API for control. The integration is tightly coupled to this library's device dataclasses, state responses, and error semantics.
   - [GitHub source](https://github.com/home-assistant/core/tree/dev/homeassistant/components/switcher_kis)
2. **[switcher_webapi](https://switcher-webapi.figenblat.com/)** — a containerized REST API wrapper that exposes device control (TCP only) as HTTP endpoints. It enables non-Python users and systems to control Switcher devices without the UDP discovery layer. This client depends on `SwitcherApi` and the message/response types.
   - [GitHub source](https://github.com/TomerFi/switcher_webapi)

When making API changes or renaming things, check if they impact these consumers. Do not break the public interface without coordinating with both clients.

## Repo Structure

```text
src/aioswitcher/
  __init__.py          # package entry, exports api, bridge, device, schedule
  bridge.py            # UDP broadcast discovery — SwitcherBridge + DatagramParser
  api/
    __init__.py        # SwitcherApi — TCP socket-based device control
    messages.py        # Response parsers (login, state, schedules)
    packets.py         # Binary protocol packet templates (hex strings)
    remotes.py         # Breeze IR remote database and command builders
  device/
    __init__.py        # DeviceType enum, all dataclasses (SwitcherPowerPlug, etc.)
    tools.py           # Helpers: hex encoding, CRC signing, timestamp, watts→amps
  schedule/
    __init__.py        # Days enum, ScheduleState enum
    parser.py          # Schedule data parser
    tools.py           # Time/weekday helpers
tests/                 # pytest suite (strict asyncio mode)
scripts/               # CLI helper scripts (discover, control, validate_token, get_login_key)
docs/                  # mkdocs documentation
```

## Scripts

CLI tools available only from the repository — they are not bundled with the `aioswitcher` PyPI package. **The `aioswitcher` package must be installed on the machine where you run them.**

These scripts expose command-line interfaces for operations the library implements (device control, discovery) and for operations outside the library (fetching login keys from devices, validating cloud tokens).

Files:
- `discover_devices.py` — runs the Bridge and prints discovered devices (JSON via `dataclasses.asdict`). No code changes needed for new devices.
- `control_device.py` — large `argparse` subcommand-based CLI (~1100 lines). The `DEVICES` dict maps human-readable names to `DeviceType` enum members. Each action has an argparser subcommand + a named async function + a dispatch case in `main()`. Token-based methods get a `-k` flag. New API methods need new subparsers, async functions, and dispatch cases. New device types need a `DEVICES` entry.
- `get_device_login_key.py` — pings a device's UDP broadcast port to extract its login key.
- `validate_token.py` — validates a Switcher cloud token via the device API.

## Protocol Types

- **Type 1** (water heaters, power plug): port **9957** (TCP), UDP port **20002/10002**. No token required.
- **Type 2** (breeze, runners, heater): port **10000** (TCP), UDP port **20003/10003**. Breeze/runners may require a token.

## Architecture

### Discovery (UDP)
1. `SwitcherBridge` opens UDP sockets on all broadcast ports.
2. `UdpClientProtocol.datagram_received` receives raw bytes, passes to `DatagramParser`.
3. `DatagramParser` extracts device type from hex bytes at offset 74–76.
4. `_parse_device_from_datagram` routes to device-specific branch by `DeviceCategory`, builds dataclass, calls `on_device` callback.

### Control (TCP)
1. `SwitcherApi` connects via `open_connection()` → `_reader`/`_writer`.
2. Every command starts with `_login()` (Type1: 1 round-trip, Type2 token: 2 round-trips).
3. Build packet string from `packets.py` templates → `_send_packet()` signs with CRC key → sends → reads 1024 bytes.
4. Response bytes parsed via response classes in `messages.py`.

## Adding a New Device Type

When a new device type is announced, changes span ~8 files:

1. **`device/__init__.py`**: Add enum member to `DeviceType` (hex representation, protocol type, category, token_needed). If it has unique fields, add a new base dataclass (e.g., `SwitcherLightBase`) and the concrete class (e.g., `SwitcherLight`) with `__post_init__` validation.
2. **`bridge.py`**: Add a branch in `_parse_device_from_datagram` for the new category/type, instantiate the dataclass, wire `DatagramParser` helpers if needed.
3. **`api/__init__.py`**: Add state retrieval and control methods. If the device type is token-based, handle the login2 flow and `GENERAL_TOKEN_COMMAND` packet pattern. If it has new commands, add packet constants to `packets.py`.
4. **`api/packets.py`**: Add new packet templates if the device uses commands not covered by existing templates.
5. **`docs/supported.md`**: Add a row to the supported devices table with name, product link, minimum version, and token requirement. Update device links section.
6. **`docs/usage_api.md`**: Add a code excerpt showing how to control the new device (state, on/off, any device-specific commands).
7. **`scripts/control_device.py`**: Add the new device name to `DEVICES` dict. Add argparser subcommand(s) for each new action (state retrieval, control). Add async function(s) that call the new API methods. Add dispatch case in `main()`.
8. **`tests/`**:
   - `test_device_dataclasses.py` — test instantiation and validation errors.
   - `test_device_enum_helpers.py` — parametrize with new enum members.
   - `test_device_parsing.py` — parse datagram for the new device.
   - `test_api_tcp_client.py` — mock TCP reads/writes for new API methods.

Note: `discover_devices.py` needs no changes — the Bridge auto-discovers all broadcasted devices.

## Testing Patterns

- `pytestmark = mark.asyncio` at module level for async tests.
- Use `@pytest_asyncio.fixture` for connected API instances (connects, yields, disconnects).
- Use `assertpy` (`assert_that(...)`), NOT `pytest` assertions.
- Mock `aioswitcher.api.open_connection` with `AsyncMock` for `StreamReader`/`StreamWriter`.
- Test fixture data is in `FakeData` dataclass at top of `test_device_dataclasses.py`.
- Binary responses are loaded from `tests/testresources/dummy_responses/*.txt` via `resource_path_root` fixture.
- Parametrize enum tests with all members.
- Every API test verifies: `writer_write.call_count`, response type, and `unparsed_response`.

## Tooling Commands

```shell
uv sync --all-groups                          # setup
uv run pytest                                 # all tests
uv run black --check src/ docs/ scripts/
uv run flake8 src/ tests/ docs/ scripts/
uv run isort --check-only src/ tests/ docs/ scripts/
uv run mypy src/ scripts/
uv run yamllint --format colored --strict .
uv run mkdocs build                           # docs
```

## Prek Hooks

Hook repos are pinned to commit SHAs. Dependabot handles regular updates automatically with a weekly cadence. For manual updates, use `uv run prek update --freeze`. **Always use `--freeze`** — without it, prek update replaces SHAs with tags. `additional_dependencies` are pinned with exact versions and must be updated manually in the config file. The agent should check if hooks are installed (`.git/hooks/pre-commit`) and remind the user to install them if not.

## Documentation (mkdocs)

Docs live in `docs/`, built with mkdocs-material (Material theme + mkdocstrings for auto API docs). Deployed to `aioswitcher.figenblat.com` via GitHub Pages on release.

Build: `uv sync --group docs && uv run mkdocs build --strict`

Structure:
- `index.md` — root page, includes other docs via markdown includes (`--8<--`)
- `install.md` — pip install line
- `usage_bridge.md` — UDP discovery code example
- `usage_api.md` — device control code examples per device type
- `supported.md` — table of supported devices (name, product link, min version, token) + product links section at bottom
- `codedocs.md` — mkdocstrings `:::` directives (auto-generated API docs on build)
- `scripts.md` — CLI helper scripts with `--help` output and examples

When adding a new device type, always update `supported.md` (table row + product link), `usage_api.md` (code excerpt), `usage_bridge.md` (output examples), and `scripts.md` (new subcommand examples). Do not break `--strict` mode — all markdown must be valid.

## Conventions

- Docstrings on ALL public functions and classes (project has ~100% coverage).
- Apache 2.0 license header on every file.
- `final` decorator on dataclasses and concrete classes that should not be subclassed.
- Custom enum members use `__new__` with extra properties (`.value`, `.display`, `.hex_rep`, etc.).
- Type annotations everywhere, mypy strict mode.
- Comments explain hex packet structure, not why code exists.
- Variable names: `sut` for system under test in tests.
