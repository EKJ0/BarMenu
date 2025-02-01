import csv

class CSVfile:
    def __init__(self): 
        self.Products = [
            {"product": "coffee", "price": 100 },
            {"product": "tea", "price": 200 },
            {"product": "water", "price": 50 },
            {"product": "juice", "price": 90 },
            {"product": "beer", "price": 500 },
            {"product": "wine", "price": 600 },
            {"product": "cocktail", "price": 350 },
            {"product": "snack", "price": 100 },
            {"product": "dessert", "price": 200 },
        ]
    
    def write_to_csv(self):
        # Open the file for writing
        with open('products.csv', mode='w', newline='') as csvfile:
            # Get fieldnames from the first dictionary
            fieldnames = self.Products[0].keys()
            
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header
            writer.writeheader()
            
            # Write each row
            for row in self.Products:
                writer.writerow(row)

    def read_from_csv(self):
        products = {}
        with open('products.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                products[row['product']] = float(row['price'])
        return products

# Create an instance of the class and call the method to write to the file
csv_file = CSVfile()
csv_file.write_to_csv()
