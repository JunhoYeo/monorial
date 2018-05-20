#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def getTileData(tile, game):
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
    # game.revealed 확인
    if tile in game.revealed:
        tile_data.append('known')
    else:
        tile_data.append('unknown')
    return tile_data

class newGame:
    def __init__(self):
        self.deck = []
        for tile in range(26):
            self.deck.append(tile) # 덱에 타일들을 채움 
        self.revealed = [] # 공개된 타일을 이곳에 저장한 뒤 하나씩 맞춰보는 식으로 한다
        self.player1tiles = [] # player 1 패 
        self.player2tiles = [] # player 2 패 

    def updatePlayerTiles(self, playerNum, player):
        if playerNum == 1:
            self.player1tiles = player.tiles
        else:
            self.player2tiles = player.tiles 
        # 사용자 타일 정보를 업데이트 
    
    def updateAll(self, player1, player2):
        self.updatePlayerTiles(1, player1)
        self.updatePlayerTiles(2, player2)

class ai:
    def __init__(self, _playerNum):
        self.playerNum = _playerNum # 해당 ai의 플레이어 번호 
        self.tiles = [] # 해당 ai가 가진 현재 타일(패)
        # self.tiles_side = [] # 같은 인덱스의 현재 타일의 면(앞면 2/뒷면 0)
        self.tiles_view = [] # 해당 ai가 보는 게임판 위의 현재 타일 상태(0~25 index로 표현) 
        # tiles_view는 곧 신경망의 input
        self.current_tile = 'none' # 이번 턴 드로우한 타일, 없으면 none

    def getTiles(self, game):
        # deck에서 랜덤하게 4장을 골라 해당 ai의 패에 넣는다.
        newtiles = random.sample(game.deck, 4) # 랜덤하게 타일 4장 고르기 
        for tile in newtiles: 
            game.deck.remove(tile) # 덱에서 빼고 
            self.tiles.append(tile) # ai 패에 넣기
        # for tile in self.tiles:
            # self.tiles_side.append(0) # 처음에는 각 모두 뒷면(상대에게 unknown)

    def sortTiles(self, game):
        # getTiles() 실행 이후, 랜덤하게 가져온 타일을 정렬
        # 13번부터 검은 타일(검은 타일 숫자 = n-13), 12/25번 조커
        jokers = []
        for tile in self.tiles:
            if getTileData(tile, game)[1] == 'joker':
                jokers.append(tile)
                self.tiles.remove(tile) # 조커가 있을 경우 정렬 전 조커 인덱스 따로 저장
        # 정렬 시작 
        blackTiles = [] 
        for tile in self.tiles:
            if getTileData(tile, game)[0] == 'black':
                blackTiles.append(tile) # 먼저 검정 타일은 타일의 인덱스 따로 저장
        for idx, tile in enumerate(self.tiles):
            if getTileData(tile, game)[0] == 'black':
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

    def printTiles(self, game):
        tiles = ''
        for tile in self.tiles:
            tiles += str(getTileData(tile, game))
            tiles += '\n'
        return tiles
    
    def drawTiles(self, game):
        if len(game.deck) <= 0:
            return # 덱에 카드가 없으면 드로우하지 못함
        drawTile = random.choice(game.deck)
        game.deck.remove(drawTile)
        self.current_tile = drawTile # 현재 드로우한 타일을 저장(패 깔 때 필요함)
        print(str(getTileData(drawTile, game)) + '\n') # print data of drawed tile
        # game.deck에서 타일 하나를 랜덤으로 가져와 => random.choice(game.deck)
        # self.tiles.append(drawTile) # 현재 타일에 추가
        # 이 부분을 그냥 뒷부분에 추가하는 대신, 제대로 된 위치로 가게 수정해야 함
        # 어떻게? 리스트의 두 수를 비교한 뒤 색에 따라 추가할지 결정하는 식으로 가능
        # 만약 새로 가져온 타일이 조커라면 랜덤으로 넣어야 하니까 먼저 확인해야 함
        insert = 0 # 타일을 삽입한 위치 
        if (getTileData(drawTile, game)[1] == 'joker'): # 드로우한 타일이 조커 (랜덤 추가)
            insert = random.randrange(len(self.tiles)+1)
            self.tiles.insert(insert, drawTile)
            # 현재 패의 랜덤 위치에 조커를 삽입
        else: 
            # getTileData(tile, game) = [color, number, status] 
            for i in range(len(self.tiles)):
                # self.tiles의 맨 앞에 추가가 가능한지 확인
                if getTileData(self.tiles[i], game)[1] == 'joker':
                    # 현재 탐색 중인 타일이 조커면 패스 
                    continue
                if int(getTileData(self.tiles[i], game)[1]) > int(getTileData(drawTile, game)[1]):
                    # 새로 드로우한 타일이 맨 앞 타일의 수보다 크면(앞에 둘 수 있음)
                    self.tiles.insert(i, drawTile) # 원래 타일 앞에 추가
                    insert = i
                    # print('added on front' + str(getTileData(self.tiles[i], game)))
                    break
                elif int(getTileData(self.tiles[i], game)[1]) == int(getTileData(drawTile, game)[1]):
                    # 새로 드로우한 타일이 맨 앞 타일의 수와 같으면(색에 따라 앞에 둘 수 있음)                    
                    if getTileData(drawTile, game)[0] == 'white':
                        # 두 타일의 색이 다르니까 원래 있던 타일은 검은색
                        self.tiles.insert(i + 1, drawTile) 
                        insert = i + 1                       
                        # 검은색이 흰색보다 앞에 와야 하므로 원래 타일 다음 자리에 추가 
                        # print('added on next' + str(getTileData(self.tiles[i], game)))
                        break
                    else:
                        # 새로 드로우한 타일은 검은색, 원래 타일은 흰색:
                        self.tiles.insert(i, drawTile) # 원래 타일 전 자리에 추가
                        insert = i                        
                        # print('added on front' + str(getTileData(self.tiles[i], game)))
                        break
                else:
                    if i == len(self.tiles)-1: # 패에 있는 모든 타일보다도 큰 수의 타일
                        self.tiles.append(drawTile)
                        # print('added on last')
                    continue
        # self.tiles_side.insert(insert, 0)
    
    def getAiView(self, game):
        # 상대방의 타일 = 번호 + 상대 패 인덱스
        # 0(상태를 알 수 없음)
        # 1(AI가 가진 타일)
        # 2 이상(상대방이 가진 타일)
        # 모든 타일의 상태가 들어간 사이즈 26(index 0~25)의 배열을 반환하면 됨
        view = []
        for index in range(26): 
            # index는 데이터 수집이 필요한 타일의 번호 
            # index가 본인 패면 1
            # index가 game.revealed에 있으면 상대방 타일이므로 2+상대 패 index
            # 둘 다 아니면 0
            if index in self.tiles: # 본인 패 
                view.append(1)
            elif index in game.revealed: # 본인 것 아니고 공개된 패(상대 패)
                # 상대 패는 game.player(?)tiles에 있음
                # index가 game.player(?)tiles에 있으면 상대방 타일 2 + 인덱스(tile_idx)
                # (?)은 self.playerNum에 따라 결정 
                tile_idx = 0
                if self.playerNum == 1:
                    tile_idx = game.player2tiles.index(index)
                    # 상대 playerNum은 2 
                else:
                    tile_idx = game.player1tiles.index(index)
                    # 상대 playerNum은 1 
                view.append(2 + tile_idx)
            else:
                view.append(0)
        self.tile_view = view
        return view
