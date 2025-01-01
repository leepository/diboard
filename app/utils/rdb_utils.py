from operator import and_, or_
from typing import List, Dict, Any

class DynamicFilter:
    def __init__(self, model_class):
        self.model_class = model_class
        self.operations = {
            'eq': lambda c, v: c == v,
            'ne': lambda c, v: c != v,
            'gt': lambda c, v: c > v,
            'gte': lambda c, v: c >= v,
            'lt': lambda c, v: c < v,
            'lte': lambda c, v: c <= v,
            'like': lambda c, v: c.like(f"%{v}%"),
            'in': lambda c, v: c.in_(v),
            'between': lambda c, v: c.between(v[0], v[1])
        }

    def apply_filters(self, query, filters: List[Dict[str, Any]]):
        """
        Apply multiple filters to a query
        filters format
        [
            {
                "field": "name",
                "op": "like",
                "value": "shirt"
            },
            {
                "field": "price",
                "op": "between",
                "value": [10, 50
            }
        ]
        """
        conditions = []

        for filter_dict in filters:
            field = filter_dict.get('field')
            op = filter_dict.get('op')
            value = filter_dict.get('value')

            if not all([field, op, value]) or op not in self.operations:
                continue

            column = getattr(self.model_class, field, None)
            if column is None:
                continue

            try:
                condition = self.operations[op](column, value)
                conditions.append(condition)
            except Exception as e:
                print(f"[EX] rdb_utils.DynamicFilter : ", str(e.args))
                continue

        if conditions:
            return query.filter(and_(*conditions))