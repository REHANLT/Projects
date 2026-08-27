import tkinter as tk
from tkinter import messagebox


class StylishTicTacToe:

    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("420x550")
        self.root.resizable(False, False)

        # Color Palette (Modern Dark Theme)
        self.BG_COLOR = "#1e1e2e"
        self.CARD_COLOR = "#313244"
        self.TEXT_COLOR = "#cdd6f4"
        self.X_COLOR = "#f38ba8"  # Soft Red/Pink
        self.O_COLOR = "#89b4fa"  # Soft Blue
        self.WIN_BG = "#a6e3a1"  # Soft Green
        self.HOVER_COLOR = "#45475a"

        self.root.configure(bg=self.BG_COLOR)

        # Game State Variables
        self.current_player = "X"
        self.board = [""] * 9
        self.scores = {"X": 0, "O": 0}
        self.game_active = True

        # UI Setup
        self._create_header()
        self._create_scoreboard()
        self._create_board()
        self._create_footer()

    def _create_header(self):
        """Header showing game title and status."""
        self.header_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.header_frame.pack(pady=(20, 10))

        self.status_label = tk.Label(
            self.header_frame,
            text="Player X's Turn",
            font=("Helvetica", 16, "bold"),
            bg=self.BG_COLOR,
            fg=self.X_COLOR,
        )
        self.status_label.pack()

    def _create_scoreboard(self):
        """Scoreboard displaying wins for X and O."""
        score_frame = tk.Frame(self.root, bg=self.CARD_COLOR, padx=15, pady=8)
        score_frame.pack(pady=10)

        self.score_x_label = tk.Label(
            score_frame,
            text="Player X: 0",
            font=("Helvetica", 11, "bold"),
            bg=self.CARD_COLOR,
            fg=self.X_COLOR,
        )
        self.score_x_label.grid(row=0, column=0, padx=15)

        divider = tk.Label(
            score_frame,
            text="|",
            font=("Helvetica", 11, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR,
        )
        divider.grid(row=0, column=1)

        self.score_o_label = tk.Label(
            score_frame,
            text="Player O: 0",
            font=("Helvetica", 11, "bold"),
            bg=self.CARD_COLOR,
            fg=self.O_COLOR,
        )
        self.score_o_label.grid(row=0, column=2, padx=15)

    def _create_board(self):
        """Creates the 3x3 interactive button grid."""
        board_container = tk.Frame(
            self.root, bg=self.CARD_COLOR, padx=10, pady=10
        )
        board_container.pack(pady=15)

        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(
                board_container,
                text="",
                font=("Helvetica", 24, "bold"),
                width=4,
                height=2,
                bg=self.BG_COLOR,
                fg=self.TEXT_COLOR,
                activebackground=self.HOVER_COLOR,
                relief="flat",
                bd=0,
                command=lambda index=i: self.make_move(index),
            )
            btn.grid(row=row, column=col, padx=4, pady=4)

            # Hover Effects
            btn.bind(
                "<Enter>", lambda e, b=btn: self._on_hover(b, entering=True)
            )
            btn.bind(
                "<Leave>", lambda e, b=btn: self._on_hover(b, entering=False)
            )

            self.buttons.append(btn)

    def _create_footer(self):
        """Controls section with Reset buttons."""
        footer_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        footer_frame.pack(pady=10)

        reset_btn = tk.Button(
            footer_frame,
            text="Restart Match",
            font=("Helvetica", 10, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR,
            activebackground=self.HOVER_COLOR,
            activeforeground=self.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=6,
            command=self.reset_game,
        )
        reset_btn.pack(side="left", padx=5)

        reset_score_btn = tk.Button(
            footer_frame,
            text="Reset Scores",
            font=("Helvetica", 10, "bold"),
            bg=self.CARD_COLOR,
            fg="#f38ba8",
            activebackground=self.HOVER_COLOR,
            activeforeground="#f38ba8",
            relief="flat",
            padx=15,
            pady=6,
            command=self.reset_scores,
        )
        reset_score_btn.pack(side="right", padx=5)

    def _on_hover(self, btn, entering):
        """Highlights buttons dynamically on cursor hover."""
        if btn["text"] == "" and self.game_active:
            btn.configure(bg=self.HOVER_COLOR if entering else self.BG_COLOR)

    def make_move(self, index):
        """Handles player clicks and updates board state."""
        if self.board[index] != "" or not self.game_active:
            return

        self.board[index] = self.current_player
        color = (
            self.X_COLOR if self.current_player == "X" else self.O_COLOR
        )
        self.buttons[index].configure(
            text=self.current_player, fg=color, bg=self.BG_COLOR
        )

        winning_combo = self._check_win()
        if winning_combo:
            self._handle_win(winning_combo)
        elif "" not in self.board:
            self._handle_tie()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            next_color = (
                self.X_COLOR if self.current_player == "X" else self.O_COLOR
            )
            self.status_label.configure(
                text=f"Player {self.current_player}'s Turn", fg=next_color
            )

    def _check_win(self):
        """Evaluates rows, columns, and diagonals for a win state."""
        winning_combos = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # Rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # Columns
            (0, 4, 8),
            (2, 4, 6),  # Diagonals
        ]
        for combo in winning_combos:
            a, b, c = combo
            if (
                self.board[a]
                == self.board[b]
                == self.board[c]
                == self.current_player
            ):
                return combo
        return None

    def _handle_win(self, combo):
        """Updates UI state upon victory."""
        self.game_active = False
        self.scores[self.current_player] += 1

        for idx in combo:
            self.buttons[idx].configure(bg=self.WIN_BG, fg="#11111b")

        self.status_label.configure(
            text=f"🎉 Player {self.current_player} Wins!", fg=self.WIN_BG
        )
        self._update_score_display()

    def _handle_tie(self):
        """Updates UI state upon a tie game."""
        self.game_active = False
        self.status_label.configure(text="🤝 It's a Tie!", fg=self.TEXT_COLOR)

    def _update_score_display(self):
        self.score_x_label.configure(text=f"Player X: {self.scores['X']}")
        self.score_o_label.configure(text=f"Player O: {self.scores['O']}")

    def reset_game(self):
        """Clears board state for a new match."""
        self.board = [""] * 9
        self.current_player = "X"
        self.game_active = True
        self.status_label.configure(
            text="Player X's Turn", fg=self.X_COLOR
        )

        for btn in self.buttons:
            btn.configure(text="", bg=self.BG_COLOR)

    def reset_scores(self):
        """Resets overall score tracking."""
        self.scores = {"X": 0, "O": 0}
        self._update_score_display()
        self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    app = StylishTicTacToe(root)
    root.mainloop()
