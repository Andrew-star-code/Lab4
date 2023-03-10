import pygame as p
class GameState:
    def __init__(self):
        self.board = [
            ["--", "wp", "wp", "wp", "wp", "wp", "--"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "--"],
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteScore = 0
        self.blackScore = 0
        self.gameOver = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if self.whiteToMove:
            p.display.set_caption('Ход белых')
        else:
            p.display.set_caption('Ход черных')
        if move.isPieceEscape:
            self.board[move.endRow][move.endCol] = "--"
            if self.whiteToMove:
                self.blackScore += 1
                if self.blackScore == 5:
                    self.gameOver = True
            else:
                self.whiteScore += 1
                if self.whiteScore == 5:
                    self.gameOver = True


    def getValidMoves(self):
        moves = []
        moves = self.getAllPossibleMoves()
        return moves

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    self.getPieceMoves(r, c, moves)
        return moves

    def getPieceMoves(self, r, c, moves):
        if self.whiteToMove:
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if c + 1 <= 6:
                if self.board[r][c + 1] == "--":
                    moves.append(Move((r, c), (r, c + 1), self.board))
            if c - 1 >= 1:
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))

        else:
            if c - 1 >= 0:
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))
            if r + 1 <= 5:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))




class Move():
    ranksToRows = {"1": 6, "2": 5, "3": 4, "4": 3, "5": 2, "6": 1, "7": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.isPieceEscape = False
        if (self.pieceMoved == 'wp' and self.endRow == 6) or (self.pieceMoved == 'bp' and self.endCol == 0):
            self.isPieceEscape = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False





    def getBoardNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)




    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]