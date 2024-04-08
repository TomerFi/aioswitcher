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
# flake8: noqa

"""Switcher convert token to valid packet string. Input: Token (String), Output: Packet value (String)"""

from base64 import b64decode
from binascii import hexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

secret_key = b"jzNrAOjc%lpg3pVr5cF!5Le06ZgOdWuJ"


def he(token: str | None) -> str:
    if token is None:
        raise RuntimeError("received None token as input")
    encrypted_value = b64decode(bytes(token, "utf-8"))
    cipher = AES.new(secret_key, AES.MODE_ECB)
    decrypted_value = cipher.decrypt(encrypted_value)
    unpadded_decrypted_value = unpad(decrypted_value, AES.block_size)
    return hexlify(unpadded_decrypted_value).decode()
