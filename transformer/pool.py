import os
from pydantic import TypeAdapter

from .base import OracleBase, ResultBase


class OracleModel(OracleBase):
    """英文「卡池」数据结构"""

    name: str
    """卡池名称"""

    format_id: str
    """卡池所属环境"""

    card_cycle_ids: list[str] = []
    """卡池包含循环"""

    card_set_ids: list[str]
    """卡池包含卡包"""


class ResultModel(ResultBase):
    """最终「卡池」数据结构"""

    oracle_name: str
    """卡池英文名称"""

    format_codename: str
    """卡池所属赛制"""

    set_codenames: list[str]
    """卡池包含卡包"""

    cycle_codenames: list[str]
    """卡池包含循环"""


oracle_validator = TypeAdapter(list[OracleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/enUS/v2/card_pools"
RESULT_FILE = "result/pools.json"


def load_oracle() -> list[OracleModel]:
    result: list[OracleModel] = list()
    filenames = sorted(os.listdir(ORACLE_FILE))
    for filename in filenames:
        fullname = os.path.join(ORACLE_FILE, filename)
        with open(fullname, "r", encoding="utf-8") as file:
            text = file.read()
            entries = oracle_validator.validate_json(text, strict=True)
            result.extend(entries)

    return result


def load_result() -> list[ResultModel]:
    oracles = load_oracle()
    results: list[ResultModel] = list()
    for oracle in oracles:
        result = ResultModel(
            codename=oracle.id,
            oracle_name=oracle.name,
            format_codename=oracle.format_id,
            set_codenames=oracle.card_set_ids.copy(),
            cycle_codenames=oracle.card_cycle_ids.copy()
        )

        results.append(result)

    return results


def save_pool() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
