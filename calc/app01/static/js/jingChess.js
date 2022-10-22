var origBoard;
const huPlayer = 'O';
const aiPlayer = 'X';
const winCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [6, 4, 2]
]
/*获取元素*/
const cells = document.querySelectorAll(".cell");
startGame();

function startGame () {
    document.querySelector(".endgame").style.display = "none";
    //设置阵列点  创建9个数组元素，元素的键0到8
    origBoard = Array.from(Array(9).keys());
    //	console.log(origBoard);
    for (var i = 0; i < cells.length; i++) {
        //把文本先设置为空
        cells[i].innerHTML = "";
        //删除属性知道已经有人赢了
        cells[i].style.removeProperty('background-color');
        //点击方块
        cells[i].addEventListener('click', turnClick, false);
    }
}

function turnClick (square) {
    //记住原来走过的方块
    if (typeof origBoard[square.target.id] == 'number') {
        //人类玩家点击
        turn(square.target.id, huPlayer);
        //由人类转向AI玩家
        if (!checkTie()) {
            //电脑玩家将棋子放到最合适的地方
            turn(bestStep(), aiPlayer);
        }
    }

}

function turn (squareId, player) {
    //这些id给玩家
    origBoard[squareId] = player;
    document.getElementById(squareId).innerHTML = player;
    //让游戏进行检查
    var gameWin = checkWin(origBoard, player);
    if (gameWin) {
        gameOver(gameWin);
    }
}
//判断胜利
function checkWin (board, player) {
    let plays = board.reduce((a, e, i) =>
        (e === player) ? a.concat(i) : a, [])
    let gameWin = null;
    //如果是属于之前winCombos胜利组合
    for (let [index, win] of winCombos.entries()) {
        if (win.every(Element => plays.indexOf(Element) > -1)) {
            //现在我们知道是哪一个组合胜利了
            gameWin = { index: index, player: player };
            break;
        }
    }
    return gameWin;
}
/*游戏结束*/
function gameOver (gameWin) {
    for (let index of winCombos[gameWin.index]) {
        //人类获胜则为蓝色
        document.getElementById(index).style.backgroundColor =
            gameWin.player == huPlayer ? "blue" : "red";
    }
    /*事件侦听器删除单击，已经结束了，不能再点击*/
    for (var i = 0; i < cells.length; i++) {
        cells[i].removeEventListener('click', turnClick, false);
    }
    declareWinner(gameWin.player == huPlayer ? "你赢了" : "你输了");
}

function emptySquares () {
    //过滤每一个元素,如果元素为number，返回所有方块
    return origBoard.filter(s => typeof s == 'number');
}

/*AI最优步骤*/
function bestStep () {
    //智能AI
    return minmax(origBoard, aiPlayer).index;
}
//检查是否是平局
function checkTie () {
    if (emptySquares().length == 0) {
        for (var i = 0; i < cells.length; i++) {
            cells[i].style.backgroundColor = "green";
            cells[i].removeEventListener('click', turnClick, false);
        }
        //谁获胜了
        // declareWinner("玩家获胜");
        return true;
    } else {
        //平局
        return false;
    }

}

function declareWinner (who) {
    document.querySelector(".endgame").style.display = 'block';
    document.querySelector(".endgame .text").innerHTML = who;
}

function minmax (newBoard, player) {
    //找到索引，空方块功能设置为a
    var availSpots = emptySquares(newBoard);

    if (checkWin(newBoard, player)) {
        return { score: -10 };
    } else if (checkWin(newBoard, aiPlayer)) {
        return { score: 20 };
    } else if (availSpots.length === 0) {
        return { score: 0 };
    }
    //之后进行评估
    var moves = [];
    //收集每个动作时的空白点
    for (var i = 0; i < availSpots.length; i++) {
        //然后设置空的索引号
        var move = {};
        move.index = newBoard[availSpots[i]];
        newBoard[availSpots[i]] = player;

        if (player == aiPlayer) {
            //存储对象，包括得分属性
            var result = minmax(newBoard, huPlayer);
            move.score = result.score;
        } else {
            //存储对象，包括得分属性
            var result = minmax(newBoard, aiPlayer);
            move.score = result.score;
        }

        newBoard[availSpots[i]] = move.index;

        moves.push(move);
    }
    var bestMove;
    //如果是AI玩家，以非常低的数字和循环通过
    if (player === aiPlayer) {
        var bestScore = -1000;
        for (var i = 0; i < moves.length; i++) {
            if (moves[i].score > bestScore) {
                bestScore = moves[i].score;
                bestMove = i;
            }
        }
    } else {
        var bestScore = 1000;
        for (var i = 0; i < moves.length; i++) {
            if (moves[i].score < bestScore) {
                bestScore = moves[i].score;
                bestMove = i;
            }
        }
    }

    return moves[bestMove];
}