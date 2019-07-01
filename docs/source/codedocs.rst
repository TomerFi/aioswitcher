Code Documentation
******************

aioswitcher
^^^^^^^^^^^

.. automodule:: aioswitcher
    :undoc-members:

aioswitcher.api
^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.api

    .. autoclass:: aioswitcher.api.SwitcherV2Api
        :members: connected

        .. automethod:: __aenter__()

        .. automethod:: __await__()

        .. automethod:: __aexit__(exc_type, exc_value, traceback)

        .. automethod:: connect()

        .. automethod:: disconnect()

        .. automethod:: _full_login()

        .. automethod:: login()

        .. automethod:: _full_get_state()

        .. automethod:: get_state()

        .. automethod:: set_auto_shutdown(full_time)

        .. automethod:: set_device_name(name)

        .. automethod:: get_schedules()

        .. automethod:: disable_enable_schedule(schedule_data)

        .. automethod:: delete_schedule(schedule_id)

        .. automethod:: create_schedule(schedule_data)

aioswitcher.api.messages
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.api.messages

    .. autoclass:: aioswitcher.api.messages.ResponseMessageType
        :show-inheritance:
        :inherited-members:

    .. autoclass:: aioswitcher.api.messages.SwitcherV2BaseResponseMSG
        :members: unparsed_response, successful, msg_type

    .. autoclass:: aioswitcher.api.messages.SwitcherV2ControlResponseMSG
        :show-inheritance:
        :inherited-members:

    .. autoclass:: aioswitcher.api.messages.SwitcherV2CreateScheduleResponseMSG
        :show-inheritance:
        :inherited-members:

    .. autoclass:: aioswitcher.api.messages.SwitcherV2DeleteScheduleResponseMSG
        :show-inheritance:
        :inherited-members:

    .. autoclass:: aioswitcher.api.messages.SwitcherV2DisableEnableScheduleResponseMSG
        :show-inheritance:
        :inherited-members:

    .. autoclass:: aioswitcher.api.messages.SwitcherV2GetScheduleResponseMSG
        :show-inheritance:
        :inherited-members:
        :members: found_schedules, get_schedules

    .. autoclass:: aioswitcher.api.messages.SwitcherV2LoginResponseMSG
        :show-inheritance:
        :inherited-members:
        :members: session_id

    .. autoclass:: aioswitcher.api.messages.SwitcherV2SetAutoOffResponseMSG
        :show-inheritance:
        :inherited-members:

    .. autoclass:: aioswitcher.api.messages.SwitcherV2StateResponseMSG
        :show-inheritance:
        :inherited-members:
        :members: state, time_left, auto_off, power, current, init_future

        .. automethod:: initialize(response)

    .. autoclass:: aioswitcher.api.messages.SwitcherV2UpdateNameResponseMSG
        :show-inheritance:
        :inherited-members:

aioswitcher.api.packets
^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.api.packets
    :undoc-members:

aioswitcher.bridge
^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.bridge

    .. autoclass:: aioswitcher.bridge.SwitcherV2Bridge
        :members: running, queue

        .. automethod:: __aenter__()

        .. automethod:: __await__()

        .. automethod:: __aexit__(exc_type, exc_value, traceback)

        .. automethod:: start()

        .. automethod:: stop()

aioswitcher.bridge.messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.bridge.messages

    .. autoclass:: aioswitcher.bridge.messages.SwitcherV2BroadcastMSG
        :members: verified, ip_address, mac_address, name, device_id, power, device_state, remaining_time_to_off, current, auto_off_set, init_future

        .. automethod:: initialize(message)

aioswitcher.consts
^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.consts
    :undoc-members:

aioswitcher.devices
^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.devices

    .. autoclass:: aioswitcher.devices.SwitcherV2Device
        :members: device_id, ip_addr, mac_addr, name, state, remaining_time, auto_off_set, power_consumption, electric_current, phone_id, device_password, last_data_update, last_state_change

        .. automethod:: update_device_data(ip_address, name, state, remaining_time, auto_off_set, power_consumption, electric_current, last_state_change)

        .. automethod:: as_dict()

aioswitcher.errors
^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.errors

    .. autoexception:: aioswitcher.errors.CalculationError
        :show-inheritance:
        :inherited-members:

    .. autoexception:: aioswitcher.errors.DecodingError
        :show-inheritance:
        :inherited-members:

    .. autoexception:: aioswitcher.errors.EncodingError
        :show-inheritance:
        :inherited-members:

aioswitcher.protocols
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.protocols

    .. autoclass:: aioswitcher.protocols.SwitcherV2UdpProtocolFactory
        :show-inheritance:
        :inherited-members:
        :members: factory_future

        .. automethod:: connection_made(transport)

        .. automethod:: datagram_received(data, addr)

        .. automethod:: error_received(exc)

        .. automethod:: connection_lost(exc)

        .. automethod:: close_transport(future)

        .. automethod:: handle_incoming_messages(data, addr)

        .. automethod:: get_device_from_message(ip_addr, future)

aioswitcher.schedules
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.schedules

    .. autoclass:: aioswitcher.schedules.SwitcherV2Schedule
        :members: schedule_id, enabled, recurring, days, start_time, end_time, duration, schedule_data, init_future

        .. automethod:: initialize(idx, schedule_details)

        .. automethod:: as_dict()

    .. automethod:: aioswitcher.schedules._calc_next_run_for_schedule(schedule_details)

    .. automethod:: aioswitcher.schedules.calc_next_run_for_schedule(loop, schedule_details)

aioswitcher.tools
^^^^^^^^^^^^^^^^^

.. automodule:: aioswitcher.tools
    :members:
    :private-members:
