from kucoin import kucoin
from bybit import bybit


def filter_contracts(*args) -> list:
    """
    Filter the contracts that are available on all of the exchanges
    """
    contracts: list = [exchange.get_contract_names_list() for exchange in args]
    # Only keep the contracts that are available on all exchanges
    return list(set(contracts[0]) & set(contracts[1]))


LEVIER = 2
PERIOD = 7

kucoin: kucoin = kucoin()
bybit: bybit = bybit()


print("Getting contracts list...")
contracts_list: list = filter_contracts(kucoin, bybit)
print("Done")


for symbol in filter_contracts(kucoin, bybit):
    bybit_funding_rate: float = bybit.get_avg_funding_rate_history(
        symbol + "USDT", PERIOD
    )
    kucoin_funding_rate: float = kucoin.get_avg_funding_rate_history(
        symbol + "USDTM", PERIOD
    )
    print(
        f"{symbol} - ByBit: {bybit_funding_rate:.2f}% - KuCoin: {kucoin_funding_rate:.2f}% - Difference: {(bybit_funding_rate - kucoin_funding_rate):.4f}%"
    )
