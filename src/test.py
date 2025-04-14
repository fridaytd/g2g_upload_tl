import json

import httpx

from app.config import config
from app.g2g.crwl_api import crwl_g2g_api_client
from app.paths import ROOT_PATH
from app.g2g.models import Collection
from app.sheet.models import NewPlatformData


def main():
    max_collection: int = 0

    keywords = crwl_g2g_api_client.get_keywords()

    flatform_datas: list[NewPlatformData] = []

    index: int = 0

    for category in crwl_g2g_api_client.get_categories().payload.results:
        # print(f"Category: {category.cat_name}")
        for brand in crwl_g2g_api_client.get_brands(
            category_id=category.cat_id
        ).payload.results:
            # print(f"Category: CatBrand: {keywords[brand.brand_id].default_name}")
            try:
                keyword_relations = crwl_g2g_api_client.get_keyword_relation(
                    service_id=category.service_id, brand_id=brand.brand_id
                ).payload.results
                for keyword_relation in keyword_relations:
                    print(
                        f"Category: {category.cat_name.id} - Brand: {keywords[brand.brand_id].default_name} - Region: {keywords[keyword_relation.region_id].default_name if keyword_relation.region_id else ''}"
                    )

                    print(
                        f"{category.service_id} - {brand.brand_id} - {
                            keyword_relation.region_id
                            if keyword_relation.region_id
                            else None
                        }"
                    )
                    print("-----------")
                    __collections = crwl_g2g_api_client.get_collections(
                        service_id=category.service_id,
                        brand_id=brand.brand_id,
                        region_id=keyword_relation.region_id
                        if keyword_relation.region_id
                        else None,
                    ).payload.results
                    if len(__collections) > max_collection:
                        max_collection = len(__collections)
                    index += 1
                    flatform_datas.append(
                        NewPlatformData(
                            STT=index,
                            # sheet_id=config.SPREADSHEET_KEY,
                            # sheet_name="Data33",
                            # index=index + 1,
                            service_id=category.service_id,
                            service_name=category.cat_name.id,
                            brand_id=brand.brand_id,
                            brand_name=keywords[brand.brand_id].default_name,
                            region_id=keyword_relation.region_id,
                            region_name=keywords[
                                keyword_relation.region_id
                            ].default_name
                            if keyword_relation.region_id
                            else "",
                            service_option=f"Category: {category.cat_name.id} - Brand: {keywords[brand.brand_id].default_name} - Region: {keywords[keyword_relation.region_id].default_name if keyword_relation.region_id else ''}",
                            product_id=keyword_relation.relation_id,
                            product_name=f"Category: {category.cat_name.id} - Brand: {keywords[brand.brand_id].default_name} - Region: {keywords[keyword_relation.region_id].default_name if keyword_relation.region_id else ''}",
                            collections=json.dumps(
                                [
                                    collection.model_dump(mode="json")
                                    for collection in __collections
                                ]
                            ),
                        )
                    )
            except httpx.HTTPStatusError as e:
                print(e)

    with open(ROOT_PATH / "data" / "collections.json", "w") as f:
        json.dump([data.model_dump(mode="json") for data in flatform_datas], f)
    print(max_collection)


def test():
    collections: list[Collection] = []

    with open(ROOT_PATH / "data" / "collections.json") as f:
        data = json.load(f)

    for dt in data:
        collections.append(Collection.model_validate(dt))

    max = 0
    index = 0
    for i, collection in enumerate(collections):
        if len(collection.children) > max:
            max = len(collection.children)
            index = 1

    print(max)
    print(data[index])
    for cole in data[index]:
        print(cole["value"])


if __name__ == "__main__":
    main()
    # test()
    # crwl_g2g_api_client.get_collections(
    #     service_id="8f88b6fd-93df-4a07-b8b0-7d90b152b81f",
    #     brand_id="9bca639f-5fc5-4ebb-8892-b2e6a2ff50f6",
    #     region_id="0f76ac42-3267-4d77-9fba-f9d9d719dac9",
    # )
    # print(NewPlatformData.get(config.SPREADSHEET_KEY, sheet_name="DT", index=1))
