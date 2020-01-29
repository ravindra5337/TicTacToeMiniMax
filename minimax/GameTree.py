import numpy as np

class GameTree:

    def IsMovePossible(self,position):
        rowIndex=position//3
        colIndex=position%3
        return self.state[rowIndex,colIndex]==0

    def GameStateAfterMoveAt(self,position,state,curPlayer):
        nxtState=np.full((3,3),0)
        nxtState=state.copy()
        rowIndex = position // 3
        colIndex = position % 3
        nxtState[rowIndex,colIndex]=curPlayer
        return nxtState

    def IsStateAlreadyExist(self,states, state2):
        for state1 in states:
            state = state1 == state2
            state = np.reshape(state, (9, 1))
            if np.sum(state) == 9:
                return True
        return False


    def IsIdenticalStateAlreadyExistInList(self,states,curState):
        if len(states)>0:
            if not self.IsStateAlreadyExist(states, curState) and not self.IsStateAlreadyExist(states, np.flip(curState, 1)):
                rotatecount=0
                identicalState=curState
                while rotatecount<4:
                    identicalState=np.rot90(identicalState)
                    if  self.IsStateAlreadyExist(states, identicalState) or self.IsStateAlreadyExist(states,np.flip(identicalState, 1)):
                        return True
                    rotatecount+=1
            else:
                return True

        return False


    def GameBoardScore(self,state, curPlayer, nxtPlayer):
        boardScore = -1
        curPlayerRow = np.full((1, 3), curPlayer)
        nxtPlayerRow = np.full((1, 3), nxtPlayer)
        emptyBoard = np.full((3, 3), 0)
        stateTranspose = state.transpose()

        if np.sum(state == emptyBoard) == 0:
            boardScore = 0

        if boardScore == -1:

            for i in range(0, 3):
                scoreh = np.sum(state[i:i + 1, ] == curPlayerRow)
                scorev = np.sum(stateTranspose[i:i + 1, ] == curPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = curPlayer
                    break
                scoreh = np.sum(state[i:i + 1, ] == nxtPlayerRow)
                scorev = np.sum(stateTranspose[i:i + 1, ] == nxtPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = nxtPlayer
                    break

            if boardScore == -1:
                dia = state.diagonal()
                antidia = np.flip(state, 1).diagonal()
                scoreh = np.sum(dia == curPlayerRow)
                scorev = np.sum(antidia == curPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = curPlayer
                    return boardScore
                scoreh = np.sum(dia == nxtPlayerRow)
                scorev = np.sum(antidia == nxtPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = nxtPlayer
                    return boardScore

        return boardScore

    def GenerateNextBoardStates(self,plyer):
        nxtstates=[]
        for i in range(0,9):
            if self.IsMovePossible(i):
                nxtState=self.GameStateAfterMoveAt(i,self.state,plyer)
                nxtPlayer = 1
                if plyer == 1:
                    nxtPlayer = 2
                boardScore=self.GameBoardScore(nxtState,plyer,nxtPlayer)
                if boardScore==-1:
                    if not self.IsIdenticalStateAlreadyExistInList(nxtstates, nxtState):
                        nxtstates.insert(0,nxtState)
                else:
                    nxtstates=[]
                    nxtstates.insert(0,nxtState)
                    break
        return nxtstates



    def __init__(self,currentState,currentPlayer,depth):
        self.state=currentState
        self.currentPlayer=currentPlayer
        self.depth=depth
        nxtPlayer=1
        if currentPlayer==1:
            nxtPlayer=2
        boardScore= self.GameBoardScore( currentState, currentPlayer, nxtPlayer)
        if boardScore==0 or boardScore==-1:
            self.boardScore=0
        else:
            self.boardScore =boardScore * -100 if boardScore==2 else boardScore * 100
            self.boardScore =self.boardScore - depth if self.boardScore>0 else self.boardScore + depth
        self.children=[]
        if boardScore==-1:
            allNxtStates=self.GenerateNextBoardStates(nxtPlayer)
            if len(allNxtStates)>0:
                for i in allNxtStates:
                    node=GameTree(i,nxtPlayer,depth+1)
                    self.children.insert(0,node)



if __name__ == '__main__':

    def GameBoardScore(state, curPlayer, nxtPlayer):
        boardScore = -1
        curPlayerRow = np.full((1, 3), curPlayer)
        nxtPlayerRow = np.full((1, 3), nxtPlayer)
        emptyBoard = np.full((3, 3), 0)
        stateTranspose = state.transpose()

        if np.sum(state == emptyBoard) == 0:
            boardScore = 0

        if boardScore == -1:

            for i in range(0, 3):
                scoreh = np.sum(state[i:i + 1, ] == curPlayerRow)
                scorev = np.sum(stateTranspose[i:i + 1, ] == curPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = curPlayer
                    break
                scoreh = np.sum(state[i:i + 1, ] == nxtPlayerRow)
                scorev = np.sum(stateTranspose[i:i + 1, ] == nxtPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = nxtPlayer
                    break

            if boardScore == -1:
                dia = state.diagonal()
                antidia = np.flip(state, 1).diagonal()
                scoreh = np.sum(dia == curPlayerRow)
                scorev = np.sum(antidia == curPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = curPlayer
                    return boardScore
                scoreh = np.sum(dia == nxtPlayerRow)
                scorev = np.sum(antidia == nxtPlayerRow)
                if scoreh == 3 or scorev == 3:
                    boardScore = nxtPlayer
                    return boardScore

        return boardScore


    def minimax(tree,isMaximizer):
        if len(tree.children)<=0:
            return tree.boardScore
        else:
            if isMaximizer:
                minScore=2000
                for child in tree.children:
                    scr=minimax(child,False)
                    minScore=scr if scr<minScore else minScore
                return minScore
            else:
                maxScore=-2000
                for child in tree.children:
                    scr=minimax(child,True)
                    maxScore=scr if scr>maxScore else maxScore
                return maxScore


    def GetOptimalMove(currentState,prevPlayer):
        tree=GameTree(currentState,prevPlayer,0)
        nextState=np.zeros((3,3))
        if prevPlayer==2:
            maxScore = -2000
            for child in tree.children:
                scr = minimax(child, True)
                if scr>maxScore:
                    maxScore=scr
                    nextState=child.state
        else:
            minScore = 2000
            for child in tree.children:
                scr = minimax(child, False)
                if scr<minScore:
                    minScore = scr
                    nextState=child.state

        return  nextState

    currentState=np.zeros((3,3))
    currentPlayer=1
    print(currentState)
    print("------------")

    while True:
        action=input("Enter the position: ")
        rowIndex=int(action)//3
        colIndex=int(action)%3
        if rowIndex>2 or colIndex>2 or currentState[rowIndex,colIndex]!=0:
            print("Invalid Choice")
            continue
        currentState[rowIndex,colIndex]=currentPlayer
        score = GameBoardScore(currentState, currentPlayer, 2 if currentPlayer == 1 else 1)
        if score==0:
            print("Game Tied")
            break
        elif score==1 or score==2:
            winner="You" if score==1 else "AI"
            print("Winner is {0}".format(winner))
            break
        print(currentState)
        print("------------")
        currentPlayer=1 if currentPlayer==2 else 2
        pvPlayer=1 if currentPlayer==2 else 1
        print("---AI Turn---")
        currentState=GetOptimalMove(currentState,pvPlayer)
        print(currentState)
        print("------------")
        currentPlayer = 1 if currentPlayer == 2 else 2
        score=GameBoardScore(currentState,currentPlayer,2 if currentPlayer==1 else 1)

        if score==0:
            print("Game Tied")
            break
        elif score==1 or score==2:
            winner = "You" if score == 1 else "AI"
            print("Winner is {0}".format(winner))
            break
