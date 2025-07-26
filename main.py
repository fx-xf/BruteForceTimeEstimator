#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pyfiglet import Figlet  # For ASCII art banner
from rich.console import Console  # For rich text formatting
from rich.panel import Panel  # For displaying panels
from rich.text import Text  # For styled text
from rich import print as rprint  # For rich printing
import colorama  # For colored terminal output

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)

# Console instance for rich text output
console = Console()

class Config:
    # Model filename constant
    MODEL_FILENAME = "password_time_model.pkl"

class UI:
    """Handles user interface operations like displaying menus and messages."""

    def __init__(self):
        self.console = Console()

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        """Displays the application banner with ASCII art and info."""
        self.clear_screen()
        banner_text = Text("""
   ███████████     ███████████    ███████████    ██████████
   ░░███░░░░░███   ░░███░░░░░░█   ░█░░░███░░░█   ░░███░░░░░█
    ░███    ░███    ░███   █ ░    ░   ░███  ░     ░███  █ ░ 
    ░██████████     ░███████          ░███        ░██████   
    ░███░░░░░███    ░███░░░█          ░███        ░███░░█   
    ░███    ░███    ░███  ░           ░███        ░███ ░   █
    ███████████     █████             █████       ██████████
   ░░░░░░░░░░░     ░░░░░             ░░░░░       ░░░░░░░░░░ 
        """, style="bold cyan")
        
        info_text = Text("Brute Force Time Estimator - Developed by fx-xf", style="green")
        
        self.console.print(banner_text, justify="center")
        self.console.rule("[bold green]◈[/bold green]" * 3, style="green")
        self.console.print(info_text, justify="center")
        self.console.print()

    def display_menu(self):
        """Displays the main menu with options."""
        menu_text = Text.from_markup(
            """
[bold yellow][0][/bold yellow] Check Password Strength
[bold yellow][1][/bold yellow] Generate Secure Password
[bold yellow][2][/bold yellow] About Developer
[bold yellow][3][/bold yellow] Exit
"""
        )
        self.console.print(
            Panel(menu_text, title="[bold cyan]Main Menu[/bold cyan]", border_style="cyan", expand=True)
        )

    def get_input(self, prompt: str) -> str:
        """Prompts user for input with styled formatting."""
        return self.console.input(f"[bold yellow]╚═>[/bold yellow] [bold white]{prompt}:[/bold white] ")

    def display_info_panel(self, title: str, content: str, border_style: str = "cyan"):
        """Displays information in a styled panel."""
        self.console.print(
            Panel(content, title=f"[bold {border_style}]{title}[/]", border_style=border_style)
        )

    def display_error(self, message: str):
        """Displays an error message in a red panel."""
        self.console.print(
            Panel(message, title="[bold red]Error[/]", border_style="red")
        )

    def display_success(self, message: str):
        """Displays a success message in a green panel."""
        self.console.print(
            Panel(message, title="[bold green]Success[/]", border_style="green")
        )

    def wait_for_enter(self, message: str = "Press Enter to continue"):
        """Waits for user to press Enter to continue."""
        self.console.input(f"[bold yellow]╚═>[/bold yellow] [bold white]{message}[/bold white]")

class PasswordAnalyzerApp:
    """Main application class for the Password Strength Analyzer."""

    def __init__(self):
        self.ui = UI()
        self.model_path = os.path.join(os.path.dirname(__file__), Config.MODEL_FILENAME)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def _get_script_path(self, script_name):
        """Returns the absolute path to a script in the project directory."""
        return os.path.join(self.script_dir, script_name)
        
    def _check_model_exists(self):
        """Checks if the model file exists."""
        if not os.path.exists(self.model_path):
            self.ui.display_error(f"Model file '{Config.MODEL_FILENAME}' not found. Please ensure the model is trained and saved.")
            return False
        return True

    def run_inference(self):
        """Runs the password strength inference script."""
        if not self._check_model_exists():
            return
            
        try:
            script_path = self._get_script_path('infer.py')
            
            if not os.path.exists(script_path):
                self.ui.display_error("infer.py script not found.")
                return
                
            self.ui.console.print("[yellow]Starting password strength check...[/yellow]")
            
            process = subprocess.Popen(
                [sys.executable, script_path, self.model_path], 
                stdin=sys.stdin, 
                stdout=sys.stdout, 
                stderr=sys.stderr
            )
            process.wait()
            
            if process.returncode != 0:
                self.ui.display_error("An error occurred during password analysis.")
                
        except Exception as e:
            self.ui.display_error(f"Unexpected error: {e}")

    def run_generator(self):
        """Runs the password generation script."""
        try:
            script_path = self._get_script_path('generate_password.py')
            
            if not os.path.exists(script_path):
                self.ui.display_error("generate_password.py script not found.")
                return
                
            self.ui.console.print("[yellow]Starting password generator...[/yellow]")
            
            process = subprocess.Popen(
                [sys.executable, script_path], 
                stdin=sys.stdin, 
                stdout=sys.stdout, 
                stderr=sys.stderr
            )
            process.wait()
            
            if process.returncode != 0:
                self.ui.display_error("An error occurred during password generation.")
                
        except Exception as e:
            self.ui.display_error(f"Unexpected error: {e}")

    def show_about(self):
        """Displays information about the developer."""
        about_content = Text.from_markup("""
[bold cyan]Developer Information:[/bold cyan]

[yellow]GitHub:[/yellow] [link=https://github.com/fx-xf]https://github.com/fx-xf[/link]

This Password Strength Analyzer helps you evaluate password complexity 
and generate secure passwords using machine learning techniques.
""")
        self.ui.display_info_panel("About Developer", about_content, "purple")

    def run(self):
        """Main application loop."""
        try:
            while True:
                self.ui.display_banner()
                self.ui.display_menu()
                
                choice = self.ui.get_input("Select an option")
                
                if choice == "0":
                    self.run_inference()
                elif choice == "1":
                    self.run_generator()
                elif choice == "2":
                    self.show_about()
                elif choice == "3":
                    self.ui.console.print("[bold red]Goodbye![/bold red]")
                    break
                else:
                    self.ui.display_error("Invalid option, please try again.")
                
                if choice in ["0", "1", "2"]:
                    self.ui.wait_for_enter()
                    
        except KeyboardInterrupt:
            self.ui.console.print("\n[bold red]Exiting...[/bold red]")
        except Exception as e:
            self.ui.display_error(f"Application error: {e}")

if __name__ == "__main__":
    app = PasswordAnalyzerApp()
    app.run()