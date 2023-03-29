from stone import ReversiStone


"""
ToDo
コマをおける場所の提案
パスの実施
最後の点数計算
"""
class ReversiModel:

    def __init__(self):
        """
        初期化
        """
        # 全てEMPTYで盤面を作成
        self.__board = [ReversiStone.EMPTY] * 100
        self.__turn = ReversiStone.BLACK

        # BLACKとWHITEのコマを配置
        self.__board[44] = ReversiStone.WHITE
        self.__board[45] = ReversiStone.BLACK
        self.__board[54] = ReversiStone.BLACK
        self.__board[55] = ReversiStone.WHITE

        # WALLを設定
        for i in range(10):
            self.__board[i] = ReversiStone.WALL
            self.__board[90 + i] = ReversiStone.WALL
            self.__board[10 * i] = ReversiStone.WALL
            self.__board[10 * i + 9] = ReversiStone.WALL

        # 候補を探索
        current_stone_kind = self.__turn
        self.__search_candidate(current_stone_kind)


    @property
    def board(self):
        return self.__board
    
    @property
    def turn(self):
        return self.__turn
        

    def put(self, i_board: int) -> bool:
        """
        盤面のi_boardに(BLACK or WHITE : stone_kind)のコマを置き、
        同じ色ではさんでいるマスをひっくり返す
        1. ひっくり返したらTrue、返せなければFalseを返す
        2. 次のコマの種類を返す
        """
        # Early return
        if self.__board[i_board] != ReversiStone.CANDIDATE:
            return False
        
        # コマをひっくり返す
        current_stone_kind = self.__turn
        i_turns = self.__flip_list(i_board, current_stone_kind)
        self.__board[i_board] = current_stone_kind
        for i_turn in i_turns:
            self.__board[i_turn] = current_stone_kind

        # 次のコマを置ける候補を探す
        reverse_stone_kind = self.__get_reverse_stone_kind(self.__turn)
        is_find_candidate = self.__search_candidate(reverse_stone_kind)

        # 候補が見つかったので、次は反対の色のプレイヤーのターン
        if is_find_candidate:
            self.__turn = reverse_stone_kind
            return True
        
        # 候補が見つからなかったので、反対の色のターンはスキップされ、同じプレイヤーの候補を再検索する
        current_stone_kind = self.__get_reverse_stone_kind(reverse_stone_kind)
        is_find_candidate = self.__search_candidate(current_stone_kind)

        # 候補が見つかったので、次も自分のターン
        if is_find_candidate:
            self.__turn = current_stone_kind
            return True
        
        # どちらの色の候補も見つからなかったのでゲーム終了
        return True
    

    def __search_candidate(self, next_stone_kind: ReversiStone) -> bool:
        """
        次のターンの人が置ける場所を置ける場所を探索する
        次のターンの人が置ける場所があればTrue、なければFalseを返す
        """
        # 現在の候補を空に
        for i, stone_kind in enumerate(self.__board.copy()):
            if stone_kind == ReversiStone.CANDIDATE:
                self.__board[i] = ReversiStone.EMPTY

        # 次の候補を探す
        is_find_candidate = False
        for i, stone_kind in enumerate(self.__board.copy()):
            if self.__can_put(i, next_stone_kind):
                is_find_candidate = True
                self.__board[i] = ReversiStone.CANDIDATE

        return is_find_candidate


    def __get_reverse_stone_kind(self, stone_kind: ReversiStone) -> ReversiStone:
        """
        反対のコマの種類を取得
        """
        if stone_kind == ReversiStone.BLACK:
            return ReversiStone.WHITE
        else:
            return ReversiStone.BLACK
        

    def __can_put(self, i_board: int, put_stone_kind: ReversiStone) -> bool:
        """
        盤面のi_boardにput_stone_kind(BLACK or WHITE)のコマを置けるかどうか
        置けるならTrue、置けなければFalseを返す
        """
        i_turns = self.__flip_list(i_board, put_stone_kind)
        if i_turns:
            return True
        else:
            return False

    
    def __flip_list(self, i_board: int, put_stone_kind: ReversiStone):
        """
        盤面のi_boardにput_stone_kind(BLACK or WHITE)を置いたときに、
        ひっくり返されるマスのリストを返す
        """
        # 候補以外なら空のリストを返す
        if self.__board[i_board] not in [ReversiStone.EMPTY, ReversiStone.CANDIDATE]:
            return []

        # 相手のコマ
        if put_stone_kind == ReversiStone.WHITE:
            enemy_stone_kind = ReversiStone.BLACK
        else:
            enemy_stone_kind = ReversiStone.WHITE

        # ひっくり返されるマスのリスト
        i_turns = []

        # 方向パラメータ
        UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
        RIGHT_UP, RIGHT_DOWN, LEFT_UP, LEFT_DOWN = RIGHT+UP, RIGHT+DOWN, LEFT+UP, LEFT+DOWN
        
        # 8方向を走査
        for v in (RIGHT, RIGHT_UP, UP, LEFT_UP, LEFT, LEFT_DOWN, DOWN, RIGHT_DOWN):
            # ひっくり返す候補
            temp = []

            # i_boardとの差
            delta = v

            # 敵のコマである限り、ひっくり返す候補に加え続ける
            while self.__board[i_board + delta] == enemy_stone_kind:
                temp.append(i_board + delta)
                delta += v
            
            # 敵のコマのあとが自分のコマなら候補を確定する
            if self.__board[i_board + delta] == put_stone_kind:
                i_turns += temp

        return i_turns