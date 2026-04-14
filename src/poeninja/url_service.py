from enum import Enum
from urllib.parse import urlencode


class SortBy(Enum):
    NONE = "none"
    LIFE = "life"
    ES = "es"
    EHP = "ehp"
    DPS = "dps"
    DEPTH = "depth"


class TimelessJewels(Enum):
    NONE = "none"
    LETHAL_PRIDE = "Lethal Pride"
    MILITANT_FAITH = "Militant Faith"
    GLOURIOUS_VANITY = "Glorious Vanity"
    BRUTAL_RESTRAINT = "Brutal Restraint"
    ELEGANT_HUBRIS = "Elegant Hubris"
    HEROIC_TRAGEDY = "Heroic Tragedy"


class TimeMachine(Enum):
    LATEST = "latest"
    HOUR_3 = "hour-3"
    HOUR_6 = "hour-6"
    HOUR_12 = "hour-12"
    HOUR_18 = "hour-18"
    DAY_1 = "day-1"
    DAY_2 = "day-2"
    DAY_3 = "day-3"
    DAY_4 = "day-4"
    DAY_5 = "day-5"
    DAY_6 = "day-6"
    WEEK_1 = "week-1"
    WEEK_2 = "week-2"
    WEEK_3 = "week-3"
    WEEK_4 = "week-4"
    WEEK_5 = "week-5"


class MinMaxFilter:
    def __init__(self, param_name: str, min_value: int = None, max_value: int = None):
        self.param_name = param_name
        self.min_value = min_value
        self.max_value = max_value

    def update_params(self, params: dict):
        if self.min_value is not None:
            params[f"min-{self.param_name}"] = self.min_value
        if self.max_value is not None:
            params[f"max-{self.param_name}"] = self.max_value


class SearchParams:
    def __init__(
        self,
        timeless_jewel: TimelessJewels,
        sort_by: SortBy,
        sort_asc: bool = False,
        time_machine: TimeMachine = TimeMachine.LATEST,
        min_level: int = None,
        max_level: int = None,
        min_life: int = None,
        max_life: int = None,
        min_es: int = None,
        max_es: int = None,
        min_ehp: int = None,
        max_ehp: int = None,
    ):
        self.timeless_jewel = timeless_jewel
        self.sort_by = sort_by
        self.sort_asc = sort_asc
        self.level_filter = MinMaxFilter("level", min_level, max_level)
        self.life_filter = MinMaxFilter("life", min_life, max_life)
        self.es_filter = MinMaxFilter("energyshield", min_es, max_es)
        self.ehp_filter = MinMaxFilter("ehp", min_ehp, max_ehp)
        self.time_machine = time_machine

    def get_urlencode_params(self) -> str:
        params = {}
        params.update({"items": self.timeless_jewel.value} if self.timeless_jewel != TimelessJewels.NONE else {})
        params.update({"timemachine": self.time_machine.value} if self.time_machine != TimeMachine.LATEST else {})
        self.level_filter.update_params(params)
        self.life_filter.update_params(params)
        self.es_filter.update_params(params)
        self.ehp_filter.update_params(params)
        params.update({"sort": self.sort_by.value} if self.sort_by != SortBy.NONE else {})
        params.update({"sort-asc": "true"} if self.sort_by != SortBy.NONE and self.sort_asc else {})
        return urlencode(params)


def construct_search_url(base_url: str, league: str, params: SearchParams) -> str:
    return f"{base_url}/poe1/builds/{league}?{params.get_urlencode_params()}"
