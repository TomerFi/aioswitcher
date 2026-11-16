Use the Bridge to discover devices and their state. The following excerpt will print all discovered devices for 60 seconds.

```python linenums="1" hl_lines="9"
import asyncio
from dataclasses import asdict
from aioswitcher.bridge import SwitcherBridge


async def print_devices(delay):
    def on_device_found_callback(device):
        print(asdict(device))  # (1)

    async with SwitcherBridge(on_device_found_callback):
        await asyncio.sleep(delay)


asyncio.run(print_devices(60))
```

1. for the callback types, check the device pacakge for implementations of
    [SwitcherBase](./codedocs.md#src.aioswitcher.device.SwitcherBase).

!!!note
    Switcher devices broadcast a state message approximately every 4 seconds.

## Discovery behind NAT

By default, the bridge uses each UDP packet's source IP. This handles devices
whose broadcast payload retains an old IP after a DHCP lease change.

If a container runtime or UDP relay rewrites the sender to a gateway address
(for example, Home Assistant running in OrbStack), use the address embedded in
the device's broadcast instead:

```python
async with SwitcherBridge(
    on_device_found_callback, broadcast_ip_network="192.168.0.0/24"
):
    await asyncio.sleep(60)
```

Only embedded addresses within the allowed network are accepted. This discovers
the device address without a fixed-IP override. Use it only when
the sender is rewritten: the embedded address can be stale after DHCP changes
until the device is restarted. Applications embedding this library must expose
or pass this option; it is not a Home Assistant configuration option by itself.
