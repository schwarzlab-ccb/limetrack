from __future__ import annotations
from dash_app_2.app.utils.schemas import Filter
from typing import Optional
import pandas as pd



class AppState:
    def __init__(self, state: dict):
        self._datasets: dict[str, pd.DataFrame] = {}
        self._filters: dict[str, Filter] = {}
        self._unserialize(state)

    @property
    def state(self) -> dict:
        state = self._serialize()

        return state
    
    @classmethod
    def initialize(cls: type[AppState]) -> AppState:
        state = AppState({
            "filters": {},
            "datasets": {},
        })

        return state
    
    def _unserialize(self, state: dict):
        if "filters" not in state or "datasets" not in state:
            raise ValueError("App state must contain 'datasets' and 'filters' keys.")
        
        self._datasets = {
            name: pd.DataFrame.from_records(records)
            for name, records in state["datasets"].items()
        }
        self._filters = {
            name: Filter(**filter_) for name, filter_ in state["filters"].items()
        }

    def _serialize(self) -> dict:
        serialized = dict(
            filters={
                name:filter_.model_dump() for name, filter_ in self._filters.items()
            },
            datasets={
                name:dataset.to_dict("records") for name, dataset in self._datasets.items()
            }
        )

        return serialized

    def add_filter(
        self,
        name: str,
        options: list[str],
        selected: list[str],
        mappings: Optional[dict] = None,
        overwrite: bool = False
    ):
        if name in self._filters and not overwrite:
            raise ValueError(f"Filter with name '{name}' already exsits")
        
        new_filter = Filter(
            options=options,
            selected=selected,
            mappings=mappings
        )

        self._filters[name] = new_filter

    def update_filter_selection(
        self, name: str, selected: str | list[str], select_delta: bool = False
    ):
        filter_ = self._filters.get(name)

        if not filter_:
            raise ValueError(f"Filter with name '{name}' not in state")
        
        if select_delta:
            selected = list(set(filter_.options) - set(selected))

        if isinstance(selected, str):
            selected = [selected]

        self._filters[name] = Filter(
            options=filter_.options,
            selected=selected,
            mappings=filter_.mappings
        )

    def get_filter(self, name: str) -> Filter:
        filter_ = self._filters.get(name)

        if not filter_:
            raise ValueError(f"Filter with name '{name}' not in state")
        
        return filter_
        
    def add_dataset(self, name: str, dataset: pd.DataFrame, overwrite: bool = False):
        if name in self._datasets:
            raise ValueError(f"Dataset with name '{name}' already exists")

        if not isinstance(dataset, pd.DataFrame) and not overwrite:
            raise ValueError("You must add a pandas dataframe as dataset.")
        
        self._datasets[name] = dataset

    def get_dataset(self, name: str) -> pd.DataFrame:
        dataset = self._datasets.get(name)

        if dataset is None:
            raise ValueError(f"Dataset with name '{name}' does not exist")
        
        return dataset
