import os
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Self, Final
from gspread.worksheet import Worksheet
from gspread.auth import service_account

from .g_sheet import gsheet_client
from .exceptions import SheetError
from ..paths import ROOT_PATH

COL_META_FIELD_NAME: Final[str] = "col_name_xxx"


class ColSheetModel(BaseModel):
    # Model config
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sheet_id: str
    sheet_name: str
    index: int

    @classmethod
    def get_worksheet(
        cls,
        sheet_id: str,
        sheet_name: str,
    ) -> Worksheet:
        spreadsheet = gsheet_client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)

        return worksheet

    @classmethod
    def mapping_fields(cls) -> dict:
        mapping_fields = {}
        for field_name, field_info in cls.model_fields.items():
            if hasattr(field_info, "metadata"):
                for metadata in field_info.metadata:
                    if COL_META_FIELD_NAME in metadata:
                        mapping_fields[field_name] = metadata[COL_META_FIELD_NAME]
                        break

        return mapping_fields

    @classmethod
    def get(
        cls,
        sheet_id: str,
        sheet_name: str,
        index: int,
    ) -> Self:
        mapping_dict = cls.mapping_fields()

        query_value = []

        for _, v in mapping_dict.items():
            query_value.append(f"{v}{index}")

        worksheet = cls.get_worksheet(sheet_id=sheet_id, sheet_name=sheet_name)

        model_dict = {
            "index": index,
            "sheet_id": sheet_id,
            "sheet_name": sheet_name,
        }

        query_results = worksheet.batch_get(query_value)
        count = 0
        for k, _ in mapping_dict.items():
            model_dict[k] = query_results[count].first()
            if isinstance(model_dict[k], str):
                model_dict[k] = model_dict[k].strip()
            count += 1
        return cls.model_validate(model_dict)

    @classmethod
    def batch_get(
        cls,
        sheet_id: str,
        sheet_name: str,
        indexes: list[int],
    ) -> list[Self]:
        worksheet = cls.get_worksheet(
            sheet_id=sheet_id,
            sheet_name=sheet_name,
        )
        mapping_dict = cls.mapping_fields()

        result_list: list[Self] = []

        query_value = []
        for index in indexes:
            for _, v in mapping_dict.items():
                query_value.append(f"{v}{index}")

        query_results = worksheet.batch_get(query_value)

        count = 0

        for index in indexes:
            model_dict = {
                "index": index,
                "sheet_id": sheet_id,
                "sheet_name": sheet_name,
            }

            for k, _ in mapping_dict.items():
                model_dict[k] = query_results[count].first()
                if isinstance(model_dict[k], str):
                    model_dict[k] = model_dict[k].strip()
                count += 1

            result_list.append(cls.model_validate(model_dict))
        return result_list

    @classmethod
    def batch_update(
        cls,
        sheet_id: str,
        sheet_name: str,
        list_object: list[Self],
    ) -> None:
        worksheet = cls.get_worksheet(
            sheet_id=sheet_id,
            sheet_name=sheet_name,
        )
        mapping_dict = cls.mapping_fields()
        update_batch = []

        for object in list_object:
            model_dict = object.model_dump(mode="json")

            for k, v in mapping_dict.items():
                update_batch.append(
                    {
                        "range": f"{v}{object.index}",
                        "values": [[model_dict[k]]],
                    }
                )

        if len(list_object) > 0:
            worksheet.batch_update(update_batch)

    def update(
        self,
    ) -> None:
        mapping_dict = self.mapping_fields()
        model_dict = self.model_dump(mode="json")

        worksheet = self.get_worksheet(
            sheet_id=self.sheet_id, sheet_name=self.sheet_name
        )

        update_batch = []
        for k, v in mapping_dict.items():
            update_batch.append(
                {
                    "range": f"{v}{self.index}",
                    "values": [[model_dict[k]]],
                }
            )

        worksheet.batch_update(update_batch)


