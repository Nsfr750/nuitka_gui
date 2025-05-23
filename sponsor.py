"""
Sponsor Dialog Module

This module provides the Sponsor dialog for the Nuitka GUI Compiler.
Displays options for users to support the project via various platforms.
"""

import tkinter as tk
import webbrowser
from typing import List, Tuple

class Sponsor:
    """
    A class to display the Sponsor sponsor_win for the Nuitka GUI Compiler.
    """
    @staticmethod
    def show_sponsor(root):
        import tkinter as tk
        import webbrowser
        # Simple sponsor sponsor_win example
        sponsor_win = tk.Toplevel(root)
        sponsor_win.title("Sponsor")
        sponsor_win.geometry("500x200")
        sponsor_win.transient(root)
        sponsor_win.grab_set()
        tk.Label(sponsor_win, text="Support development!", font=("Arial", 14, "bold")).pack(pady=8)
        tk.Label(sponsor_win, text="You can sponsor this project on:").pack(pady=2)
        def open_url(url):
            try:
                webbrowser.open(url)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open URL: {e}")
        btn_frame = tk.Frame(sponsor_win)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="GitHub Sponsors", command=lambda: open_url("https://github.com/sponsors/"), width=16).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Patreon", command=lambda: open_url("https://patreon.com/"), width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Buy Me a Coffee", command=lambda: open_url("https://paypal.me/3dmega"), width=16).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="Discord", command=lambda: open_url("https://discord.gg/"), width=16).pack(side=tk.LEFT, padx=4)
        tk.Button(sponsor_win, text="Close", command=sponsor_win.destroy).pack(pady=10)
            
        # Add a thank you message
        thank_you = tk.Label(
            sponsor_win,
            text="Thank you for considering to support the project!",
            font=('Helvetica', 12, 'bold'),
            pady=10
        )
        thank_you.pack()
        
        # Frame to hold the sponsor buttons
        btn_frame = tk.Frame(sponsor_win, pady=20)
        btn_frame.pack(expand=True)
        
        # Define sponsorship options with their display text and URLs
        buttons: List[Tuple[str, str]] = [
            ("⭐ Sponsor on GitHub", "https://github.com/sponsors/Nsfr750"),
            ("💬 Join Discord", "https://discord.gg/BvvkUEP9"),
            ("☕ Buy Me a Coffee", "https://paypal.me/3dmega"),
            ("❤️ Join Patreon", "https://www.patreon.com/Nsfr750")
        ]
        
        # Create and pack each sponsor button
        for text, url in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                pady=8,
                padx=15,
                relief=tk.RAISED,
                bd=2,
                command=lambda u=url: Sponsor._open_url(u)
            )
            btn.pack(side=tk.LEFT, padx=10, ipadx=5, ipady=3)
        
        # Close button at the bottom
        close_btn = tk.Button(
            sponsor_win,
            text="Close",
            command=sponsor_win.destroy,
            width=15,
            pady=5
        )
        close_btn.pack(pady=(0, 10))
        
        # Make the sponsor_win modal
        sponsor_win.transient(root)
        sponsor_win.grab_set()
        root.wait_window(sponsor_win)

