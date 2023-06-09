import io
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import StringIO
from typing import Generic, List, TypeVar
from src.history.history_item import HistoryItemInterface


T = TypeVar('T', bound=HistoryItemInterface)
class History(Generic[T]):
    """
    Describes the chain of events in the simulation.

    Args:
        Generic (HistoryItemInterface): type of history item that should be stored
    """
    def __init__(self) -> None:
        self.__stack: List[T] = []

    def record(self, item: T) -> None:
        self.__stack.append(item)
    
    def get_history_csv(self) -> List[str]:
        return [self.__stack[0].get_csv_header_row(), *[item.get_as_csv_row() for item in self.__stack]]
    
    def save(self, path: str) -> None:
        """
        Save the history description and corresponding graphs.

        Args:
            path (str): path to the wanted output destination
        """
        csv_lines = StringIO('\n'.join(self.get_history_csv()))
        df = pd.read_csv(csv_lines, header='infer')
        df['total_rumor_percentage'] = (df['total_rumors'].values / df['total_people'].values) * 100
        df['total_affected_percentage'] = (df['total_affected'].values / df['total_people'].values) * 100

        # Plot rumor count graph
        ax = plt.gca()
        df.plot(kind='line', xlabel='generation', ylabel='count', y='total_rumors', ax=ax)
        df.plot(kind='line', y='s1_rumors', ax=ax)
        df.plot(kind='line', y='s2_rumors', ax=ax)
        df.plot(kind='line', y='s3_rumors', ax=ax)
        df.plot(kind='line', y='s4_rumors', ax=ax)
        
        # From: https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png')
        plt.cla()

        # Plot rumor percentage graph
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        df.plot(kind='line', xlabel='generation', y='total_rumor_percentage', ax=ax)
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        plt.cla()

        # Plot total affected percentage graph
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        df.plot(kind='line', xlabel='generation', y='total_affected_percentage', ax=ax)
        buffer3 = io.BytesIO()
        plt.savefig(buffer3, format='png')
        plt.cla()

        # Create parent directories
        Path(path).parent.mkdir(parents=True, exist_ok=True, mode=666)

        # Create excel file and save graphs
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Data')
        worksheet = writer.sheets['Data']
        # From: https://xlsxwriter.readthedocs.io/worksheet.html#insert_image
        worksheet.insert_image('N1', 'image.png', {'image_data': buffer1})
        worksheet.insert_image('N25', 'image.png', {'image_data': buffer2})
        worksheet.insert_image('N50', 'image.png', {'image_data': buffer3})
        writer.close()


    def __getitem__(self, item):
        return self.__stack[item]

