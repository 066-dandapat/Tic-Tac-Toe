import tkinter as tk
from tkinter import messagebox
import math, time

# --- Initialize window ---
window = tk.Tk()
window.title(" Tic Tac Toe With AI ")
window.geometry("600x700")
window.resizable(True, True)

# --- Game State ---
board = [" "] * 9
buttons = []
player = "X"
ai = "O"
is_dark = True
is_fullscreen = False

# --- Colors ---
DARK_THEME = {
    "bg": "#101010",
    "btn_bg": "#202020",
    "fg": "white",
    "active_bg": "#303030",
    "text_player": "#00ffff",
    "text_ai": "#ff007f"
}

LIGHT_THEME = {
    "bg": "#f2f2f2",
    "btn_bg": "#e0e0e0",
    "fg": "black",
    "active_bg": "#d0d0d0",
    "text_player": "#0066ff",
    "text_ai": "#ff3366"
}

theme = DARK_THEME.copy()

# --- Game Logic ---
def check_winner(b, p):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in win_conditions:
        if all(b[i]==p for i in combo):
            return combo
    return None

def is_full(b):
    return all(cell!=" " for cell in b)

def minimax(b, depth, is_maximizing):
    if check_winner(b, ai): return 1
    if check_winner(b, player): return -1
    if is_full(b): return 0

    if is_maximizing:
        best=-math.inf
        for i in range(9):
            if b[i]==" ":
                b[i]=ai
                val=minimax(b, depth+1, False)
                b[i]=" "
                best=max(best,val)
        return best
    else:
        best=math.inf
        for i in range(9):
            if b[i]==" ":
                b[i]=player
                val=minimax(b, depth+1, True)
                b[i]=" "
                best=min(best,val)
        return best

def best_move():
    best_score=-math.inf; move=None
    for i in range(9):
        if board[i]==" ":
            board[i]=ai
            score=minimax(board,0,False)
            board[i]=" "
            if score>best_score:
                best_score=score
                move=i
    return move

# --- Animation ---
def rgb_highlight_line(indices, duration=1.5, steps=30):
    """Highlight only the winning line with RGB lighting."""
    for i in range(steps):
        r=int(127+128*math.sin(i/6))
        g=int(127+128*math.sin(i/6+2))
        b=int(127+128*math.sin(i/6+4))
        color=f"#{r:02x}{g:02x}{b:02x}"
        for idx in indices:
            buttons[idx].config(bg=color)
        window.update()
        time.sleep(duration/steps)
    time.sleep(0.3)

def fade_in(btn, text, color, steps=8, delay=0.04):
    btn.config(text=text, disabledforeground=color)
    for i in range(steps):
        gray=f"#{int(255*(i+1)/steps):02x}{int(255*(i+1)/steps):02x}{int(255*(i+1)/steps):02x}"
        btn.config(disabledforeground=gray)
        window.update()
        time.sleep(delay)
    btn.config(disabledforeground=color)

# --- Theme ---
def apply_theme():
    window.config(bg=theme["bg"])
    frame.config(bg=theme["bg"])
    top_bar.config(bg=theme["bg"])
    toggle_btn.config(bg=theme["btn_bg"], fg=theme["fg"], activebackground=theme["active_bg"])
    for btn in buttons:
        btn.config(bg=theme["btn_bg"], fg=theme["fg"], activebackground=theme["active_bg"])

def toggle_theme():
    global theme, is_dark
    is_dark = not is_dark
    theme = DARK_THEME.copy() if is_dark else LIGHT_THEME.copy()
    toggle_btn.config(text="🌙 Dark" if not is_dark else "🌞 Light")
    apply_theme()

# --- Fullscreen ---
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    window.attributes("-fullscreen", is_fullscreen)

# --- Popup Reset ---
def show_reset_popup(message):
    """Ask player to play again or exit."""
    choice = messagebox.askyesno("Game Over", f"{message}\n\nDo you want to play again?")
    if choice:
        reset_game()
    else:
        window.destroy()

# --- Gameplay ---
def on_click(i):
    if board[i]==" ":
        board[i]=player
        buttons[i].config(state="disabled")
        fade_in(buttons[i],player,theme["text_player"])
        win_combo=check_winner(board,player)
        if win_combo:
            rgb_highlight_line(win_combo)
            show_reset_popup("🎉 You win!")
            return
        if is_full(board):
            show_reset_popup("🤝 It's a draw!")
            return
        window.after(500, ai_turn)

def ai_turn():
    move=best_move()
    if move is not None:
        board[move]=ai
        buttons[move].config(state="disabled")
        fade_in(buttons[move],ai,theme["text_ai"])
        win_combo=check_winner(board,ai)
        if win_combo:
            rgb_highlight_line(win_combo)
            show_reset_popup("💻 AI wins!")
            return
        if is_full(board):
            show_reset_popup("🤝 It's a draw!")
            return

def reset_game():
    global board
    board=[" "]*9
    for btn in buttons:
        btn.config(text=" ", state="normal", bg=theme["btn_bg"])

# --- UI Layout ---
top_bar=tk.Frame(window,bg=theme["bg"])
top_bar.pack(fill="x",pady=10)

toggle_btn=tk.Button(top_bar,text="🌞 Light",font=("Arial",13,"bold"),
                     command=toggle_theme,width=10)
toggle_btn.pack(side="left",padx=10)

# Fullscreen button hidden

frame=tk.Frame(window,bg=theme["bg"])
frame.pack(expand=True,pady=40)

for i in range(9):
    btn=tk.Button(frame,text=" ",font=("Arial",48,"bold"),width=3,height=1,
                  bg=theme["btn_bg"],fg=theme["fg"],relief="ridge",
                  command=lambda i=i:on_click(i))
    btn.grid(row=i//3,column=i%3,padx=15,pady=15)
    buttons.append(btn)

apply_theme()

messagebox.showinfo("Tic Tac Toe",
    "You are X \n   AI is O   ")

window.mainloop()
