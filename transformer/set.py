from pydantic import TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleModel(OracleBase):
    """英文「卡包」数据结构"""

    name: str
    """卡包名称"""

    legacy_code: str
    """卡包旧版唯一标识符"""

    card_cycle_id: str
    """卡包所属循环ID"""

    card_set_type_id: str
    """卡包所属卡包类型ID"""

    date_release: str
    """卡包发行日期"""

    position: int
    """卡包在循环中位置"""

    size: int
    """卡包卡牌数量"""

    released_by: str
    """卡包发行组"""


class LocaleModel(LocaleBase):
    """中文「卡包」数据结构"""

    name: str
    """卡包名称"""


class ResultModel(ResultBase):
    """最终「卡包」数据结构"""

    oracle_name: str
    """卡包英文名称"""

    locale_name: str
    """卡包中文名称"""

    cycle_codename: str
    """卡包所属循环ID"""

    settype_codename: str
    """卡包所属卡包类型ID"""

    release_date: str
    """卡包发行日期"""

    position: int
    """卡包在循环中位置"""

    size: int
    """卡包卡牌数量"""

    released_by: str
    """卡包发行组"""


oracle_validator = TypeAdapter(list[OracleModel])
locale_validator = TypeAdapter(list[LocaleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/enUS/v2/card_sets.json"
LOCALE_FILE = "source/zhCN/data/json/sets.json"
RESULT_FILE = "result/sets.json"


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
            cycle_codename=oracle.card_cycle_id,
            settype_codename=oracle.card_set_type_id,
            release_date=oracle.date_release,
            position=oracle.position,
            size=oracle.size,
            released_by=oracle.released_by
        )

        results.append(result)

    return results


def save_set() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
