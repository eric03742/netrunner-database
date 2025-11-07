import os
from pydantic import TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleSnapshot(OracleBase):
    """英文「环境」数据结构"""

    date_start: str
    """环境开始时间"""

    card_pool_id: str
    """环境使用卡池"""

    restriction_id: str = ""
    """环境使用禁限表"""

    active: bool = False
    """环境是否正在使用"""


class OracleFormat(OracleBase):
    """英文「赛制」数据结构"""

    name: str
    """赛制名称"""

    snapshots: list[OracleSnapshot]
    """赛制历代环境"""


class LocaleFormat(LocaleBase):
    """中文「赛制」数据结构"""

    name: str
    """赛制名称"""


class ResultSnapshot(ResultBase):
    """最终「环境」数据结构"""

    start_date: str
    """环境开始日期"""

    format_codename: str
    """环境所属赛制"""

    restriction_codename: str
    """环境使用禁限表"""

    pool_codename: str
    """环境使用卡池"""

    active: bool
    """环境是否正在使用"""


class ResultFormat(ResultBase):
    """最终「赛制」数据结构"""

    oracle_name: str
    """赛制英文名称"""

    locale_name: str
    """赛制中文名称"""


locale_validator = TypeAdapter(list[LocaleFormat])
result_format_validator = TypeAdapter(list[ResultFormat])
result_snapshot_validator = TypeAdapter(list[ResultSnapshot])


ORACLE_FILE = "source/en/v2/formats/"
LOCALE_FILE = "source/zh/data/json/formats.json"
RESULT_FORMAT_FILE = "result/formats.json"
RESULT_SNAPSHOT_FILE = "result/snapshots.json"


def load_oracle() -> list[OracleFormat]:
    result: list[OracleFormat] = list()
    filenames = sorted(os.listdir(ORACLE_FILE))
    for filename in filenames:
        fullname = os.path.join(ORACLE_FILE, filename)
        with open(fullname, "r", encoding="utf-8") as file:
            text = file.read()
            entry = OracleFormat.model_validate_json(text, strict=True)
            result.append(entry)

    return result


def load_locale() -> dict[str, LocaleFormat]:
    with open(LOCALE_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        entries = locale_validator.validate_json(text, strict=True)
        result: dict[str, LocaleFormat] = dict()
        for e in entries:
            result[e.id] = e

        return result


def load_format() -> list[ResultFormat]:
    oracles = load_oracle()
    locales = load_locale()
    results: list[ResultFormat] = list()
    for oracle in oracles:
        locale = locales.get(oracle.id, None)
        if locale is None:
            raise Exception(f"ID = {oracle.id}：缺少中文数据!")

        result = ResultFormat(
            codename=oracle.id,
            oracle_name=oracle.name,
            locale_name=locale.name
        )

        results.append(result)

    return results


def load_snapshot() -> list[ResultSnapshot]:
    oracles = load_oracle()
    results: list[ResultSnapshot] = list()
    for oracle in oracles:
        for snapshot in oracle.snapshots:
            result = ResultSnapshot(
                codename=snapshot.id,
                start_date=snapshot.date_start,
                format_codename=oracle.id,
                pool_codename=snapshot.card_pool_id,
                restriction_codename=snapshot.restriction_id,
                active=snapshot.active
            )

            results.append(result)

    return results


def save_format() -> None:
    results = load_format()
    raw = result_format_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FORMAT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)


def save_snapshot() -> None:
    results = load_snapshot()
    raw = result_snapshot_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_SNAPSHOT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