class Product(ColSheetModel):
    # highlight: Annotated[str, {COL_META_FIELD_NAME: "A"}]
    CHECK: Annotated[int, {COL_META_FIELD_NAME: "B"}]
    Product_name: Annotated[str, {COL_META_FIELD_NAME: "C"}]
    Note: Annotated[str | None, {COL_META_FIELD_NAME: "D"}] = None
    Last_update: Annotated[str | None, {COL_META_FIELD_NAME: "E"}] = None
    Product_link: Annotated[str, {COL_META_FIELD_NAME: "F"}]
    CHECK_PRODUCT_COMPARE: Annotated[int, {COL_META_FIELD_NAME: "G"}]
    PRODUCT_COMPARE: Annotated[str, {COL_META_FIELD_NAME: "H"}]
    DONGIAGIAM_MIN: Annotated[float, {COL_META_FIELD_NAME: "I"}]
    DONGIAGIAM_MAX: Annotated[float, {COL_META_FIELD_NAME: "J"}]
    DONGIA_LAMTRON: Annotated[int, {COL_META_FIELD_NAME: "K"}]
    IDSHEET_MIN: Annotated[str, {COL_META_FIELD_NAME: "L"}]
    SHEET_MIN: Annotated[str, {COL_META_FIELD_NAME: "M"}]
    CELL_MIN: Annotated[str, {COL_META_FIELD_NAME: "N"}]
    IDSHEET_MAX: Annotated[str | None, {COL_META_FIELD_NAME: "O"}] = None
    SHEET_MAX: Annotated[str | None, {COL_META_FIELD_NAME: "P"}] = None
    CELL_MAX: Annotated[str | None, {COL_META_FIELD_NAME: "Q"}] = None
    IDSHEET_STOCK: Annotated[str, {COL_META_FIELD_NAME: "R"}]
    SHEET_STOCK: Annotated[str, {COL_META_FIELD_NAME: "S"}]
    CELL_STOCK: Annotated[str, {COL_META_FIELD_NAME: "T"}]
    UNIT_STOCK: Annotated[int, {COL_META_FIELD_NAME: "U"}]
    MIN_UNIT_PER_ORDER: Annotated[int | None, {COL_META_FIELD_NAME: "V"}] = None
    IDSHEET_BLACKLIST: Annotated[str, {COL_META_FIELD_NAME: "w"}]
    SHEET_BLACKLIST: Annotated[str, {COL_META_FIELD_NAME: "X"}]
    CELL_BLACKLIST: Annotated[str, {COL_META_FIELD_NAME: "Y"}]
    RELAX_TIME: Annotated[int, {COL_META_FIELD_NAME: "Z"}]

    def min_price(self) -> float:
        g_client = service_account(ROOT_PATH.joinpath(os.environ["KEYS_PATH"]))

        res = g_client.http_client.values_get(
            id=self.IDSHEET_MIN, range=f"{self.SHEET_MIN}!{self.CELL_MIN}"
        )

        min_price = res.get("values", None)

        if min_price:
            return float(min_price[0][0])

        raise SheetError(
            f"{self.IDSHEET_MIN}->{self.SHEET_MIN}->{self.CELL_MIN} is None"
        )

    def max_price(self) -> float | None:
        if self.IDSHEET_MAX is None or self.SHEET_MAX is None or self.CELL_MAX is None:
            return None

        g_client = service_account(ROOT_PATH.joinpath(os.environ["KEYS_PATH"]))

        res = g_client.http_client.values_get(
            id=self.IDSHEET_MAX, range=f"{self.SHEET_MAX}!{self.CELL_MAX}"
        )
        max_price = res.get("values", None)
        if max_price:
            return float(max_price[0][0])

        return None

    def stock(self) -> int:
        g_client = service_account(ROOT_PATH.joinpath(os.environ["KEYS_PATH"]))

        res = g_client.http_client.values_get(
            id=self.IDSHEET_STOCK, range=f"{self.SHEET_STOCK}!{self.CELL_STOCK}"
        )

        stock = res.get("values", None)
        if stock:
            return int(stock[0][0])

        raise SheetError(
            f"{self.IDSHEET_MIN}->{self.SHEET_MIN}->{self.CELL_MIN} is None"
        )

    def blacklist(self) -> list[str]:
        g_client = service_account(ROOT_PATH.joinpath(os.environ["KEYS_PATH"]))

        spreadsheet = g_client.open_by_key(self.IDSHEET_BLACKLIST)

        worksheet = spreadsheet.worksheet(self.SHEET_BLACKLIST)

        blacklist = worksheet.batch_get([self.CELL_BLACKLIST])[0]
        if blacklist:
            res = []
            for blist in blacklist:
                for i in blist:
                    res.append(i)
            return res

        raise SheetError(
            f"{self.IDSHEET_BLACKLIST}->{self.IDSHEET_BLACKLIST}->{self.CELL_BLACKLIST} is None"
        )


