import typing
from dataclasses import dataclass
from base64 import b64decode
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class WhitelistInsuranceAccountJSON(typing.TypedDict):
    nonce: int
    user_key: str


@dataclass
class WhitelistInsuranceAccount:
    discriminator: typing.ClassVar = b"\nh\xc0\xcb\x81<(\x02"
    layout: typing.ClassVar = borsh.CStruct(
        "nonce" / borsh.U8, "user_key" / BorshPubkey
    )
    nonce: int
    user_key: PublicKey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: PublicKey,
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.Optional["WhitelistInsuranceAccount"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp["result"]["value"]
        if info is None:
            return None
        if info["owner"] != str(PROGRAM_ID):
            raise ValueError("Account does not belong to this program")
        bytes_data = b64decode(info["data"][0])
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[PublicKey],
        commitment: typing.Optional[Commitment] = None,
    ) -> typing.List[typing.Optional["WhitelistInsuranceAccount"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["WhitelistInsuranceAccount"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != PROGRAM_ID:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "WhitelistInsuranceAccount":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = WhitelistInsuranceAccount.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonce=dec.nonce,
            user_key=dec.user_key,
        )

    def to_json(self) -> WhitelistInsuranceAccountJSON:
        return {
            "nonce": self.nonce,
            "user_key": str(self.user_key),
        }

    @classmethod
    def from_json(
        cls, obj: WhitelistInsuranceAccountJSON
    ) -> "WhitelistInsuranceAccount":
        return cls(
            nonce=obj["nonce"],
            user_key=PublicKey(obj["user_key"]),
        )
