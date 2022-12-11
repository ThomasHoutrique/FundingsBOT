import httpx
from httpx import Response


class bybit:
    def __init__(self):
        self.base_url = "https://api.bybit.com"

    def get_contract_names_list(self):
        """
        Get the list of active contracts from ByBit
        """
        url: str = f"{self.base_url}/v2/public/symbols"
        response: Response = httpx.get(url)
        if response.status_code == 200:
            contracts_names: list = []
            for contract in response.json()["result"]:
                contracts_names.append(contract["base_currency"])
            return contracts_names
        else:
            raise Exception("Error getting contract list from ByBit")

    def get_avg_funding_rate_history(self, symbol: str, period: int) -> float:
        """
        Get the average funding rate for a given symbol over a given period of time
        symbol: str
        period: int
        """
        if period > 33:
            raise Exception("Period must be less than 33 days")
        url: str = f"{self.base_url}/derivatives/v3/public/funding/history-funding-rate?category=linear&limit={period * 3}&symbol={symbol}"
        response: Response = httpx.get(url)
        if response.status_code == 200:
            avg_funding_rate: float = 0.0
            for funding_rate in response.json()["result"]["list"]:
                avg_funding_rate += float(funding_rate["fundingRate"]) * 100
            avg_funding_rate: float = avg_funding_rate / (period * 3)
            return avg_funding_rate
        else:
            raise Exception(
                f"Error getting funding rate history for {symbol} from ByBit"
            )
