
import operator

from tensortrade.data import Lambda, Module, Select, BinOp
from tensortrade.wallets import Wallet


def create_wallet_source(wallet: Wallet, include_worth=True):
    exchange_name = wallet.exchange.name
    symbol = wallet.instrument.symbol

    with Module(exchange_name + ":/" + symbol) as wallet_ds:
        def balance_as_float(w):
            return w.balance.as_float()
        free_balance = Lambda(balance_as_float, wallet, name="free")

        def locked_balance_as_float(w):
            return w.locked_balance.as_float()
        locked_balance = Lambda(locked_balance_as_float, wallet, name="locked")

        def total_balance_as_float(w):
            return w.total_balance.as_float()
        total_balance = Lambda(total_balance_as_float, wallet, name="total")

        nodes = [free_balance, locked_balance, total_balance]

        if include_worth:
            def include_worth_func(node):
                return node.name.endswith(symbol)

            price = Select(include_worth_func)(wallet.exchange)
            worth = BinOp(operator.mul, name="worth")(price, total_balance)
            nodes += [worth]

    return wallet_ds