class PlatformData(ColSheetModel):
    STT: Annotated[int, {COL_META_FIELD_NAME: "A"}]
    service_id: Annotated[str, {COL_META_FIELD_NAME: "B"}]
    service_name: Annotated[str, {COL_META_FIELD_NAME: "C"}]
    category_id: Annotated[str | None, {COL_META_FIELD_NAME: "D"}] = None
    category_name: Annotated[str, {COL_META_FIELD_NAME: "E"}]
    sub_category_id: Annotated[str | None, {COL_META_FIELD_NAME: "F"}] = None
    sub_category_name: Annotated[str | None, {COL_META_FIELD_NAME: "G"}] = None
    service_option: Annotated[str, {COL_META_FIELD_NAME: "H"}]
    product_id: Annotated[str, {COL_META_FIELD_NAME: "I"}]
    product_name: Annotated[str, {COL_META_FIELD_NAME: "J"}]
    attributes: list | None = None
    attribute_1: Annotated[str | None, {COL_META_FIELD_NAME: "K"}] = None
    attribute_1_value: Annotated[str | None, {COL_META_FIELD_NAME: "L"}] = None
    attribute_2: Annotated[str | None, {COL_META_FIELD_NAME: "M"}] = None
    attribute_2_value: Annotated[str | None, {COL_META_FIELD_NAME: "N"}] = None
    attribute_3: Annotated[str | None, {COL_META_FIELD_NAME: "O"}] = None
    attribute_3_value: Annotated[str | None, {COL_META_FIELD_NAME: "P"}] = None
    attribute_4: Annotated[str | None, {COL_META_FIELD_NAME: "Q"}] = None
    attribute_4_value: Annotated[str | None, {COL_META_FIELD_NAME: "R"}] = None
    attribute_5: Annotated[str | None, {COL_META_FIELD_NAME: "S"}] = None
    attribute_5_value: Annotated[str | None, {COL_META_FIELD_NAME: "T"}] = None
    attribute_6: Annotated[str | None, {COL_META_FIELD_NAME: "U"}] = None
    attribute_6_value: Annotated[str | None, {COL_META_FIELD_NAME: "V"}] = None
    attribute_7: Annotated[str | None, {COL_META_FIELD_NAME: "W"}] = None
    attribute_7_value: Annotated[str | None, {COL_META_FIELD_NAME: "X"}] = None
    attribute_8: Annotated[str | None, {COL_META_FIELD_NAME: "Y"}] = None
    attribute_8_value: Annotated[str | None, {COL_META_FIELD_NAME: "Z"}] = None
    attribute_9: Annotated[str | None, {COL_META_FIELD_NAME: "AA"}] = None
    attribute_9_value: Annotated[str | None, {COL_META_FIELD_NAME: "AB"}] = None
    attribute_10: Annotated[str | None, {COL_META_FIELD_NAME: "AC"}] = None
    attribute_10_value: Annotated[str | None, {COL_META_FIELD_NAME: "AD"}] = None


