import tkinter as tk
from engine import EngineInterface
from engine import GameState


class MainWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(False, False)     
        self.board = Board(self)
        self.board.pack()
        self.player_color = "yellow"
        self.engine_color = "red"
        self.new_game_flag = False
        self.difficulty_level = tk.StringVar()        
        self.difficulty_level.set("Medium")    
        self.player_make_first_move = True
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.score = [0, 0]
        self.title("Four in a row: 0 - 0")
        self.animations = True
        
    def new_game_dialog_box(self):    
        self.protocol("WM_DELETE_WINDOW", self.dont_close_window) # Disable close window    
        dialog_box = DialogBox(main_window, "New game")
        if self.new_game_flag:
            self.new_game_flag = False
            self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window     
        else:
            self.destroy()
               
    def update_difficulty_level(self, *args):
        """Update the difficulty level in the engine and reset score if
        the level is changed."""
        current_level = engine_interface.difficulty_level
        if self.difficulty_level.get() == "Easy":
            engine_interface.difficulty_level = 1
        elif self.difficulty_level.get() == "Medium":
            engine_interface.difficulty_level = 2
        elif self.difficulty_level.get() == "Hard":
            engine_interface.difficulty_level = 3
        if engine_interface.difficulty_level != current_level:
            self.score = [0, 0]
            self.title_update()
        
    def title_update(self):
        self.title("Four in a row: " + str(self.score[0]) + " - " + str(self.score[1]))
        
    def update_and_pause(self, time_in_ms):
        self.board.unbind_mouse()
        self.update_idletasks()                    
        self.after(time_in_ms)
        self.update() # Handle possible events.
        self.board.rebind_mouse()

    def mouse_click(self, column_number):
        """This function is called if the column with column_number have been
        clicked on.
        """
        self.protocol("WM_DELETE_WINDOW", self.dont_close_window) # Disable close window
        
        # Player make a move, if there is empty places left in the column.
        column_height = game_state.column_height[column_number]
        if column_height < 6:
            game_state.make_move(column_number)
            self.board.add_disk_to_top_of_column(column_number, self.player_color, self.animations)
        else:
            self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window
            return
        
        # If player win.
        if engine_interface.four_in_a_row(game_state):
            self.score[0] += 1
            self.title_update()
            self.highlight_four_in_a_row(self.player_color)
            self.update_and_pause(1000)
            dialog_box = DialogBox(main_window, "You win! Congratulations!")            
            if self.new_game_flag:
                self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window
                self.new_game()
            else:
                self.destroy()
            return
                
        # If draw.
        if game_state.number_of_moves == 42:
            self.update_and_pause(600)
            dialog_box = DialogBox(main_window, "Draw")
            if self.new_game_flag:
                self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window
                self.new_game()
            else:
                self.destroy()
            return

        # Engine makes a move
        column_number = engine_interface.engine_move(game_state)
        game_state.make_move(column_number)
        if self.animations:
            self.update_and_pause(50)
        else:
            self.update_and_pause(300)                       
        self.board.add_disk_to_top_of_column(column_number, self.engine_color, self.animations)

        # If engine win.
        if engine_interface.four_in_a_row(game_state):
            self.score[1] += 1
            self.title_update()
            self.highlight_four_in_a_row(self.engine_color)
            self.update_and_pause(1000)
            dialog_box = DialogBox(main_window, "Computer win!")
            if self.new_game_flag:
                self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window            
                self.new_game()
            else:
                self.destroy()            
            return

        # If draw.
        if game_state.number_of_moves == 42:   
            self.update_and_pause(600)
            dialog_box = DialogBox(main_window, "Draw")          
            if self.new_game_flag:
                self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window
                self.new_game()
            else:
                self.destroy()
            return

        self.protocol("WM_DELETE_WINDOW", self.close_window) # Enable close window
    
    def highlight_four_in_a_row(self, color):     
        positions = engine_interface.four_in_a_row_positions(game_state)        
        self.update_and_pause(500)
        for (column, row) in positions:
            self.board.remove_disk(column, row)
        self.update_and_pause(500)
        for (column, row) in positions:
            self.board.add_disk(column, row, color)
        
    def new_game(self):
        self.new_game_flag = False
        self.player_make_first_move = not self.player_make_first_move
        game_state.__init__()
        self.board.remove_all_disks()

        if not self.player_make_first_move:
            column_number = engine_interface.engine_move(game_state)
            game_state.make_move(column_number)
            self.update_and_pause(300)                     
            self.board.add_disk_to_top_of_column(column_number, self.engine_color, self.animations)

    def dont_close_window(self):
        pass

    def close_window(self):
        self.destroy()
        
    
