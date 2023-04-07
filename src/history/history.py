from typing import Generic, List, TypeVar
from src.history.history_item import HistoryItemInterface


T = TypeVar('T', bound=HistoryItemInterface)
class History(Generic[T]):
    def __init__(self) -> None:
        self.__stack: List[T] = []

    def record(self, item: T) -> None:
        self.__stack.append(item)
    
    def __getitem__(self, item):
        return self.__stack[item]

