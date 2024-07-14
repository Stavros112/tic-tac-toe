from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

userPlayer = 'O'
aiPlayer = 'X'
boardSize = 3
numberOfSimulations = 1000

def getBoardCopy(board):
    return [row.copy() for row in board]

def hasMovesLeft(board):
    for row in board:
        if '.' in row:
            return True
    return False

def getNextMoves(currentBoard, player):
    nextMoves = []
    for y in range(boardSize):
        for x in range(boardSize):
            if currentBoard[y][x] == '.':
                boardCopy = getBoardCopy(currentBoard)
                boardCopy[y][x] = player
                nextMoves.append(boardCopy)
    return nextMoves

def hasWon(currentBoard, player):
    winningSet = [player] * boardSize
    for row in currentBoard:
        if row == winningSet:
            return True
    for y in range(boardSize):
        column = [currentBoard[x][y] for x in range(boardSize)]
        if column == winningSet:
            return True
    if [currentBoard[i][i] for i in range(boardSize)] == winningSet:
        return True
    if [currentBoard[i][boardSize - i - 1] for i in range(boardSize)] == winningSet:
        return True
    return False

def getNextPlayer(currentPlayer):
    return 'O' if currentPlayer == 'X' else 'X'

def getBestNextMove(currentBoard, currentPlayer):
    evaluations = {}
    for _ in range(numberOfSimulations):
        player = currentPlayer
        boardCopy = getBoardCopy(currentBoard)
        simulationMoves = []
        nextMoves = getNextMoves(boardCopy, player)
        score = boardSize * boardSize
        while nextMoves:
            roll = random.randint(0, len(nextMoves) - 1)
            boardCopy = nextMoves[roll]
            simulationMoves.append(boardCopy)
            if hasWon(boardCopy, player):
                break
            score -= 1
            player = getNextPlayer(player)
            nextMoves = getNextMoves(boardCopy, player)
        firstMove = simulationMoves[0]
        firstMoveKey = repr(firstMove)
        if player == userPlayer and hasWon(boardCopy, player):
            score *= -1
        if firstMoveKey in evaluations:
            evaluations[firstMoveKey] += score
        else:
            evaluations[firstMoveKey] = score
    bestMove = max(evaluations, key=evaluations.get)
    return eval(bestMove)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    currentBoard = data['board']
    currentPlayer = data['currentPlayer']
    nextBoard = getBestNextMove(currentBoard, currentPlayer)
    nextPlayer = getNextPlayer(currentPlayer)
    return jsonify({'board': nextBoard, 'nextPlayer': nextPlayer})

if __name__ == '__main__':
    app.run(debug=True)
