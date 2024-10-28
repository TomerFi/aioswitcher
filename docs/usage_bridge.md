Use the Bridge to discover devices and their state. The following excerpt will print all discovered devices for 60 seconds.

```python linenums="1" hl_lines="9"
import asyncio
from dataclasses import asdict
from aioswitcher.bridge import SwitcherBridge

async def print_devices(delay):
    def on_device_found_callback(device):
        print(asdict(device)) # (1)

    async with SwitcherBridge(on_device_found_callback):
        await asyncio.sleep(delay)

asyncio.run(print_devices(60))
```

1. for the callback types, check the device pacakge for implementations of
    [SwitcherBase](./codedocs.md#src.aioswitcher.device.SwitcherBase).

!!!note
    Switcher devices broadcast a state message approximately every 4 seconds.
