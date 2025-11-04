from typing import List, Dict

class DataAggregationService:
    """
    Serviço para transformar dados brutos do Application Insights em estruturas para Chart.js
    """

    @staticmethod
    def aggregate_for_bar_chart(data: List[dict], label_field: str = 'label', value_field: str = 'value') -> Dict:
        labels = []
        values = []
        for item in data:
            labels.append(str(item.get(label_field, '')))
            values.append(float(item.get(value_field, 0)))
        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Tokens",
                    "backgroundColor": "#011334",
                    "borderColor": "#E1FF00",
                    "data": values
                }
            ]
        }

    @staticmethod
    def aggregate_for_pie_chart(data: List[dict], label_field: str = 'label', value_field: str = 'value') -> Dict:
        labels = []
        values = []
        for item in data:
            labels.append(str(item.get(label_field, '')))
            values.append(float(item.get(value_field, 0)))
        colors = [
            "#011334", "#E1FF00", "#D8E8EE", "#F5F5F5", "#677185", "#99A1AE", "#CCD0D6", "#F3FF99", "#F9FFCC"
        ]
        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Tokens",
                    "backgroundColor": colors[:len(labels)],
                    "data": values
                }
            ]
        }
