from httpx import Response
import httpx


class kucoin:
    def __init__(self):
        self.base_url = "https://api-futures.kucoin.com"

    def get_contract_names_list(self):
        """
        Get the list of active contracts from KuCoin
        """
        url: str = f"{self.base_url}/api/v1/contracts/active"
        contracts_names: list = []
        response: Response = httpx.get(url)
        if response.status_code == 200:
            for contract in response.json()["data"]:
                contracts_names.append(contract["baseCurrency"])
            return contracts_names
        else:
            raise Exception("Error getting contract list from KuCoin")

    def get_avg_funding_rate_history(self, symbol: str, period: int) -> float:
        """
        Get the average funding rate for a given symbol over a given period of time
        symbol: str
        period: int
        """
        if period > 33:
            raise Exception("Period must be less than 33 days")
        url: str = f"https://futures.kucoin.com/_api/web-front/contract/{symbol}/funding-rates?reverse=true&maxCount={period * 3}&lang=en_US"
        response: Response = httpx.get(url)
        if response.status_code == 200:
            avg_funding_rate: float = 0.0
            for funding_rate in response.json()["data"]["dataList"]:
                avg_funding_rate += float(funding_rate["value"]) * 100
            avg_funding_rate: float = avg_funding_rate / (period * 3)
            return avg_funding_rate
        else:
            raise Exception(
                f"Error getting funding rate history for {symbol} from KuCoin for {period} days"
            )
