import random

class newGame:
    def __init__(self):
        self.deck = []
        for tile in range(26):
            self.deck.append(tile) # 덱에 타일들을 채움 

class ai:
    def __init__(self):
        self.tiles = [] # 해당 ai가 가진 현재 타일(패)
        self.tiles_view = [] # 해당 ai가 보는 게임판 위의 현재 타일 상태(0~25 index로 표현) 
        # tiles_view는 곧 신경망의 input
        
    def getTiles(self, game):
        # deck에서 랜덤하게 4장을 골라 해당 ai의 패에 넣는다.
        newtiles = random.sample(game.deck, 4) # 랜덤하게 타일 4장 고르기 
        for tile in newtiles: 
            game.deck.remove(tile) # 덱에서 빼고 
            self.tiles.append(tile) # ai 패에 넣기

    def sortTiles(self):
        # getTiles() 실행 이후, 랜덤하게 가져온 타일을 정렬
        # 13번부터 검은 타일(검은 타일 숫자 = n-13), 12/25번 조커
        jokers = []
        for tile in self.tiles:
            if tile == 12 or tile == 25:
                jokers.append(tile)
                self.tiles.remove(tile) # 조커가 있을 경우 정렬 전 조커 인덱스 따로 저장
        # 정렬 시작 
        blackTiles = [] 
        for tile in self.tiles:
            if tile >= 13:
                blackTiles.append(tile) # 먼저 검정 타일은 타일의 인덱스 따로 저장
        for idx, tile in enumerate(self.tiles):
            if tile >= 13:
                self.tiles[idx] -= 13 # self.tiles에서는 검정 타일 원래 수만 남겨 놓고(-13)
        self.tiles.sort() # 오름차순으로 정렬
        for blackTile in blackTiles: 
            for idx, tile in enumerate(self.tiles):
                if tile == blackTile - 13:
                    self.tiles[idx] += 13 
                    # 전에 저장해 두었던 검정 타일과 같은 수인 맨 첫 번째 타일을 다시 +13
                    break
        # 정렬 끝
        # 이렇게 해 주면 색(인덱스)에 상관없이 고유의 타일 숫자로 정렬되고, 
        # 두 수가 같을 때에는 검정 타일이 먼저 오게 됨(=게임 룰과 일치)
        # ex > [16, 15, 2, 3] (3, 2, 2, 3) => [15, 2, 16, 3]
        for joker in jokers:
            self.tiles.insert(random.randrange(len(self.tiles)+1), joker)
            print('joker : ' + str(joker))
        # self.tiles의 랜덤 위치에 처음에 따로 빼 둔 조커를 끼워 넣음

    def printTile(self):
        tiles = ''
        for tile in self.tiles:
            if tile == 12: # white joker 
                tiles += str(['white', 'joker'])
            elif tile == 25: # black joker
                tiles += str(['black', 'joker'])
            elif tile >= 13: # black tile
                tiles += str(['black', tile - 13])
            else: # white tile
                tiles += str(['white', tile])
            tiles += ' '
        return tiles

if __name__ == '__main__':
    game = newGame()
    m1 = ai() # monorial 1
    m2 = ai() # monorial 2
    m1.getTiles(game)
    m1.sortTiles()
    m2.getTiles(game)
    m2.sortTiles()
    print('m1 : ' + m1.printTile())
    print('m2 : ' + m2.printTile())