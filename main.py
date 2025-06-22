import csv
from pprint import pprint

def get_items_to_list():
    
    with open('input.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        items = []
        for row in reader:
            
            if row['Listed'] == "FALSE" and 'sf' not in row['Custom Label (SKU)']:
                if int(row['Custom Label (SKU)']) > 70:
                    items.append(row)
        return items        

def create_ebay_draft_csv(items, output_filename='ebay_draft_listings.csv'):
    """
    Create an eBay draft listings CSV file using the same format as output.csv
    
    Args:
        items: List of item dictionaries from get_items_to_list()
        output_filename: Name of the output CSV file
    """
    
    # Define the header rows that match the output.csv format
    header_rows = [
        ['#INFO', 'Version=0.0.2', 'Template= eBay-draft-listings-template_US', '', '', '', '', '', '', '', ''],
        ['#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html', '', '', '', '', '', '', '', '', '', ''],
        ['#INFO After you\'ve successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.com/sh/lst/drafts', '', '', '', '', '', '', '', '', '', ''],
        ['#INFO', '', '', '', '', '', '', '', '', '', ''],
        ['Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)', 'Custom label (SKU)', 'Category ID', 'Title', 'UPC', 'Price', 'Quantity', 'Item photo URL', 'Condition ID', 'Description', 'Format']
    ]
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header rows
        for row in header_rows:
            writer.writerow(row)
        
        # Write the item data rows
        for item in items:
            # Extract data from item dictionary and format for eBay CSV
            sku = item.get('Custom Label (SKU)', '')
            title = item.get('Title', 'Default Title')
            price = item.get('Price', '0').replace('$', '') if item.get('Price') else '0'  # Remove $ sign
            quantity = item.get('Quantity', '1')
            condition_id = item.get('Condition ID', 'NEW')
            description = item.get('Description', '<p><CENTER><H4>This is a Test Auction...Please Do Not Bid</H4></CENTER><P>This is one of those test auctions. Please do not bid as there is no merchandise being auctioned.</P>')
            
            # Create the data row for this item
            data_row = [
                'Draft',  # Action
                sku,      # Custom label (SKU)
                '47140',  # Category ID (you may want to customize this based on item type)
                title,    # Title
                '',       # UPC
                price,    # Price
                quantity, # Quantity
                '',       # Item photo URL
                condition_id,  # Condition ID
                description,   # Description
                'FixedPrice'   # Format
            ]
            
            writer.writerow(data_row)
    
    print(f"eBay draft listings CSV created: {output_filename}")
    print(f"Total items processed: {len(items)}")

def main():
    items = get_items_to_list()
    pprint(items)
    
    # Create the eBay draft listings CSV
    create_ebay_draft_csv(items)

if __name__ == "__main__":
    main()
