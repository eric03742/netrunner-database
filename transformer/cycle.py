from pydantic import TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleModel(OracleBase):
    """英文「循环」数据结构"""

    name: str
    """循环名称"""

    legacy_code: str
    """循环旧版唯一标识符"""

    position: int
    """循环序号"""

    released_by: str
    """循环发行组"""


class LocaleModel(LocaleBase):
    """中文「循环」数据结构"""

    name: str
    """循环名称"""


class ResultModel(ResultBase):
    """最终「循环」数据结构"""

    oracle_name: str
    """循环英文名称"""

    locale_name: str
    """循环中文名称"""

    position: int
    """循环序号"""

    released_by: str
    """循环发行组"""


oracle_validator = TypeAdapter(list[OracleModel])
locale_validator = TypeAdapter(list[LocaleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/en/v2/card_cycles.json"
LOCALE_FILE = "source/zh/data/json/cycles.json"
RESULT_FILE = "result/cycles.json"


def load_oracle() -> list[OracleModel]:
    with open(ORACLE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = oracle_validator.validate_json(text, strict=True)
        return entries


def load_locale() -> dict[str, LocaleModel]:
    with open(LOCALE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = locale_validator.validate_json(text, strict=True)
        result: dict[str, LocaleModel] = dict()
        for e in entries:
            result[e.id] = e

        return result


def load_result() -> list[ResultModel]:
    oracles = load_oracle()
    locales = load_locale()
    results: list[ResultModel] = list()
    for oracle in oracles:
        locale = locales.get(oracle.id, None)
        if locale is None:
            raise Exception(f"ID = {oracle.id}：缺少中文数据!")

        result = ResultModel(
            codename=oracle.id,
            oracle_name=oracle.name,
            locale_name=locale.name,
            position=oracle.position,
            released_by=oracle.released_by
        )

        results.append(result)

    return results


def save_cycle() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