class Board(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.column_list = []
        for column_number in range(7):
            column = Column(self, column_number)
            column.pack(side=tk.LEFT)
            self.column_list.append(column)

    def mouse_click(self, column_number):
        self.parent.mouse_click(column_number)      

    def add_disk_to_top_of_column(self, column_number, color, animations):
        """column_number is 0,1 to 6. animations is True or False."""
        self.column_list[column_number].add_disk_to_top_of_column(color, animations)

    def add_disk(self, column, row, color):
        self.column_list[column].add_disk(row, color)

    def remove_disk(self, column, row):
        self.column_list[column].remove_disk(row)

    def remove_all_disks(self):
        for column in self.column_list:
            column.remove_all_disks()

    def unbind_mouse(self):
        for column in self.column_list:
            column.unbind_mouse()
        
    def rebind_mouse(self):
       for column in self.column_list:
            column.rebind_mouse()

class Column(tk.Frame):
    def __init__(self, parent, column_number):
        """column_number is 0,1 to 6 and is used as an identifier."""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.column_number = column_number
        self.disks_in_column = 0
        self.column = []
        for cell in range(6):
            new_cell = Cell(self, 90)
            new_cell.pack(side=tk.BOTTOM)
            self.column.append(new_cell)

    def mouse_click(self, event):
        self.parent.mouse_click(self.column_number)

    def add_disk_to_top_of_column(self, color, animations):
        """animations is True or False."""
        if animations:            
            time_in_each_row = [0.41421356237309515, 0.31783724519578205, 0.2679491924311228,
                                0.2360679774997898, 0.21342176528338808]
            total_time = 0
            min_time = 250                          
            self.add_disk(5, color)
            self.update_idletasks()
            row = 4
            while row >= self.disks_in_column:
                pause_time = round(165*time_in_each_row[row])
                self.after(pause_time)
                total_time += pause_time
                self.remove_disk(row + 1)
                self.add_disk(row, color)
                self.update_idletasks()            
                row -=1
            if total_time < min_time:
                self.after(min_time - total_time)  
        else:
            self.add_disk(self.disks_in_column, color)
        self.disks_in_column += 1

    def add_disk(self, row, color):
        self.column[row].add_disk(color)

    def remove_disk(self, row):
        self.column[row].remove_disk()

    def remove_all_disks(self):
        self.disks_in_column = 0   
        for cell in self.column:
            cell.remove_disk()

    def unbind_mouse(self):
        for cell in self.column:
            cell.unbind_mouse()

    def rebind_mouse(self):
        for cell in self.column:
            cell.rebind_mouse()
                
class Cell(tk.Canvas):

    def __init__(self, parent, side_length):
        """A cell is the a square-shaped piece of the board consisting of
        one empty space where a disk can be placed.
        """
        self.parent = parent
        self.background_color = "#1439f9"
        tk.Canvas.__init__(self, parent, width=side_length, height=side_length,
                           bg=self.background_color, highlightthickness=0)                         
        # An odd diameter can give a better looking circle.
        radius = (9 * side_length) // 20
        d = (side_length - (2 * radius + 1)) // 2
        self.disk = self.create_oval(d, d, d + 2 * radius + 1, d + 2 * radius + 1,
                                     width=2, outline="#0000AA")                                                                              
        self.bind("<Button-1>", parent.mouse_click)
    
    def add_disk(self, color):
        self.itemconfig(self.disk, fill=color)

    def remove_disk(self):   
        self.itemconfig(self.disk, fill=self.background_color)
        
    def unbind_mouse(self):
        self.unbind("<Button-1>")
        
    def rebind_mouse(self):
        self.bind("<Button-1>", self.parent.mouse_click)
        
        
class DialogBox(tk.Toplevel):

    def __init__(self, parent, text):
        """Return 'play' or 'quit'."""
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.transient(parent)
        self.wait_visibility() # Window needs to be visible for the grab.
        self.grab_set() # Routes all events for this application to this widget.
        self.focus_set()
        self.title("Four in a row")
        box_width = 300
        box_height = 120

        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        if box_width >= parent_width:
            x_offset = parent.winfo_rootx()
        else:
            x_offset = parent.winfo_rootx() + (parent_width - box_width) // 2
        
        y_offset = parent.winfo_rooty() + (parent_height - box_height - 40) // 2
        if y_offset < parent.winfo_rooty():
            y_offset = parent.winfo_rooty()
        
        self.geometry("%dx%d+%d+%d" % (box_width, box_height, x_offset, y_offset))
    
        text = tk.Label(self, text=text, font=("", 11, "bold"), borderwidth=10)
        text.pack()

        radio_button_frame = tk.Frame(master=self)
        tk.Radiobutton(radio_button_frame, text="Easy", font=("", 10),
                       variable=parent.difficulty_level, value="Easy").pack(side=tk.LEFT)
        tk.Radiobutton(radio_button_frame, text="Medium", font=("", 10),
                       variable=parent.difficulty_level, value="Medium").pack(side=tk.LEFT)
        tk.Radiobutton(radio_button_frame, text="Hard", font=("", 10),
                       variable=parent.difficulty_level, value="Hard").pack()
        radio_button_frame.pack()

        button_frame = tk.Frame(master=self, pady=10)
        button_frame.pack()
        tk.Button(button_frame, text="Play", font=("", 10), width=8,
                  command=self.play).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Quit", font=("", 10), width=8,
                  command=self.quit).pack()
        self.bind("<Return>", self.play)
        self.bind("<Escape>", self.quit)
        parent.wait_window(window=self)
           
    def play(self, event=None):
        self.parent.new_game_flag = True
        self.parent.update_difficulty_level()
        self.destroy()
            
    def quit(self, event=None):
        self.destroy()
                      
game_state = GameState()
engine_interface = EngineInterface(2)                    
main_window = MainWindow()
main_window.update()
main_window.new_game_dialog_box()
main_window.mainloop()
