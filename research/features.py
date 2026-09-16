"""Quality gates applied to the feature table before any report reads it."""

from __future__ import annotations

import numpy as np
import pandas as pd

SALES_PREFIXES = ("sold_", "sell_first_day_", "sell_last_day_", "revenue_", "price_")
SALES_COLUMNS = ("sold_units_total", "sells_last_3_days")


def sales_columns(feats: pd.DataFrame) -> list[str]:
    return [c for c in feats.columns if c.startswith(SALES_PREFIXES) or c in SALES_COLUMNS]


def mask_unreliable_sales(feats: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Blank the sales columns of seats whose market replay does not reconcile to the recorded money.

    A seat is unreliable when `money_check_turns` (turns where the replica's end-of-turn money
    differs from the recording) is above zero. Returns the masked table and the rows that were
    masked, so a report can state the exclusion.
    """
    if "money_check_turns" not in feats:
        return feats, feats.iloc[0:0]
    feats = feats.copy()
    bad = feats.money_check_turns.fillna(0) > 0
    feats["sales_reliable"] = ~bad
    feats.loc[bad, sales_columns(feats)] = np.nan
    return feats, feats[bad]
