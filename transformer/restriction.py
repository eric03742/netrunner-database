import os
from pydantic import BaseModel, ConfigDict, TypeAdapter

from .base import OracleBase, ResultBase


class OracleBannedSubtype(BaseModel):
    """英文「禁限表」禁止子类型数据结构"""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    banned: list[str] = list()


class OracleModel(OracleBase):
    """英文「禁限表」数据结构"""

    name: str
    """禁限表名称"""

    format_id: str
    """禁限表所属环境"""

    date_start: str
    """禁限表开始日期"""

    banned: list[str] = list()
    """禁限表禁止卡牌"""

    restricted: list[str] = list()
    """（暂不使用）"""

    subtypes: OracleBannedSubtype = OracleBannedSubtype()
    """禁限表禁止子类型"""

    universal_faction_cost: dict[str, list[str]] = dict()
    """（暂不使用）"""

    global_penalty: dict[str, list[str]] = dict()
    """（暂不使用）"""

    points: dict[str, list[str]] = dict()
    """（暂不使用）"""

    point_limit: int = 0
    """（暂不使用）"""


class ResultModel(ResultBase):
    """最终「禁限表」数据结构"""

    codename: str
    """禁限表唯一标识"""

    oracle_name: str
    """禁限表英文名称"""

    format_codename: str
    """禁限表所属赛制"""

    start_date: str
    """禁限表开始日期"""

    banned_card_codenames: list[str]
    """禁限表禁止卡牌"""

    banned_subtype_codenames: list[str]
    """禁限表禁止子类型"""


result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/enUS/v2/restrictions"
RESULT_FILE = "result/restrictions.json"


def load_oracle() -> list[OracleModel]:
    result: list[OracleModel] = list()
    subfolders = sorted(os.listdir(ORACLE_FILE))
    for folder in subfolders:
        location = os.path.join(ORACLE_FILE, folder)
        filenames = sorted(os.listdir(location))
        for filename in filenames:
            fullname = os.path.join(location, filename)
            with open(fullname, "r", encoding="utf-8") as file:
                text = file.read()
                entries = OracleModel.model_validate_json(text, strict=True)
                result.append(entries)

    return result


def load_result() -> list[ResultModel]:
    oracles = load_oracle()
    results: list[ResultModel] = list()
    for oracle in oracles:
        result = ResultModel(
            codename=oracle.id,
            oracle_name=oracle.name,
            format_codename=oracle.format_id,
            start_date=oracle.date_start,
            banned_card_codenames=oracle.banned.copy(),
            banned_subtype_codenames=oracle.subtypes.banned.copy(),
        )

        results.append(result)

    return results


def save_restrictions() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
