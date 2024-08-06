import enum, requests
from src.core.util.dict import convert_dict_keys_to_snake_case


class RiotClientException(Exception):

    class Type(enum.Enum):
        MethodNotAllowed = "method_not_allowed"
        RequestFailed = "request_failed"

    def __init__(self, type: Type, status_code: int = None, data: any = None, *args: object) -> None:
        super().__init__(*args)
        match type:
            case RiotClientException.Type.MethodNotAllowed:
                self.message = "Method not allowed"
            case RiotClientException.Type.RequestFailed:
                self.message = "Request failed"
        self.status_code = status_code
        self.data = data


class RiotClient:

    class Method(enum.Enum):
        GET = "get"
        POST = "post"

    class HostType(enum.Enum):
        REGIONAL = "regional"
        PLATFORM = "platform"

    class RegionalHost(enum.Enum):
        AMERICAS = "https://americas.api.riotgames.com"
        ASIA = "https://asia.api.riotgames.com"
        EUROPE = "https://europe.api.riotgames.com"
        SEA = "https://sea.api.riotgames.com"

    class PlatformHost(enum.Enum):
        BR1 = "https://br1.api.riotgames.com"
        EUN1 = "https://eun1.api.riotgames.com"
        EUW1 = "https://euw1.api.riotgames.com"
        JP1 = "https://jp1.api.riotgames.com"
        KR = "https://kr.api.riotgames.com"
        LA1 = "https://la1.api.riotgames.com"
        LA2 = "https://la2.api.riotgames.com"
        NA1 = "https://na1.api.riotgames.com"
        OC1 = "https://oc1.api.riotgames.com"
        TR1 = "https://tr1.api.riotgames.com"
        RU = "https://ru.api.riotgames.com"
        PH2 = "https://ph2.api.riotgames.com"
        SG2 = "https://sg2.api.riotgames.com"
        TH2 = "https://th2.api.riotgames.com"
        TW2 = "https://tw2.api.riotgames.com"
        VN2 = "https://vn2.api.riotgames.com"

    def __init__(self, api_key: str, regional_host: RegionalHost, platform_host: PlatformHost) -> None:
        self.api_key = api_key
        self.regional = regional_host
        self.platform_host = platform_host

    def get_host(self, host_type: HostType):
        if host_type == RiotClient.HostType.REGIONAL:
            return self.regional.value
        else:
            return self.platform_host.value

    def get_headers(self):
        return {"X-Riot-Token": self.api_key}

    def make_request(self, path: str, method: Method, host_type: HostType):
        host = self.get_host(host_type)
        request_args = {"url": f"{host}/{path}", "headers": self.get_headers()}
        match method:
            case RiotClient.Method.GET:
                response = requests.get(**request_args)
            case RiotClient.Method.POST:
                response = requests.post(**request_args)
            case _:
                raise RiotClientException(RiotClientException.Type.MethodNotAllowed)
        response_data = convert_dict_keys_to_snake_case(response.json())
        if response.status_code == 200:
            return response_data
        else:
            raise RiotClientException(RiotClientException.Type.RequestFailed, response.status_code, response_data)


class RiotService:
    def __init__(self, client: RiotClient) -> None:
        self.client = client


class Account(RiotService):
    def by_puuid(self, puuid: str) -> dict["name":str]:
        return self.client.make_request(
            f"/riot/account/v1/accounts/by-puuid/{puuid}",
            RiotClient.Method.GET,
            host_type=RiotClient.HostType.REGIONAL,
        )

    def by_riot_id(self, game_name: str, tag_line: str):
        return self.client.make_request(
            f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
            RiotClient.Method.GET,
            host_type=RiotClient.HostType.REGIONAL,
        )


class Summoner(RiotService):
    def by_puuid(self, puuid):
        return self.client.make_request(
            f"/lol/summoner/v4/summoners/by-puuid/{puuid}",
            RiotClient.Method.GET,
            host_type=RiotClient.HostType.PLATFORM,
        )


class RiotServices:
    def __init__(
        self, api_key: str, regional_host: RiotClient.RegionalHost, platform_host: RiotClient.PlatformHost
    ) -> None:
        client = RiotClient(api_key, regional_host, platform_host)
        self.account = Account(client)
        self.summoner = Summoner(client)
