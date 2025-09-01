import requests
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Currency Converter")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # API configuration
        self.api_key = "YOUR_API_KEY"  # Get free API key from exchangerate-api.com
        self.base_url = "https://v6.exchangerate-api.com/v6/"
        
        # Currency data
        self.currencies = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "BRL": "Brazilian Real",
            "MXN": "Mexican Peso",
            "SGD": "Singapore Dollar",
            "HKD": "Hong Kong Dollar",
            "NZD": "New Zealand Dollar",
            "SEK": "Swedish Krona",
            "KRW": "South Korean Won",
            "RUB": "Russian Ruble",
            "ZAR": "South African Rand",
            "TRY": "Turkish Lira",
            "PLN": "Polish Złoty"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Live Currency Converter",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=10)
        
        # Amount input
        amount_frame = tk.Frame(main_frame, bg='#f0f0f0')
        amount_frame.pack(fill='x', pady=10)
        
        tk.Label(
            amount_frame,
            text="Amount:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.amount_entry = tk.Entry(
            amount_frame,
            font=("Arial", 12),
            width=15
        )
        self.amount_entry.pack(side='left', padx=10)
        self.amount_entry.insert(0, "1")
        
        # Currency selection frame
        currency_frame = tk.Frame(main_frame, bg='#f0f0f0')
        currency_frame.pack(fill='x', pady=20)
        
        # From currency
        from_frame = tk.Frame(currency_frame, bg='#f0f0f0')
        from_frame.pack(fill='x', pady=5)
        
        tk.Label(
            from_frame,
            text="From:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.from_currency = ttk.Combobox(
            from_frame,
            values=list(self.currencies.keys()),
            font=("Arial", 12),
            width=15,
            state="readonly"
        )
        self.from_currency.pack(side='left', padx=10)
        self.from_currency.set("USD")
        
        # To currency
        to_frame = tk.Frame(currency_frame, bg='#f0f0f0')
        to_frame.pack(fill='x', pady=5)
        
        tk.Label(
            to_frame,
            text="To:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.to_currency = ttk.Combobox(
            to_frame,
            values=list(self.currencies.keys()),
            font=("Arial", 12),
            width=15,
            state="readonly"
        )
        self.to_currency.pack(side='left', padx=10)
        self.to_currency.set("EUR")
        
        # Convert button
        self.convert_btn = tk.Button(
            main_frame,
            text="Convert",
            command=self.convert_currency,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=20,
            pady=10
        )
        self.convert_btn.pack(pady=20)
        
        # Result frame
        result_frame = tk.Frame(main_frame, bg='#f0f0f0')
        result_frame.pack(fill='x', pady=10)
        
        self.result_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',
            fg='#2196F3'
        )
        self.result_label.pack()
        
        # Exchange rate label
        self.rate_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.rate_label.pack()
        
        # Last updated label
        self.updated_label = tk.Label(
            result_frame,
            text="",
            font=("Arial", 8),
            bg='#f0f0f0',
            fg='#999999'
        )
        self.updated_label.pack()
        
        # Swap button
        swap_btn = tk.Button(
            main_frame,
            text="↔ Swap Currencies",
            command=self.swap_currencies,
            font=("Arial", 10),
            bg='#FF9800',
            fg='white',
            relief='flat',
            padx=15,
            pady=5
        )
        swap_btn.pack(pady=10)
        
    def get_exchange_rate(self, from_curr, to_curr):
        """Get live exchange rate from API"""
        try:
            # Using a free API (no API key required for basic usage)
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data['rates']
            
            if to_curr in rates:
                return rates[to_curr], data['date']
            else:
                raise ValueError(f"Currency {to_curr} not found")
                
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch exchange rate: {str(e)}")
            return None, None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None, None
    
    def convert_currency(self):
        """Convert currency and display result"""
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if not from_curr or not to_curr:
                messagebox.showerror("Error", "Please select both currencies")
                return
            
            if from_curr == to_curr:
                self.result_label.config(text=f"{amount:.2f} {from_curr}")
                self.rate_label.config(text=f"1 {from_curr} = 1 {to_curr}")
                self.updated_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                return
            
            # Get exchange rate
            rate, date = self.get_exchange_rate(from_curr, to_curr)
            
            if rate is not None:
                converted_amount = amount * rate
                
                # Display result
                self.result_label.config(
                    text=f"{converted_amount:.2f} {to_curr}"
                )
                
                # Display exchange rate
                self.rate_label.config(
                    text=f"1 {from_curr} = {rate:.4f} {to_curr}"
                )
                
                # Display last updated
                self.updated_label.config(
                    text=f"Last updated: {date} {datetime.now().strftime('%H:%M:%S')}"
                )
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def swap_currencies(self):
        """Swap the from and to currencies"""
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)
        
        # Auto-convert after swap
        self.convert_currency()

def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
