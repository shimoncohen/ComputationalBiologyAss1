class HistoryItemInterface:
    @staticmethod
    def get_csv_header_row() -> str:
        """Get the header row describing the history item data."""
        pass

    def get_as_csv_row(self) -> str:
        """Get the data in csv format."""
        pass


class RumorHistoryItem(HistoryItemInterface):
    def __init__(self, s_counts, s_rumor_counts) -> None:
        super().__init__()

        self.__s_counts = s_counts
        self.__total_people = sum(self.__s_counts)

        self.__s_rumor_counts = s_rumor_counts
        self.__total_rumors = sum(self.__s_rumor_counts)
    
    @staticmethod
    def get_csv_header_row() -> str:
        return 'total_people,s1_count,s2_count,s3_count,s4_count,total_rumors,s1_rumors,s2_rumors,s3_rumors,s4_rumors'

    def get_as_csv_row(self) -> str:
        people_str = ",".join(map(str, self.__s_counts))
        rumor_str = ",".join(map(str, self.__s_rumor_counts))
        return f'{self.__total_people},{people_str},{self.__total_rumors},{rumor_str}'
