import os
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, TypeAdapter

from .base import OracleBase, LocaleBase, ResultBase


class OracleCardFace(BaseModel):
    """英文「卡牌」卡面子类型数据结构"""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    title: str = ""
    """卡牌卡面名称"""

    stripped_title: str = ""
    """卡牌卡面名称（ASCII）"""

    text: str
    """卡牌卡面文本"""

    stripped_text: str
    """卡牌卡面文本（ASCII）"""

    subtypes: list[str] = list()
    """卡牌卡面子类型"""

    base_link: Optional[int] = None
    """卡牌卡面中转"""


class OracleModel(OracleBase):
    """英文「卡牌」数据结构"""

    title: str
    """卡牌名称"""

    stripped_title: str
    """卡牌名称（ASCII）"""

    text: str = ""
    """卡牌文本"""

    stripped_text: str = ""
    """卡牌文本（ASCII）"""

    card_type_id: str
    """卡牌类型"""

    subtypes: list[str] = list()
    """卡牌子类型"""

    side_id: str
    """卡牌阵营"""

    faction_id: str
    """卡牌派系"""

    is_unique: bool
    """卡牌是否独有"""

    deck_limit: Optional[int] = None
    """卡牌牌组限制"""

    advancement_requirement: Optional[int] = None
    """卡牌推进需求"""

    agenda_points: Optional[int] = None
    """卡牌议案分数"""

    base_link: Optional[int] = None
    """卡牌基础中转"""

    minimum_deck_size: Optional[int] = None
    """卡牌牌组最小张数"""

    influence_limit: Optional[int] = None
    """卡牌牌组影响力上限"""

    influence_cost: Optional[int] = None
    """卡牌影响力费用"""

    cost: Optional[int] = None
    """卡牌费用"""

    strength: Optional[int] = None
    """卡牌强度"""

    memory_cost: Optional[int] = None
    """卡牌内存费用"""

    trash_cost: Optional[int] = None
    """卡牌销毁费用"""

    layout_id: Optional[Literal["normal", "flip", "copy", "facade", "progression"]] = None
    """卡牌布局"""

    faces: list[OracleCardFace] = list()
    """卡牌其它牌面"""

    attribution: str = ""
    """卡牌冠名"""

    designed_by: str
    """卡牌设计组"""

    pronouns: str = ""
    """卡牌人称代词"""

    pronunciation_ipa: str = ""
    """卡牌读音（国际音标）"""

    pronunciation_approx: str = ""
    """卡牌读音（英文音标）"""

    narrative_text: str = ""
    """卡牌背景文字"""


class LocaleModel(LocaleBase):
    """中文「卡牌」数据结构"""

    name: str
    """卡牌名称"""

    text: str
    """卡牌文本"""


class ResultModel(ResultBase):
    """最终「卡牌」数据结构"""

    oracle_title: str
    """卡牌英文名称"""

    locale_title: str
    """卡牌中文名称"""

    stripped_title: str
    """卡牌英文名称（ASCII）"""

    oracle_text: str
    """卡牌英文文本"""

    locale_text: str
    """卡牌中文文本"""

    stripped_text: str
    """卡牌英文文本（ASCII）"""

    type_codename: str
    """卡牌类型"""

    subtype_codenames: list[str]
    """卡牌子类型"""

    side_codename: str
    """卡牌阵营"""

    faction_codename: str
    """卡牌派系"""

    is_unique: bool
    """卡牌是否独有"""

    deck_limit: Optional[int]
    """卡牌牌组限制"""

    advancement_requirement: Optional[int]
    """卡牌推进需求"""

    agenda_point: Optional[int]
    """卡牌议案分数"""

    base_link: Optional[int]
    """卡牌基础中转"""

    minimum_deck_size: Optional[int]
    """卡牌牌组最小张数"""

    influence_limit: Optional[int]
    """卡牌牌组影响力上限"""

    influence_cost: Optional[int]
    """卡牌影响力费用"""

    cost: Optional[int]
    """卡牌费用"""

    strength: Optional[int]
    """卡牌强度"""

    memory_cost: Optional[int]
    """卡牌内存费用"""

    trash_cost: Optional[int]
    """卡牌销毁费用"""

    attribution: str
    """卡牌冠名"""

    designed_by: str
    """卡牌设计组"""

    pronouns: str = ""
    """卡牌人称代词"""

    pronunciation_ipa: str
    """卡牌读音（国际音标）"""

    pronunciation_approx: str
    """卡牌读音（英文音标）"""

    extra_face: int
    """卡牌额外牌面数"""

    oracle_narrative: str
    """卡牌英文背景文字"""


locale_validator = TypeAdapter(list[LocaleModel])
result_validator = TypeAdapter(list[ResultModel])


ORACLE_FILE = "source/enUS/v2/cards"
LOCALE_FILE = "source/zhCN/data/json/cards.json"
RESULT_FILE = "result/cards.json"


def load_oracle() -> list[OracleModel]:
    result: list[OracleModel] = list()
    filenames = sorted(os.listdir(ORACLE_FILE))
    for filename in filenames:
        fullname = os.path.join(ORACLE_FILE, filename)
        with open(fullname, "r", encoding="utf-8") as file:
            text = file.read()
            item = OracleModel.model_validate_json(text, strict=True)
            result.append(item)

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

        oracle_text = oracle.text
        stripped_text = oracle.stripped_text
        if len(oracle.faces) > 0:
            for face in oracle.faces:
                face_type = "<strong>Back:</strong> " if oracle.layout_id == "flip" else "<strong>Side:</strong> "
                face_stripped_type = "Back: " if oracle.layout_id == "flip" else "Side: "
                face_title = face.title if len(face.title) > 0 else oracle.title
                face_stripped_title = face.stripped_title if len(face.stripped_title) > 0 else oracle.stripped_title
                face_text = face.text
                face_stripped_text = face.stripped_text
                oracle_text = oracle_text + f"\n{face_type}{face_title}\n{face_text}"
                stripped_text = stripped_text + f"\n{face_stripped_type}{face_stripped_title}\n{face_stripped_text}"

        result = ResultModel(
            codename=oracle.id,
            oracle_title=oracle.title,
            locale_title=locale.name,
            stripped_title=oracle.stripped_title,
            oracle_text=oracle_text,
            locale_text=locale.text,
            stripped_text=stripped_text,
            type_codename=oracle.card_type_id,
            subtype_codenames=oracle.subtypes.copy(),
            side_codename=oracle.side_id,
            faction_codename=oracle.faction_id,
            is_unique=oracle.is_unique,
            deck_limit=oracle.deck_limit,
            advancement_requirement=oracle.advancement_requirement,
            agenda_point=oracle.agenda_points,
            base_link=oracle.base_link,
            minimum_deck_size=oracle.minimum_deck_size,
            influence_limit=oracle.influence_limit,
            influence_cost=oracle.influence_cost,
            cost=oracle.cost,
            strength=oracle.strength,
            memory_cost=oracle.memory_cost,
            trash_cost=oracle.trash_cost,
            attribution=oracle.attribution,
            designed_by=oracle.designed_by,
            pronouns=oracle.pronouns,
            pronunciation_ipa=oracle.pronunciation_ipa,
            pronunciation_approx=oracle.pronunciation_approx,
            extra_face=len(oracle.faces),
            oracle_narrative=oracle.narrative_text
        )

        results.append(result)

    return results


def save_card() -> None:
    results = load_result()
    raw = result_validator.dump_json(results, indent=2, ensure_ascii=False)
    texts = raw.decode("utf-8", errors="strict")
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(texts)
