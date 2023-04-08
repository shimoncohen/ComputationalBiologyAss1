from typing import Generic, List, TypeVar
from src.history.history_item import HistoryItemInterface


T = TypeVar('T', bound=HistoryItemInterface)
class History(Generic[T]):
    def __init__(self) -> None:
        self.__stack: List[T] = []

    def record(self, item: T) -> None:
        self.__stack.append(item)
    
    def get_history_csv(self) -> List[str]:
        return [ self.__stack[0].get_csv_header_row(), *[item.get_as_csv_row() for item in self.__stack]]

    def __getitem__(self, item):
        return self.__stack[item]

