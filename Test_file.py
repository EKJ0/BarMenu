import pygame
import pypyodbc
import csv

# Database connection setup
Driver_name = "Sql Server"
Server_name = "BOOK-8AQHAH9SGN\\SQLEXPRESS"
Database_name = "BarRestaurant"

connection_string = f"Driver={{{Driver_name}}};Server={Server_name};Database={Database_name};Trusted_Connection=yes;"
conn = pypyodbc.connect(connection_string)

pygame.init()

# Function to read product prices from CSV
def read_product_prices():
    products = {}
    try:
        with open('products.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                products[row['product'].lower()] = float(row['price'])
    except FileNotFoundError:
        print("Error: products.csv file not found.")
    return products

# Load product prices
product_prices = read_product_prices()

def create_window():
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bar - Restaurant")

    menu_font = pygame.font.Font(None, 28)

    # Menu items (static display)
    menu_items = list(product_prices.keys())

    # Order tracking (internal, not displayed)
    current_order = []

    # Input handling
    quantity_input = ""
    product_input = ""
    input_box = pygame.Rect(50, height - 300, 200, 40)
    input_font = pygame.font.Font(None, 36)
    input_color_inactive = pygame.Color('lightpink3')
    input_color_active = pygame.Color('pink2')
    input_color = input_color_inactive
    input_active = False
    entering_quantity = True  # Determines if user is entering quantity or product name

    # Button properties
    button_size = 80  
    padding = 5
    start_x = 20  
    start_y = height - 250  

    # Define button labels
    button_labels = [
        "1", "2", "3", "Delete",
        "4", "5", "6", "0",
        "7", "8", "9", "OK"
    ]

    # Create buttons (3x4 grid)
    buttons = []
    font = pygame.font.Font(None, 36)

    for row in range(3):
        for col in range(4):
            x = start_x + col * (button_size + padding)
            y = start_y + row * (button_size + padding)
            button_rect = pygame.Rect(x, y, button_size, button_size)
            button_text = button_labels[row * 4 + col]
            text_surface = font.render(button_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            buttons.append((button_rect, text_surface, text_rect, button_text))

    # Add Check out button
    checkout_width = 150
    checkout_height = 60
    checkout_x = width - checkout_width - 20
    checkout_y = height - checkout_height - 20
    checkout_rect = pygame.Rect(checkout_x, checkout_y, checkout_width, checkout_height)
    checkout_text_surface = font.render("Check out", True, (0, 0, 0))
    checkout_text_rect = checkout_text_surface.get_rect(center=checkout_rect.center)

    buttons.append((checkout_rect, checkout_text_surface, checkout_text_rect, "Check out"))

    running = True
    while running:
        screen.fill((255, 255, 255))  # Clear screen before each draw

        # Draw instruction note in top right corner
        note_text = "Write quantity first, then product name"
        note_surface = menu_font.render(note_text, True, (255, 182, 193))  # Red text
        note_rect = note_surface.get_rect(topright=(width + 390, 10))
        screen.blit(note_surface, note_rect)
        
        # Draw menu items as a vertical list
        for i, item in enumerate(menu_items):
            text = menu_font.render(f"{i+1}. {item}: {product_prices[item]} ALL", True, (0, 0, 0))
            screen.blit(text, (20, 20 + i * 30))

        # Draw current order
        #order_y = 60  # Moved down to make space for the note
        #order_x = width - 200
        for item, qty, price in current_order:
            text = menu_font.render(f"{qty} x {item}: {price} ALL", True, (0, 0, 0))
            #screen.blit(text, (order_x, order_y))

            #order_y += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    input_color = input_color_active
                else:
                    input_active = False
                    input_color = input_color_inactive

                mouse_pos = pygame.mouse.get_pos()
                for button, _, _, button_text in buttons:
                    if button.collidepoint(mouse_pos):
                        if button_text == "Delete":
                            if entering_quantity:
                                quantity_input = quantity_input[:-1]
                            else:
                                product_input = product_input[:-1]
                        elif button_text == "OK":
                            if entering_quantity:
                                entering_quantity = False
                            else:
                                item_name = product_input.lower().strip()
                                if item_name in product_prices and quantity_input.isdigit():
                                    quantity = int(quantity_input)
                                    price = product_prices[item_name] * quantity
                                    current_order.append((item_name, quantity, price))
                                    print(f"Added to order: {quantity} x {item_name} - {price} ALL")
                                else:
                                    print(f"Invalid item or quantity: {quantity_input} {product_input}")
                                quantity_input, product_input = "", ""
                                entering_quantity = True
                        elif button_text == "Check out":
                            total = sum(price for _, _, price in current_order)
                            print(f"Final total: {total} ALL")  # Print total in terminal
                            running = False
                        else:
                            if entering_quantity:
                                quantity_input += button_text
                            else:
                                product_input += button_text
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if entering_quantity:
                        entering_quantity = False
                    else:
                        item_name = product_input.lower().strip()
                        if item_name in product_prices and quantity_input.isdigit():
                            quantity = int(quantity_input)
                            price = product_prices[item_name] * quantity
                            current_order.append((item_name, quantity, price))
                            print(f"Added to order: {quantity} x {item_name} - {price} ALL")
                        else:
                            print(f"Invalid item or quantity: {quantity_input} {product_input}")
                        quantity_input, product_input = "", ""
                        entering_quantity = True
                elif event.key == pygame.K_BACKSPACE:
                    if entering_quantity:
                        quantity_input = quantity_input[:-1]
                    else:
                        product_input = product_input[:-1]
                else:
                    if entering_quantity:
                        quantity_input += event.unicode
                    else:
                        product_input += event.unicode

        # Draw input box
        pygame.draw.rect(screen, input_color, input_box, 2)
        text_surface = input_font.render(quantity_input if entering_quantity else product_input, True, (0, 0, 0))
        width = max(200, text_surface.get_width() + 10)
        input_box.w = width
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Draw buttons and their labels
        for button, text_surface, text_rect, _ in buttons:
            pygame.draw.rect(screen, (200, 200, 200), button)
            pygame.draw.rect(screen, (100, 100, 100), button, 2)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
    pygame.quit()

create_window()
