import os
from pydantic import BaseModel, ConfigDict, TypeAdapter

from .base import ResultBase


class OracleModel(BaseModel):
    """英文「FAQ」数据结构"""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    card_id: str
    """FAQ所属卡牌"""

    question: str = ""
    """FAQ问题"""

    answer: str = ""
    """FAQ答案"""

    text_ruling: str =""
    """FAQ文本规则"""

    date_update: str
    """FAQ日期"""

    nsg_rules_team_verified: bool = False
    """FAQ是否官方认证"""


class ResultModel(ResultBase):
    """最终「FAQ」数据结构"""

    question: str
    """FAQ问题"""

    answer: str
    """FAQ答案"""

    text: str
    """FAQ文本"""

    card_codename: str
    """FAQ所属卡牌"""

    update_date: str
    """FAQ日期"""

    nsg_verified: bool
    """FAQ是否官方认证"""


oracle_validator = TypeAdapter(list[OracleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/enUS/v2/rulings"
RESULT_FILE = "result/rulings.json"


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
    curr_card = ""
    curr_count = 0
    oracles = load_oracle()
    results: list[ResultModel] = list()
    for oracle in oracles:
        if oracle.card_id != curr_card:
            curr_card = oracle.card_id
            curr_count = 0
        else:
            curr_count = curr_count + 1

        codename = f"{curr_card}-{curr_count}"
        result = ResultModel(
            codename=codename,
            question=oracle.question,
            answer=oracle.answer,
            text=oracle.text_ruling,
            card_codename=oracle.card_id,
            update_date=oracle.date_update,
            nsg_verified=oracle.nsg_rules_team_verified
        )

        results.append(result)

    return results


def save_ruling() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
