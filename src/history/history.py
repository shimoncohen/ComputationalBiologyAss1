import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import StringIO
from typing import Generic, List, TypeVar
from src.history.history_item import HistoryItemInterface


T = TypeVar('T', bound=HistoryItemInterface)
class History(Generic[T]):
    def __init__(self) -> None:
        self.__stack: List[T] = []

    def record(self, item: T) -> None:
        self.__stack.append(item)
    
    def get_history_csv(self) -> List[str]:
        return [self.__stack[0].get_csv_header_row(), *[item.get_as_csv_row() for item in self.__stack]]
    
    def save(self, path: str) -> None:
        csv_lines = StringIO('\n'.join(self.get_history_csv()))
        df = pd.read_csv(csv_lines, header='infer')
        df['total_rumor_percentage'] = df['total_rumors'].values / df['total_people'].values

        ax = plt.gca()
        df.plot(kind='line', xlabel='generation', ylabel='count', y='total_rumors', ax=ax)
        df.plot(kind='line', y='s1_rumors', ax=ax)
        df.plot(kind='line', y='s2_rumors', ax=ax)
        df.plot(kind='line', y='s3_rumors', ax=ax)
        df.plot(kind='line', y='s4_rumors', ax=ax)
        plt.savefig('count.png')
        plt.cla()

        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        df.plot(kind='line', xlabel='generation', y='total_rumor_percentage', ax=ax)
        plt.savefig('percentage.png')

        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Data')
        worksheet = writer.sheets['Data']
        worksheet.insert_image('N1', 'count.png')
        worksheet.insert_image('N25', 'percentage.png')
        writer.close()

        os.remove('count.png')
        os.remove('percentage.png')


    def __getitem__(self, item):
        return self.__stack[item]

