from pydantic import BaseModel, ConfigDict


class OracleBase(BaseModel):
    """英文源数据通用字段"""

    model_config = ConfigDict(strict=True, frozen=True)

    id: str
    """唯一标识符"""


class LocaleBase(BaseModel):
    """本地化数据通用字段"""

    model_config = ConfigDict(strict=True, frozen=True)

    id: str
    """唯一标识符"""


class ResultBase(BaseModel):
    """最终数据通用字段"""

    model_config = ConfigDict(strict=True)

    codename: str
    """唯一标识符"""
