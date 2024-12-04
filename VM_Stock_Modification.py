import customtkinter as ctk
from tkinter import messagebox, Toplevel

class VendingMachineApp:
    def __init__(self, root):
        self.root = root
        self.center_window(600, 600)
        self.root.title("Vending Machine")

        self.total_price = 0
        self.cart = {}  # Cart will store {item_name: (price, quantity)}
        self.selected_item = None
        self.selected_price = 0

        # Initialize items with price and stock values
        self.items = {
            "Soda": (1.5, 10),
            "Chips": (2.0, 8),
            "Candy": (1.0, 15),
            "Water": (1.2, 20),
            "Juice": (2.5, 12),
            "Cookies": (3.0, 5),
            "Nuts": (2.8, 7),
            "Gum": (0.5, 50),
            "Coffee": (3.5, 10),
            "Tea": (3.0, 8),
            "Granola Bar": (1.8, 20),
            "Crackers": (1.7, 15),
            "Milk": (1.6, 10),
            "Energy Drink": (2.9, 10),
            "Popcorn": (2.3, 12),
            "Pretzels": (2.1, 15),
            "Protein Bar": (2.4, 8),
            "Biscuits": (1.9, 18),
            "Yogurt": (3.2, 6),
            "Chewing Gum": (0.8, 30),
            "Ice Cream": (3.6, 5),
            "Mints": (0.7, 40),
            "Chocolates": (1.2, 25),
            "Smoothie": (3.8, 7),
            "Seltzer": (2.2, 15),
            "Choco Bar": (2.1, 10),
            "Cereal Bar": (2.0, 12),
            "Fruit Snacks": (1.5, 20),
            "Brownie": (3.3, 10),
            "Cupcake": (3.4, 8),
            "Trail Mix": (2.7, 15),
            "Rice Cake": (1.3, 18),
        }

        # Initialize stock separately
        self.stock = {item: quantity for item, (_, quantity) in self.items.items()}
        self.create_widgets()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)
        self.root.geometry(f"{width}x{height}+{position_right}+{position_top}")

    def create_widgets(self):
        header_label = ctk.CTkLabel(self.root, text="               Welcome to The Vending Machine", font=("Arial", 40, "bold"))
        header_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create a frame for the item buttons (4x8 grid)
        items_frame = ctk.CTkFrame(self.root, width=400, height=400)
        items_frame.grid(row=1, column=0, pady=3, padx=20, sticky="nsew")

        for col in range(4):
            items_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        self.item_buttons = {}
        row = 0
        col = 0
        for item, (price, _) in self.items.items():
            button = ctk.CTkButton(
                items_frame,
                text=f"{item}\n${price}\nStock: {self.stock[item]}",
                command=lambda item=item, price=price: self.select_item(item, price),
                font=("Arial", 20), width=20, height=15
            )
            button.grid(row=row, column=col, padx=5, pady=7, sticky="ew")
            self.item_buttons[item] = button
            col += 1
            if col >= 4:
                col = 0
                row += 1

        cart_frame = ctk.CTkFrame(self.root, width=150, height=300)
        cart_frame.grid(row=1, column=1, pady=90, padx=5, sticky="nsew")
        cart_frame.grid_columnconfigure(0, weight=1)

        self.slider_label = ctk.CTkLabel(cart_frame, text="Select Quantity: 0", font=("Arial", 16))
        self.slider_label.grid(row=1, column=0, pady=10, sticky="nsew")

        self.quantity_slider = ctk.CTkSlider(cart_frame, from_=0, to=30, command=self.update_quantity)
        self.quantity_slider.grid(row=2, column=0, pady=5, sticky="nsew")

        add_button = ctk.CTkButton(cart_frame, text="Add to Cart", command=self.add_to_cart, width=200, height=70, font=("Arial", 18))
        add_button.grid(row=3, column=0, pady=10, sticky="nsew")

        edit_item_button = ctk.CTkButton(cart_frame, text="Edit Item in Cart", command=self.edit_cart_item, width=200, height=70, font=("Arial", 18))
        edit_item_button.grid(row=4, column=0, pady=10, sticky="nsew")

        remove_last_button = ctk.CTkButton(cart_frame, text="Remove Last", command=self.remove_last_addition, width=200, height=70, font=("Arial", 18))
        remove_last_button.grid(row=5, column=0, pady=10, sticky="nsew")

        checkout_button = ctk.CTkButton(cart_frame, text="Checkout", command=self.checkout, width=200, height=70, font=("Arial", 18))
        checkout_button.grid(row=6, column=0, pady=10, sticky="nsew")

        reset_button = ctk.CTkButton(cart_frame, text="Reset", command=self.reset, width=200, height=70, font=("Arial", 18))
        reset_button.grid(row=7, column=0, pady=10, sticky="nsew")

        self.selected_items_frame = ctk.CTkFrame(self.root, width=300, height=300)
        self.selected_items_frame.grid(row=1, column=2, pady=5, padx=5, sticky="nsew")

        self.selected_items_list = ctk.CTkLabel(self.selected_items_frame, text="", font=("Arial", 16))
        self.selected_items_list.grid(row=0, column=0, pady=5, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def select_item(self, item, price):
        self.selected_item = item
        self.selected_price = price
        self.slider_label.configure(text="Select Quantity: 0")
        self.quantity_slider.set(0)

    def update_quantity(self, value):
        self.slider_label.configure(text=f"Select Quantity: {int(value)}")

    def add_to_cart(self):
        quantity = int(self.quantity_slider.get())
        if self.selected_item and quantity > 0:
            available_stock = self.stock[self.selected_item]
            if quantity <= available_stock:
                if self.selected_item in self.cart:
                    current_price, current_quantity = self.cart[self.selected_item]
                    self.cart[self.selected_item] = (current_price, current_quantity + quantity)
                else:
                    self.cart[self.selected_item] = (self.selected_price, quantity)

                self.total_price += self.selected_price * quantity
                self.stock[self.selected_item] -= quantity
                self.update_cart_display()
            else:
                messagebox.showerror("Stock Error", "Not enough stock available.")
        else:
            messagebox.showwarning("Selection Error", "Please select an item and a quantity.")

    def update_cart_display(self):
        selected_items = "\n".join([f"{item}: {qty} x ${price} = ${price * qty:.2f}" for item, (price, qty) in self.cart.items()])
        self.selected_items_list.configure(text=selected_items)
        for item, (price, _) in self.items.items():
            self.item_buttons[item].configure(text=f"{item}\n${price}\nStock: {self.stock[item]}")

    def remove_last_addition(self):
        if self.cart:
            last_item = list(self.cart.keys())[-1]  # Get the last item in the cart
            price, quantity = self.cart[last_item]
            self.total_price -= price * quantity  # Subtract the price of the last item
            del self.cart[last_item]  # Remove the last item from the cart

            # Restore the stock
            self.stock[last_item] += quantity

            self.update_cart_display()  # Update the displayed cart items
        else:
            self.selected_items_list.configure(text="Cart is empty.")

    def edit_cart_item(self):
        def update_item():
            new_quantity = int(quantity_slider.get())
            if new_quantity <= self.stock[selected_item_var.get()]:
                current_price, _ = self.cart[selected_item_var.get()]
                self.cart[selected_item_var.get()] = (current_price, new_quantity)
                self.update_cart_display()

        def delete_item():
            item_to_delete = selected_item_var.get()
            if item_to_delete in self.cart:
                price, quantity = self.cart[item_to_delete]
                self.total_price -= price * quantity
                del self.cart[item_to_delete]
                self.stock[item_to_delete] += quantity
                self.update_cart_display()

        edit_window = Toplevel(self.root)
        edit_window.title("Edit Cart Item")
        edit_window.geometry("300x600")

        selected_item_var = ctk.StringVar(value=list(self.cart.keys())[0])

        ctk.CTkLabel(edit_window, text="Select Item",font=("Arial",18)).pack(pady=15)
        item_menu = ctk.CTkOptionMenu(edit_window, values=list(self.cart.keys()), variable=selected_item_var,font=("Arial",18))
        item_menu.pack(pady=10)

        ctk.CTkLabel(edit_window, text="New Quantity",font=("Arial",18)).pack(pady=10)
        quantity_slider = ctk.CTkSlider(edit_window, from_=0, to=30)
        quantity_slider.pack(pady=20)

        slider_value_label = ctk.CTkLabel(edit_window, text=f"Quantity: {int(quantity_slider.get())}",font=("Arial",18))
        slider_value_label.pack(pady=15)

        def update_slider_value(val):
            slider_value_label.configure(text=f"Quantity: {int(val)}")

        quantity_slider.configure(command=update_slider_value)

        update_button = ctk.CTkButton(edit_window, text="Update", command=update_item,font=("Arial",18))
        update_button.pack(pady=15)

        delete_button = ctk.CTkButton(edit_window, text="Delete Item", command=delete_item, fg_color="red",font=("Arial",18))
        delete_button.pack(pady=15)

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Checkout", "Your cart is empty!")
            return
        messagebox.showinfo("Checkout", f"Your total is ${self.total_price:.2f}")

    def reset(self):
        self.cart.clear()
        self.total_price = 0
        self.update_cart_display()

if __name__ == "__main__":
    root = ctk.CTk()
    app = VendingMachineApp(root)
    root.mainloop()