class NewPlatformData(BaseModel):
    STT: Annotated[int, {COL_META_FIELD_NAME: "A"}]
    service_id: Annotated[str, {COL_META_FIELD_NAME: "B"}]
    service_name: Annotated[str, {COL_META_FIELD_NAME: "C"}]
    brand_id: Annotated[str | None, {COL_META_FIELD_NAME: "D"}] = None
    brand_name: Annotated[str, {COL_META_FIELD_NAME: "E"}]
    region_id: Annotated[str, {COL_META_FIELD_NAME: "F"}]
    region_name: Annotated[str, {COL_META_FIELD_NAME: "G"}]
    service_option: Annotated[str, {COL_META_FIELD_NAME: "H"}]
    product_id: Annotated[str, {COL_META_FIELD_NAME: "I"}]
    product_name: Annotated[str, {COL_META_FIELD_NAME: "J"}]
    collections: Annotated[str, {COL_META_FIELD_NAME: "K"}]

    # attribute_1: Annotated[str | None, {COL_META_FIELD_NAME: "I"}] = None
    # attribute_1_value: Annotated[str | None, {COL_META_FIELD_NAME: "J"}] = None
    # attribute_2: Annotated[str | None, {COL_META_FIELD_NAME: "K"}] = None
    # attribute_2_value: Annotated[str | None, {COL_META_FIELD_NAME: "L"}] = None
    # attribute_3: Annotated[str | None, {COL_META_FIELD_NAME: "M"}] = None
    # attribute_3_value: Annotated[str | None, {COL_META_FIELD_NAME: "N"}] = None
    # attribute_4: Annotated[str | None, {COL_META_FIELD_NAME: "O"}] = None
    # attribute_4_value: Annotated[str | None, {COL_META_FIELD_NAME: "P"}] = None
    # attribute_5: Annotated[str | None, {COL_META_FIELD_NAME: "Q"}] = None
    # attribute_5_value: Annotated[str | None, {COL_META_FIELD_NAME: "R"}] = None
    # attribute_6: Annotated[str | None, {COL_META_FIELD_NAME: "S"}] = None
    # attribute_6_value: Annotated[str | None, {COL_META_FIELD_NAME: "T"}] = None
    # attribute_7: Annotated[str | None, {COL_META_FIELD_NAME: "U"}] = None
    # attribute_7_value: Annotated[str | None, {COL_META_FIELD_NAME: "V"}] = None
    # attribute_8: Annotated[str | None, {COL_META_FIELD_NAME: "W"}] = None
    # attribute_8_value: Annotated[str | None, {COL_META_FIELD_NAME: "X"}] = None
    # attribute_9: Annotated[str | None, {COL_META_FIELD_NAME: "Y"}] = None
    # attribute_9_value: Annotated[str | None, {COL_META_FIELD_NAME: "Z"}] = None
    # attribute_10: Annotated[str | None, {COL_META_FIELD_NAME: "AA"}] = None
    # attribute_10_value: Annotated[str | None, {COL_META_FIELD_NAME: "AB"}] = None


