from typing import List, Dict, Any, Optional
from datetime import datetime

class TokenAnalyticsService:
    def __init__(self, logs: List[Dict[str, Any]]):
        self.logs = logs

    def _build_filters(self, data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        def match(entry):
            for key, value in filters.items():
                if value is not None:
                    if key == 'data_inicio' and 'data_hora' in entry:
                        if entry['data_hora'] < value:
                            return False
                    elif key == 'data_fim' and 'data_hora' in entry:
                        if entry['data_hora'] > value:
                            return False
                    elif key in entry and entry[key] != value:
                        return False
            return True
        return [e for e in data if match(e)]

    def _group_and_summarize(self, data: List[Dict[str, Any]], group_by: List[str],
                             sum_fields: List[str]) -> List[Dict[str, Any]]:
        from collections import defaultdict
        result = defaultdict(lambda: {k: 0 for k in sum_fields})
        for entry in data:
            key = tuple(entry.get(g) for g in group_by)
            for field in sum_fields:
                result[key][field] += float(entry.get(field, 0) or 0)
        output = []
        for key, sums in result.items():
            row = {group_by[i]: key[i] for i in range(len(group_by))}
            row.update(sums)
            output.append(row)
        return output

    def tokens_by_project(self, filters: Dict[str, Any], group_by_user: bool = False) -> List[Dict[str, Any]]:
        data = self._build_filters(self.logs, filters)
        group_by = ['projeto']
        if group_by_user:
            group_by.append('usuario_executor')
        return self._group_and_summarize(data, group_by, ['tokens_entrada', 'tokens_saida'])

    def tokens_by_tipo_analise(self, filters: Dict[str, Any], group_by_user: bool = False) -> List[Dict[str, Any]]:
        data = self._build_filters(self.logs, filters)
        group_by = ['tipo_analise']
        if group_by_user:
            group_by.append('usuario_executor')
        return self._group_and_summarize(data, group_by, ['tokens_entrada', 'tokens_saida'])

    def tokens_by_day(self, filters: Dict[str, Any], group_by_user: bool = False) -> List[Dict[str, Any]]:
        data = self._build_filters(self.logs, filters)
        for entry in data:
            if 'data_hora' in entry:
                entry['dia'] = entry['data_hora'].strftime('%Y-%m-%d')
            else:
                entry['dia'] = None
        group_by = ['dia']
        if group_by_user:
            group_by.append('usuario_executor')
        return self._group_and_summarize(data, group_by, ['tokens_entrada', 'tokens_saida'])

    def tokens_by_model(self, filters: Dict[str, Any], group_by_user: bool = False) -> List[Dict[str, Any]]:
        data = self._build_filters(self.logs, filters)
        group_by = ['model_name']
        if group_by_user:
            group_by.append('usuario_executor')
        return self._group_and_summarize(data, group_by, ['tokens_entrada', 'tokens_saida'])

    def tokens_by_model_time(self, filters: Dict[str, Any], group_by_user: bool = False) -> List[Dict[str, Any]]:
        data = self._build_filters(self.logs, filters)
        for entry in data:
            if 'data_hora' in entry:
                entry['dia'] = entry['data_hora'].strftime('%Y-%m-%d')
            else:
                entry['dia'] = None
        group_by = ['model_name', 'dia']
        if group_by_user:
            group_by.append('usuario_executor')
        return self._group_and_summarize(data, group_by, ['tokens_entrada', 'tokens_saida'])
