import csv
from dataclasses import dataclass, asdict, astuple

@dataclass
class ShoheiBattingScore:
    # define the fields for your item here like:
    game_date       : str
    at_bat          : int
    run             : int
    hit             : int
    home_run        : int
    strikeout       : int
    bb              : int
    steal           : int
    # has_saved_csv   : bool = False

    def getDict(self) -> dict :
        return asdict(self)

    def asList(self) -> list :
        return astuple(self, tuple_factory=list)

    def save2csv(self, file_path:str) -> None :
        # # csvの初回作成時のみ、ヘッダ作成
        # if self.has_saved_csv is False:
        #     self.generate_csv(file_path)
        # 行レコード追加
        try:
            with open(file_path, 'a') as f:
                # dialectの登録
                csv.register_dialect('dialect01', doublequote=True, quoting=csv.QUOTE_ALL)
                writer = csv.writer(
                    f, dialect='dialect01')
                # CSVへの書き込み
                writer.writerow(self.asList())
        
        except :
            raise FileNotFoundError("csvの保存に失敗しました")

    def generate_csv(self, file_path:str) ->  None:
        try:
            with open(file_path, 'w') as f:
                # dialectの登録
                csv.register_dialect('dialect01', doublequote=True, quoting=csv.QUOTE_ALL)
                writer = csv.writer(
                    f, dialect='dialect01')
                # CSVへの書き込み
                writer.writerow(self.getDict().keys())
            # フラグ変更
            # self.has_saved_csv = True
        
        except :
            raise FileNotFoundError("csvの生成に失敗しました")
