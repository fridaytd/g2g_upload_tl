from pydantic import BaseModel, RootModel
from typing import Generic, TypeVar

T = TypeVar("T", bound=BaseModel)


class ResponseResult(BaseModel, Generic[T]):
    results: list[T]


class Response(BaseModel, Generic[T]):
    code: int
    messages: list[str]
    payload: ResponseResult[T]
    request_id: str


class CatName(BaseModel):
    en: str
    id: str
    ko: str | None = None


class Category(BaseModel):
    cat_name: CatName
    cat_id: str
    service_id: str
    created_at: int
    updated_at: int
    sort_order: int


class Brand(BaseModel):
    brand_id: str
    service_id: str
    brand_img_url: str
    services: list[str]
    brand_tags: list[str]
    total_offer: int


class Keyword(BaseModel):
    en: str
    keyword_id: str
    keyword_category: str
    default_name: str
    seo_term: str | None = None


class KeywordDict(RootModel[dict[str, Keyword]]):
    def __getitem__(self, item):
        return self.root[item]


class MarketingTitle(BaseModel):
    en: str | None = None
    id: str | None = None


class Cat(BaseModel):
    service_id: str
    brand_id: str
    seo_term_alias: str | None = None
    marketing_title: MarketingTitle | None = None
    cat_path: str | None = None


class SeoTerm(BaseModel):
    seo_term: str
    seo_term_alias: str | None = None


class CategoryJson(RootModel[dict[str, Cat | SeoTerm]]):
    pass


class KeywordRelation(BaseModel):
    relation_id: str
    service_id: str
    brand_id: str
    region_id: str


class ChildrenCollection(BaseModel):
    collection_id: str
    dataset_id: str
    parent_id: str
    value: str
    description: dict
    sort_order: int
    total_children: int
    children: list["ChildrenCollection"]
    product_tags: list[str]
    dpd_collections: list[dict]
    is_multi_layer: bool


class CollectionLabel(BaseModel):
    id: str | None = None
    en: str


class Collection(BaseModel):
    collection_id: str
    is_grouping: bool
    is_multiselect: bool
    value: str
    label: CollectionLabel
    sort_order: int
    input_field: str
    is_required: bool
    is_updatable: bool
    is_multi_layer: bool
    created_at: int
    updated_at: int
    is_feature: bool
    children: list[ChildrenCollection]
