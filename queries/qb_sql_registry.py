"""
Registered QODBC SQL strings by name. Add new reports here as you go.

Inventory Valuation Summary — columns and DateMacro from your QODBC definition.
"""

from __future__ import annotations

# DateMacro was completed with a closing quote (your paste ended at 'ThisMonthToDate).
# Change to e.g. 'Today', 'ThisMonthToDate', 'ThisFiscalYearToDate' as needed.
_INVENTORY_VALUATION_SUMMARY = """sp_report InventoryValuationSummary show ItemDesc_Title, QuantityOnHand_Title, AverageCost_Title, ValueOnHand_Title, PercentOfTotalValue_Title, UnitPrice_Title, RetailValueOnHand_Title, PercentOfTotalRetail_Title, Text, Blank, ItemDesc, QuantityOnHand, AverageCost, ValueOnHand, PercentOfTotalValue, UnitPrice, RetailValueOnHand, PercentOfTotalRetail parameters DateMacro = 'ThisMonthToDate'"""

REGISTERED_SQL: dict[str, str] = {
    "usa_inventory_evaluation_summary": _INVENTORY_VALUATION_SUMMARY,
}
