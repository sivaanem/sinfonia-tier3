from uuid import UUID


APP_NAME_TO_UUID = {
    "helloworld": "00000000-0000-0000-0000-000000000000",
    "loadtest": "00000000-0000-0000-0000-000000000111"
}

UUID_TO_APP_NAME = {
    "00000000-0000-0000-0000-000000000111": "loadtest",
    "00000000-0000-0000-0000-000000000000": "helloworld",
}


def app_name_to_uuid(value: str) -> UUID:
    uuid = APP_NAME_TO_UUID.get(value, value)
    return UUID(uuid)


def uuid_to_app_name(uuid: str | UUID) -> str:
    return UUID_TO_APP_NAME[str(uuid)]
