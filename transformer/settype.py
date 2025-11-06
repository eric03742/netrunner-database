from pydantic import TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleModel(OracleBase):
    """英文「卡包类型」数据结构"""

    name: str
    """卡包类型名称"""

    description: str
    """卡包类型描述"""


class LocaleModel(LocaleBase):
    """中文「卡包类型」数据结构"""

    name: str
    """卡包类型名称"""

    description: str
    """卡包类型描述"""


class ResultModel(ResultBase):
    """最终「卡包类型」数据结构"""

    oracle_name: str
    """卡包类型英文名称"""

    locale_name: str
    """卡包类型中文名称"""

    oracle_desc: str
    """卡包类型英文描述"""

    locale_desc: str
    """卡包类型中文描述"""


oracle_validator = TypeAdapter(list[OracleModel])
locale_validator = TypeAdapter(list[LocaleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/en/v2/card_set_types.json"
LOCALE_FILE = "source/zh/data/json/set_types.json"
RESULT_FILE = "result/settypes.json"


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
            oracle_desc=oracle.description,
            locale_desc=locale.description
        )

        results.append(result)

    return results


def save_settype() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
