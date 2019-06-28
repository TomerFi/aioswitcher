Code Documentation
******************

aioswitcher
^^^^^^^^^^^

.. automodule:: aioswitcher
    :undoc-members:

aioswitcher.consts
^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.consts
    :undoc-members:

aioswitcher.devices
^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.devices

    .. autoclass:: aioswitcher.devices.SwitcherV2Device

        .. automethod:: update_device_data(ip_address, name, state, remaining_time, auto_off_set, power_consumption, electric_current, last_state_change)
        
        .. automethod:: as_dict()

aioswitcher.errors
^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.errors

    .. autoexception:: aioswitcher.errors.CalculationError
        :show-inheritance:

    .. autoexception:: aioswitcher.errors.DecodingError
        :show-inheritance:

    .. autoexception:: aioswitcher.errors.EncodingError
        :show-inheritance:

aioswitcher.protocols
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.protocols

    .. autoclass:: aioswitcher.protocols.SwitcherV2UdpProtocolFactory
        :show-inheritance:

        .. automethod:: connection_made(transport)

        .. automethod:: datagram_received(data, addr)

        .. automethod:: error_received(exc)

        .. automethod:: connection_lost(exc)

        .. automethod:: close_transport(future)

        .. automethod:: handle_incoming_messeges(data, addr)

        .. automethod:: et_device_from_message(ip_addr, future)
