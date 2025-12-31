import os
from typing import Optional
from pydantic import BaseModel, ConfigDict, TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OraclePrintingFace(BaseModel):
    """英文「卡图」卡面子类型数据结构"""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    flavor: str
    """卡图卡面风味文字"""

    copy_quantity: Optional[int] = None
    """不使用"""


class OracleModel(OracleBase):
    """英文「卡图」数据结构"""

    card_id: str
    """卡图所属卡牌"""

    card_set_id: str
    """卡图所属卡包"""

    position: int
    """卡图序号"""

    flavor: str = ""
    """卡图风味文字"""

    quantity: int
    """卡图数量"""

    faces: list[OraclePrintingFace] = list()
    """卡图牌面"""

    illustrator: str = ""
    """卡图插画作者"""

    released_by: str
    """卡图发行组"""

    copy_quantity: Optional[int] = None
    """不使用"""

    layout_id: str = ""
    """不使用"""


class LocaleModel(LocaleBase):
    """中文「卡图」数据结构"""

    flavor: str
    """卡图风味文字"""


class ResultModel(ResultBase):
    """最终「卡图」数据结构"""

    card_codename: str
    """卡图所属卡牌"""

    set_codename: str
    """卡图所属卡包"""

    position: int
    """卡图序号"""

    oracle_flavor: str
    """卡图英文风味文字"""

    locale_flavor: str
    """卡图本地化风味文字"""

    quantity: int
    """卡图在卡包中数量"""

    extra_face: int
    """卡牌额外牌面数"""

    illustrator: str
    """卡图插画作者"""

    released_by: str
    """卡图发行组"""


oracle_validator = TypeAdapter(list[OracleModel])
locale_validator = TypeAdapter(list[LocaleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/enUS/v2/printings"
LOCALE_FILE = "source/zhCN/data/json/printings.json"
RESULT_FILE = "result/printings.json"


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

        oracle_flavor = oracle.flavor
        for face in oracle.faces:
            if len(face.flavor) > 0:
                oracle_flavor = oracle_flavor + ("\n" if len(oracle_flavor) > 0 else "") + face.flavor

        result = ResultModel(
            codename=oracle.id,
            card_codename=oracle.card_id,
            set_codename=oracle.card_set_id,
            position=oracle.position,
            oracle_flavor=oracle_flavor,
            locale_flavor=locale.flavor,
            quantity=oracle.quantity,
            extra_face=len(oracle.faces),
            illustrator=oracle.illustrator,
            released_by=oracle.released_by
        )

        results.append(result)

    return results


def save_printing() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
