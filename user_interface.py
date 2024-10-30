
import customtkinter as ctk
from CTkTable import *
from bow_main import BOW
import pandas as pd 

class UserInterface(ctk.CTk):
    
    bow_client = None
    grid_textbox = None
    
    def __init__(self):
        super().__init__()
        self.title("Baby Pink App")
        self.geometry("600x450")  # Set the size of the window

        # Set the background color of the entire app
        self.configure(fg_color="#FFB6C1")  # Using fg_color for the main window

        # Create a label with a message, making it larger and bold
        self.label = ctk.CTkLabel(
            self,
            text="Hello. Describe a movie and\nI'll give you a match!",  # Broken quote
            fg_color="#FFB6C1",
            font=("Helvetica", 20, "bold"),  # Font size 20 and bold for better visibility
            text_color="white"  # Strong white text color
        )
        self.label.pack(pady=(30, 10), padx=20, fill='x')  # Increased top padding

        # Entry for user input with white background
        self.user_input = ctk.CTkEntry(self, text_color="black", width=300, fg_color="white", border_width=2)
        self.user_input.pack(pady=20)

        self.root = ctk.CTk()


        # Button to submit the input, setting its color to black with bold text
        self.submit_button = ctk.CTkButton(
            self,
            text="Submit",
            command=self.submit_input,
            fg_color="black",  # Set button color to black
            text_color="white",  # Text color for contrast
            font=("Helvetica", 14, "bold")  # Button text size and bold
        )
        self.submit_button.pack(pady=10)

        # Label for results
        self.results_label = ctk.CTkLabel(
            self,
            text="Your Movie Suggestions :D",  # Changed label text
            fg_color="#FFB6C1",
            font=("Helvetica", 16, "bold"),  # Font size for results label
            text_color="white"  # Strong white text color
        )
        self.results_label.pack(pady=(10, 0), padx=20, fill='x')  # Reduced space between label and box

        # Box to contain results of the search with black border
        #self.results_box = ctk.CTkTextbox(self, width=600, height=200, fg_color="white", border_width=2, corner_radius=5)
        #self.results_box.pack(pady=20)  # Reduced space above the results box
        
        self.grid_textbox = ctk.CTkTextbox(self, width=600, fg_color="White", text_color="black", height=300)
        self.grid_textbox.pack(padx=20, pady=20)
        
        self.bow_client = BOW()

    def submit_input(self):
        # This is where you handle the input
        user_description = self.user_input.get()
        print(user_description)
        # Check if user input is received
        if user_description:
            result = self.bow_client.search_movies(user_description)
            if not result.empty:
                
                self.grid_textbox.delete("0.1", ctk.END)
                
                df_ = pd.DataFrame(result, columns=['Title', 'Director', 'Overview', 'Score'])
                formatted_text = ""
                for index, row in df_.iterrows():
                    formatted_text += f"Title: {row['Title']}\n"
                    formatted_text += f"Director: {row['Director']}\n"
                    formatted_text += f"Overview: {row['Overview']}\n"
                    formatted_text += f"Score: {row['Score']:.1f}\n"
                    formatted_text += "-" * 40 + "\n"
                
                self.grid_textbox.insert("0.0", formatted_text)
                
                #self.results_box.delete('1.0', ctk.END)  # Clear previous results
                #self.results_box.insert(ctk.END, f"{result.values.tolist()}") # result.to_string(index=False)}
        else:
            pass
            # Display a message if no input is provided
            #self.results_box.delete('1.0', ctk.END)  # Clear previous results
            #self.results_box.insert(ctk.END, "Please enter a description.")