class SOffer(ColSheetModel):
    Check: Annotated[str, {COL_META_FIELD_NAME: "B"}]
    Note: Annotated[str | None, {COL_META_FIELD_NAME: "C"}] = None
    Timeline: Annotated[str | None, {COL_META_FIELD_NAME: "D"}] = None
    Offer_ID: Annotated[str | None, {COL_META_FIELD_NAME: "E"}] = None
    ADMIN: Annotated[str | None, {COL_META_FIELD_NAME: "F"}] = None
    SELLER: Annotated[str | None, {COL_META_FIELD_NAME: "G"}] = None
    Type_of_Product: Annotated[str, {COL_META_FIELD_NAME: "H"}]
    ProductID: Annotated[str, {COL_META_FIELD_NAME: "I"}]
    Title: Annotated[str, {COL_META_FIELD_NAME: "J"}]
    Description: Annotated[str, {COL_META_FIELD_NAME: "K"}]
    min_qty: Annotated[int, {COL_META_FIELD_NAME: "L"}]
    api_qty: Annotated[int, {COL_META_FIELD_NAME: "M"}]
    low_stock_alert_qty: Annotated[int | None, {COL_META_FIELD_NAME: "N"}] = 0
    currency: Annotated[str, {COL_META_FIELD_NAME: "O"}]
    unit_price: Annotated[float, {COL_META_FIELD_NAME: "P"}]
    attribute_1: Annotated[str | None, {COL_META_FIELD_NAME: "Q"}] = None
    attribute_1_value: Annotated[str | None, {COL_META_FIELD_NAME: "R"}] = None
    attribute_2: Annotated[str | None, {COL_META_FIELD_NAME: "S"}] = None
    attribute_2_value: Annotated[str | None, {COL_META_FIELD_NAME: "T"}] = None
    attribute_3: Annotated[str | None, {COL_META_FIELD_NAME: "U"}] = None
    attribute_3_value: Annotated[str | None, {COL_META_FIELD_NAME: "V"}] = None
    attribute_4: Annotated[str | None, {COL_META_FIELD_NAME: "W"}] = None
    attribute_4_value: Annotated[str | None, {COL_META_FIELD_NAME: "X"}] = None
    attribute_5: Annotated[str | None, {COL_META_FIELD_NAME: "Y"}] = None
    attribute_5_value: Annotated[str | None, {COL_META_FIELD_NAME: "Z"}] = None
    attribute_6: Annotated[str | None, {COL_META_FIELD_NAME: "AA"}] = None
    attribute_6_value: Annotated[str | None, {COL_META_FIELD_NAME: "AB"}] = None
    attribute_7: Annotated[str | None, {COL_META_FIELD_NAME: "AC"}] = None
    attribute_7_value: Annotated[str | None, {COL_META_FIELD_NAME: "AD"}] = None
    attribute_8: Annotated[str | None, {COL_META_FIELD_NAME: "AE"}] = None
    attribute_8_value: Annotated[str | None, {COL_META_FIELD_NAME: "AF"}] = None
    attribute_9: Annotated[str | None, {COL_META_FIELD_NAME: "AG"}] = None
    attribute_9_value: Annotated[str | None, {COL_META_FIELD_NAME: "AH"}] = None
    attribute_10: Annotated[str | None, {COL_META_FIELD_NAME: "AI"}] = None
    attribute_10_value: Annotated[str | None, {COL_META_FIELD_NAME: "AJ"}] = None

    def get_attribute_dict(
        self,
    ) -> dict[str, str]:
        attribute_dict: dict[str, str] = {}
        if self.attribute_1 and self.attribute_1_value:
            attribute_dict[self.attribute_1] = self.attribute_1_value
        if self.attribute_2 and self.attribute_2_value:
            attribute_dict[self.attribute_2] = self.attribute_2_value
        if self.attribute_3 and self.attribute_3_value:
            attribute_dict[self.attribute_3] = self.attribute_3_value
        if self.attribute_4 and self.attribute_4_value:
            attribute_dict[self.attribute_4] = self.attribute_4_value
        if self.attribute_5 and self.attribute_5_value:
            attribute_dict[self.attribute_5] = self.attribute_5_value
        if self.attribute_6 and self.attribute_6_value:
            attribute_dict[self.attribute_6] = self.attribute_6_value
        if self.attribute_7 and self.attribute_7_value:
            attribute_dict[self.attribute_7] = self.attribute_7_value
        if self.attribute_8 and self.attribute_8_value:
            attribute_dict[self.attribute_8] = self.attribute_8_value
        if self.attribute_9 and self.attribute_9_value:
            attribute_dict[self.attribute_9] = self.attribute_9_value
        if self.attribute_10 and self.attribute_10_value:
            attribute_dict[self.attribute_10] = self.attribute_10_value

        return attribute_dict
