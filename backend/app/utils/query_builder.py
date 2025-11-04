from typing import List, Dict, Any, Optional
from datetime import datetime

class KQLQueryBuilder:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.filters: List[str] = []
        self.aggregations: List[str] = []
        self.extends: List[str] = []
        self.summarize: Optional[str] = None
        self.order_by: Optional[str] = None

    def add_time_filter(self, field: str, start: datetime, end: datetime):
        start_iso = start.isoformat()
        end_iso = end.isoformat()
        self.filters.append(f"{field} >= datetime('{start_iso}') and {field} <= datetime('{end_iso}')")
        return self

    def add_field_filter(self, field: str, value: Any):
        if isinstance(value, str):
            self.filters.append(f"{field} == '{value}'")
        elif value is None:
            self.filters.append(f"isnull({field})")
        else:
            self.filters.append(f"{field} == {value}")
        return self

    def add_in_filter(self, field: str, values: List[Any]):
        safe_values = [f"'{v}'" if isinstance(v, str) else str(v) for v in values]
        self.filters.append(f"{field} in ({', '.join(safe_values)})")
        return self

    def add_extend(self, extend_expr: str):
        self.extends.append(extend_expr)
        return self

    def add_aggregation(self, aggregation_expr: str):
        self.aggregations.append(aggregation_expr)
        return self

    def set_summarize(self, summarize_expr: str):
        self.summarize = summarize_expr
        return self

    def set_order_by(self, order_by_expr: str):
        self.order_by = order_by_expr
        return self

    def build(self) -> str:
        query = [self.table_name]
        if self.filters:
            query.append(f"| where {' and '.join(self.filters)}")
        for ext in self.extends:
            query.append(f"| extend {ext}")
        if self.aggregations:
            for agg in self.aggregations:
                query.append(f"| {agg}")
        if self.summarize:
            query.append(f"| summarize {self.summarize}")
        if self.order_by:
            query.append(f"| order by {self.order_by}")
        return '\n'.join(query)
