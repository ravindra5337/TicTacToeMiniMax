import numpy as np

class GameTree:

    def __init__(self, current_state, current_player, depth):
        self.state = current_state
        self.currentPlayer = current_player
        self.depth = depth
        nxt_player = 1
        if current_player == 1:
            nxt_player = 2
        board_score = self.game_board_score(current_state, current_player, nxt_player)
        if board_score == 0 or board_score == -1:
            self.board_score = 0
        else:
            self.board_score = board_score * -100 if board_score == 2 else board_score * 100
            self.board_score = self.board_score - depth if self.board_score > 0 else self.board_score + depth
        self.children = []
        if board_score == -1:
            all_nxt_states = self.generate_next_board_states(nxt_player)
            if len(all_nxt_states) > 0:
                for i in all_nxt_states:
                    node = GameTree(i, nxt_player, depth + 1)
                    self.children.insert(0, node)

    def is_move_possible(self, position):
        row_index=position//3
        col_index=position%3
        return self.state[row_index,col_index]==0

    def get_game_state_after_move(self, position, state, cur_player):
        nxt_state=np.full((3,3),0)
        nxt_state=state.copy()
        row_index = position // 3
        col_index = position % 3
        nxt_state[row_index,col_index]=cur_player
        return nxt_state

    def is_state_already_exist(self, states, state2):
        for state1 in states:
            state = state1 == state2
            state = np.reshape(state, (9, 1))
            if np.sum(state) == 9:
                return True
        return False


    def is_mirror_state_already_exist(self, states, cur_state):
        if len(states)>0:
            if not self.is_state_already_exist(states, cur_state) and not self.is_state_already_exist(states, np.flip(cur_state, 1)):
                rotate_count=0
                identical_state=cur_state
                while rotate_count<4:
                    identical_state=np.rot90(identical_state)
                    if  self.is_state_already_exist(states, identical_state) or self.is_state_already_exist(states, np.flip(identical_state, 1)):
                        return True
                    rotate_count+=1
            else:
                return True

        return False


    def game_board_score(self, state, cur_player, nxt_player):
        board_score = -1
        cur_player_row = np.full((1, 3), cur_player)
        nxt_player_row = np.full((1, 3), nxt_player)
        empty_board = np.full((3, 3), 0)
        state_transpose = state.transpose()

        if np.sum(state == empty_board) == 0:
            board_score = 0

        if board_score == -1:

            for i in range(0, 3):
                scoreh = np.sum(state[i:i + 1, ] == cur_player_row)
                scorev = np.sum(state_transpose[i:i + 1, ] == cur_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = cur_player
                    break
                scoreh = np.sum(state[i:i + 1, ] == nxt_player_row)
                scorev = np.sum(state_transpose[i:i + 1, ] == nxt_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = nxt_player
                    break

            if board_score == -1:
                dia = state.diagonal()
                antidia = np.flip(state, 1).diagonal()
                scoreh = np.sum(dia == cur_player_row)
                scorev = np.sum(antidia == cur_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = cur_player
                    return board_score
                scoreh = np.sum(dia == nxt_player_row)
                scorev = np.sum(antidia == nxt_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = nxt_player
                    return board_score

        return board_score

    def generate_next_board_states(self, plyer):
        nxt_states=[]
        for i in range(0,9):
            if self.is_move_possible(i):
                nxt_state=self.get_game_state_after_move(i, self.state, plyer)
                nxt_player = 1
                if plyer == 1:
                    nxt_player = 2
                board_score=self.game_board_score(nxt_state, plyer, nxt_player)
                if board_score==-1:
                    if not self.is_mirror_state_already_exist(nxt_states, nxt_state):
                        nxt_states.insert(0,nxt_state)
                else:
                    nxt_states=[]
                    nxt_states.insert(0,nxt_state)
                    break
        return nxt_states





if __name__ == '__main__':

    def game_board_score(state, cur_player, nxt_player):
        board_score = -1
        cur_player_row = np.full((1, 3), cur_player)
        nxt_player_row = np.full((1, 3), nxt_player)
        empty_board = np.full((3, 3), 0)
        state_transpose = state.transpose()

        if np.sum(state == empty_board) == 0:
            board_score = 0

        if board_score == -1:

            for i in range(0, 3):
                scoreh = np.sum(state[i:i + 1, ] == cur_player_row)
                scorev = np.sum(state_transpose[i:i + 1, ] == cur_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = cur_player
                    break
                scoreh = np.sum(state[i:i + 1, ] == nxt_player_row)
                scorev = np.sum(state_transpose[i:i + 1, ] == nxt_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = nxt_player
                    break

            if board_score == -1:
                dia = state.diagonal()
                antidia = np.flip(state, 1).diagonal()
                scoreh = np.sum(dia == cur_player_row)
                scorev = np.sum(antidia == cur_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = cur_player
                    return board_score
                scoreh = np.sum(dia == nxt_player_row)
                scorev = np.sum(antidia == nxt_player_row)
                if scoreh == 3 or scorev == 3:
                    board_score = nxt_player
                    return board_score

        return board_score


    def minimax(tree, is_maximizer):
        if len(tree.children)<=0:
            return tree.board_score
        else:
            if is_maximizer:
                min_score=2000
                for child in tree.children:
                    scr=minimax(child,False)
                    min_score=scr if scr<min_score else min_score
                return min_score
            else:
                max_score=-2000
                for child in tree.children:
                    scr=minimax(child,True)
                    max_score=scr if scr>max_score else max_score
                return max_score


    def get_optimal_move(currentState, prev_player):
        tree=GameTree(currentState, prev_player, 0)
        next_state=np.zeros((3,3))
        if prev_player==2:
            max_score = -2000
            for child in tree.children:
                scr = minimax(child, True)
                if scr>max_score:
                    max_score=scr
                    next_state=child.state
        else:
            min_score = 2000
            for child in tree.children:
                scr = minimax(child, False)
                if scr<min_score:
                    min_score = scr
                    next_state=child.state

        return  next_state

    current_state=np.zeros((3, 3))
    current_player=1
    print(current_state)
    print("------------")

    while True:
        action=input("Enter the position: ")
        row_index= int(action) // 3
        col_index= int(action) % 3
        if row_index>2 or col_index>2 or current_state[row_index, col_index]!=0:
            print("Invalid Choice")
            continue
        current_state[row_index, col_index]=current_player
        score = game_board_score(current_state, current_player, 2 if current_player == 1 else 1)
        if score==0:
            print("Game Tied")
            break
        elif score==1 or score==2:
            winner="You" if score==1 else "AI"
            print("Winner is {0}".format(winner))
            break
        print(current_state)
        print("------------")
        current_player=1 if current_player == 2 else 2
        pv_player=1 if current_player == 2 else 1
        print("---AI Turn---")
        current_state=get_optimal_move(current_state, pv_player)
        print(current_state)
        print("------------")
        current_player = 1 if current_player == 2 else 2
        score=game_board_score(current_state, current_player, 2 if current_player == 1 else 1)

        if score==0:
            print("Game Tied")
            break
        elif score==1 or score==2:
            winner = "You" if score == 1 else "AI"
            print("Winner is {0}".format(winner))
            break
