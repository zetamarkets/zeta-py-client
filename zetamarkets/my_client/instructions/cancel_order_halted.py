from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class CancelOrderHaltedArgs(typing.TypedDict):
    side: types.side.SideKind
    order_id: int


layout = borsh.CStruct("side" / types.side.layout, "order_id" / borsh.U128)


class CancelOrderHaltedAccounts(typing.TypedDict):
    cancel_accounts: CancelAccountsNested


class CancelAccountsNested(typing.TypedDict):
    zeta_group: PublicKey
    state: PublicKey
    margin_account: PublicKey
    dex_program: PublicKey
    serum_authority: PublicKey
    open_orders: PublicKey
    market: PublicKey
    bids: PublicKey
    asks: PublicKey
    event_queue: PublicKey


def cancel_order_halted(
    args: CancelOrderHaltedArgs, accounts: CancelOrderHaltedAccounts
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["zeta_group"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["state"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["margin_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["dex_program"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["serum_authority"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["open_orders"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["market"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["bids"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["asks"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["cancel_accounts"]["event_queue"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    identifier = b"\x00\xc0\xe9\x02\xfc\xfb\x82\xa9"
    encoded_args = layout.build(
        {
            "side": args["side"].to_encodable(),
            "order_id": args["order_id"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, PROGRAM_ID, data)
