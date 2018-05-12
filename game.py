#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def getTileData(tile):
    tile_data = []
    if tile == 12: # white joker 
        tile_data.append('white')
        tile_data.append('joker')
    elif tile == 25: # black joker
        tile_data.append('black')
        tile_data.append('joker')
    elif tile >= 13: # black tile
        tile_data.append('black')
        tile_data.append(tile - 13)
    else: # white tile
        tile_data.append('white')
        tile_data.append(tile)
    return tile_data

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
        self.current_tile = 'none' # 이번 턴 드로우한 타일, 없으면 none

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
            if getTileData(tile)[1] == 'joker':
                jokers.append(tile)
                self.tiles.remove(tile) # 조커가 있을 경우 정렬 전 조커 인덱스 따로 저장
        # 정렬 시작 
        blackTiles = [] 
        for tile in self.tiles:
            if getTileData(tile)[0] == 'black':
                blackTiles.append(tile) # 먼저 검정 타일은 타일의 인덱스 따로 저장
        for idx, tile in enumerate(self.tiles):
            if getTileData(tile)[0] == 'black':
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
            # print('joker : ' + str(joker))
        # self.tiles의 랜덤 위치에 처음에 따로 빼 둔 조커를 끼워 넣음

    def printTiles(self):
        tiles = ''
        for tile in self.tiles:
            tiles += str(getTileData(tile))
            tiles += ' '
        return tiles
    
    def drawTiles(self, game):
        if len(game.deck) <= 0:
            return # 덱에 카드가 없으면 드로우하지 못함
        drawTile = random.choice(game.deck)
        game.deck.remove(drawTile)
        print(str(getTileData(drawTile))) # print data of drawed tile
        # game.deck에서 타일 하나를 랜덤으로 가져와 => random.choice(game.deck)
        # self.tiles.append(drawTile) # 현재 타일에 추가
        # 이 부분을 그냥 뒷부분에 추가하는 대신, 제대로 된 위치로 가게 수정해야 함
        # 어떻게? 리스트의 두 수를 비교한 뒤 색에 따라 추가할지 결정하는 식으로 가능
        # 만약 새로 가져온 타일이 조커라면 랜덤으로 넣어야 하니까 먼저 확인해야 함
        if (getTileData(drawTile)[1] == 'joker'): # 드로우한 타일이 조커 (랜덤 추가)
            self.tiles.insert(random.randrange(len(self.tiles)+1), drawTile)
            # 현재 패의 랜덤 위치에 조커를 삽입
        else: 
            # getTileData(tile) = [color, number] 
            for i in range(len(self.tiles)):
                # self.tiles의 맨 앞에 추가가 가능한지 확인
                if getTileData(self.tiles[i])[1] == 'joker':
                    # 현재 탐색 중인 타일이 조커면 패스 
                    continue
                if int(getTileData(self.tiles[i])[1]) > int(getTileData(drawTile)[1]):
                    # 새로 드로우한 타일이 맨 앞 타일의 수보다 크면(앞에 둘 수 있음)
                    self.tiles.insert(i, drawTile) # 원래 타일 앞에 추가
                    # print('added on front' + str(getTileData(self.tiles[i])))
                    break
                elif int(getTileData(self.tiles[i])[1]) == int(getTileData(drawTile)[1]):
                    # 새로 드로우한 타일이 맨 앞 타일의 수와 같으면(색에 따라 앞에 둘 수 있음)                    
                    if getTileData(drawTile)[0] == 'white':
                        # 두 타일의 색이 다르니까 원래 있던 타일은 검은색
                        self.tiles.insert(i+1, drawTile) 
                        # 검은색이 흰색보다 앞에 와야 하므로 원래 타일 다음 자리에 추가 
                        # print('added on next' + str(getTileData(self.tiles[i])))
                        break
                    else:
                        # 새로 드로우한 타일은 검은색, 원래 타일은 흰색:
                        self.tiles.insert(i, drawTile) # 원래 타일 전 자리에 추가
                        # print('added on front' + str(getTileData(self.tiles[i])))
                        break
                else:
                    if i == len(self.tiles)-1: # 패에 있는 모든 타일보다도 큰 수의 타일
                        self.tiles.append(drawTile)
                        # print('added on last')
                    continue

if __name__ == '__main__':
    game = newGame()
    m1 = ai() # monorial 1
    m2 = ai() # monorial 2
    m1.getTiles(game)
    m1.sortTiles()
    m2.getTiles(game)
    m2.sortTiles()
    print('m1 : ' + m1.printTiles())
    print('m2 : ' + m2.printTiles())
    # game start
    while(1):
        # m1 turn => ai에 turn() 메소드 만들기
        print('m1 : draw')
        m1.drawTiles(game)
        print('m1 : ' + m1.printTiles())
        # todo
        # m1가 보는 게임판 상황 가져오기 
        # 인공신경망에 input(test)
        # output을 처리 후 행동
        # 원래 정답을 구하고 한 100번?쯤 train
        print('m2 : draw')
        m2.drawTiles(game)
        print('m2 : ' + m2.printTiles())