from pybit.unified_trading import HTTP
from dotenv import dotenv_values

class _Config:
    """
        Load environment variables from .env file\n
        API_KEY, API_SECRET, ENVIROMENT
    """
    def __init__(self):
        self._env = dotenv_values(".env")
        self._api_key:str = self._env.get("API_KEY", "")
        self._api_secret:str = self._env.get("API_SECRET", "")
        self._is_production:bool = self._env.get("ENVIROMENT", "testnet") == "mainnet"

    def get_session(self):
        """
            Get a new session for the API\n
            Returns: session object
        """

        _session = HTTP(
            demo = not self._is_production,
            testnet = not self._is_production,
            api_key = self._api_key,
            api_secret = self._api_secret,
        )
        return _session

    def __repr__(self):
        masked_key = self._api_key[:4] + "..." if self._api_key else "None"
        return (
            f"api_key={masked_key},"
            f"testnet={not self._is_production},"
            f"enviroment={"mainnet" if self._is_production else "testnet"}"
        )

session = _Config().get_session()
