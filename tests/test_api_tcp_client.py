# Copyright Tomer Figenblat.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Switcher unofficial integration TCP socket API module test cases."""

from asyncio import get_event_loop, open_connection, start_server

from assertpy import assert_that
from pytest import fixture, mark

pytestmark = mark.asyncio


async def tcp_server_cb(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    writer.write(message[::-1].encode())
    writer.close()
    await writer.wait_closed()


@fixture(scope="module")
def tcp_port(unused_tcp_port_factory):
    return unused_tcp_port_factory()


@fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop
    loop.close()


@fixture(autouse=True, scope="module")
async def tcp_server(tcp_port):
    server = await start_server(tcp_server_cb, "127.0.0.1", tcp_port)
    await server.start_serving()
    yield
    server.close()
    await server.wait_closed()


@fixture
async def tcp_client(tcp_port):
    reader, writer = await open_connection("127.0.0.1", tcp_port)
    yield reader, writer
    writer.close()
    await writer.wait_closed()


async def test_ttt(tcp_client):
    tcp_client[1].write("message".encode())
    response = await tcp_client[0].read(1024)
    assert_that(response.decode()).is_equal_to("egassem")
