import tkinter as tk
import customtkinter as ctk


class Game(ctk.CTk):

    width = 500
    height = 380

    def __init__(self):
        super().__init__()

        """Interface"""

        self.resizable(False, False)
        self.title('Tic-Tac-Toe')
        self.geometry(f"{self.width}x{self.height}")

        self.label_human = ctk.CTkLabel(self, text='Human: 0')
        self.label_human.grid(row=0, column=0, padx=[30, 0], pady=[20, 20])
        self.label_computer = ctk.CTkLabel(self, text='Computer: 0')
        self.label_computer.grid(row=0, column=4)
        self.label_info = ctk.CTkLabel(self, text='')
        self.label_info.grid(row=0, column=8)

        self.gameboard = Board(self)
        self.gameboard.grid(row=1, column=0, rowspan=10, columnspan=8, padx=[40, 30], pady=[10, 0])

        button_new = ctk.CTkButton(self, text='New Game', command=self.gameboard.restart)
        button_new.grid(row=1, column=8)
        button_switch = ctk.CTkButton(self, text='Switch', command=self.switcher)
        button_switch.grid(row=2, column=8)
        button_reset = ctk.CTkButton(self, text='Reset', command=self.reset_score_value)
        button_reset.grid(row=3, column=8)

    def reset_score_value(self):
        self.gameboard.team_blue['score'] = 0
        self.gameboard.team_green['score'] = 0
        self.label_human.configure(text='Human: ' + str(self.gameboard.team_blue['score']))
        self.label_computer.configure(text='Computer: ' + str(self.gameboard.team_green['score']))
        self.label_info.configure(text='')
        self.gameboard.restart()

    def switcher(self):
        players = [self.gameboard.team_blue, self.gameboard.team_green]
        current_player_index = players.index(self.gameboard.who_starts)
        switch_player_index = (current_player_index + 1) % len(players)
        self.gameboard.who_starts = players[switch_player_index]

        temp_value = players[0]['sym']
        players[0]['sym'] = players[1]['sym']
        players[1]['sym'] = temp_value

        self.gameboard.restart()

    def run(self):
        self.mainloop()

    def close_window(self):
        self.destroy()


class Board(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """Board and logic"""

        self.game_run = True
        self.cells = []

        # Settings for Player and Computer
        self.team_blue = {
            'player': 'Human',
            'label': self.master.label_human,
            'color': 'SkyBlue1',
            'sym': 'X',
            'score': 0
        }
        self.team_green = {
            'player': 'Computer',
            'label': self.master.label_computer,
            'color': 'green',
            'sym': 'O',
            'score': 0
        }

        self.who_starts = self.team_blue
        self.create_board()
        self.check_who_starts()

    def create_board(self):
        for row in range(3):
            line = []
            for col in range(3):
                button = tk.Button(self, text=' ', width=4, height=2,
                                   font=('Verdana', 20, 'bold'),
                                   background='grey',
                                   command=lambda row=row, col=col: self.insert_sym(row, col, self.team_blue)
                                   )
                button.grid(row=row, column=col)
                line.append(button)
            self.cells.append(line)

    def check_who_starts(self):
        if self.who_starts == self.team_green:
            self.computer_move()

    def restart(self):
        for row in range(3):
            for col in range(3):
                self.cells[row][col]['text'] = ' '
        self.game_run = True
        self.master.label_info.configure(text='')
        self.check_who_starts()

    def insert_sym(self, row, col, player):
        if self.game_run and self.cells[row][col]['text'] == ' ':
            self.cells[row][col]['text'] = player['sym']
            if self.check_win(player['sym']):
                self.write_score(player)
            elif len(self.check_empty_cells()) == 0:
                self.master.label_info.configure(text=f"Draw!")
            elif player['player'] != 'Computer' and len(self.check_empty_cells()) > 0:
                self.computer_move()

    def write_score(self, player):
        player['score'] += 1
        self.game_run = False
        new_score = player['label'].cget('text').split(':')[0] + f": {str(player['score'])}"
        player['label'].configure(text=new_score)
        self.master.label_info.configure(text=f"{player['player']} Win!", text_color=player['color'])

    def check_win(self, sym):
        for n in range(3):
            if self.cells[n][0]['text'] == self.cells[n][1]['text'] == self.cells[n][2]['text'] == sym:
                return True
            elif self.cells[0][n]['text'] == self.cells[1][n]['text'] == self.cells[2][n]['text'] == sym:
                return True
        if self.cells[0][0]['text'] == self.cells[1][1]['text'] == self.cells[2][2]['text'] == sym:
            return True
        elif self.cells[2][0]['text'] == self.cells[1][1]['text'] == self.cells[0][2]['text'] == sym:
            return True
        else:
            return False

    def check_empty_cells(self):
        cells_empty = []
        for row in range(3):
            for col in range(3):
                if self.cells[row][col]['text'] == ' ':
                    cells_empty.append((row, col))
        return cells_empty

    def computer_move(self):
        best_score = -10000
        worst_score = 10000

        for row, col in self.check_empty_cells():
            self.cells[row][col]['text'] = self.team_green['sym']
            score = self.minimax_alg(0, False, best_score, worst_score)
            self.cells[row][col]['text'] = ' '
            if score > best_score:
                best_score = score
                best_move = (row, col)

        self.insert_sym(best_move[0], best_move[1], self.team_green)

    def minimax_alg(self, depth, is_maximizing, alpha, beta):
        if self.check_win(self.team_green['sym']):
            return 1
        elif self.check_win(self.team_blue['sym']):
            return -1
        elif len(self.check_empty_cells()) == 0:
            return 0
        if is_maximizing:
            best_score = -10000
            for row, col in self.check_empty_cells():
                self.cells[row][col]['text'] = self.team_green['sym']
                score = self.minimax_alg(depth + 1, False, alpha, beta)
                self.cells[row][col]['text'] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = 10000
            for row, col in self.check_empty_cells():
                self.cells[row][col]['text'] = self.team_blue['sym']
                score = self.minimax_alg(depth + 1, True, alpha, beta)
                self.cells[row][col]['text'] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Game()
    app.protocol('WM_DELETE_WINDOW', app.close_window)
    app.run()
