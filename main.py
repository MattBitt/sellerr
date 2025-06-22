import csv
import os
from pathlib import Path
from pprint import pprint
import glob
# UPDATE THIS AFTER RUNNING THE SCRIPT TO GET READY FOR NEXT TIME
LAST_ITEM_LISTED = 70

def delete_old_csvs_in_output():
    """
    Delete any existing CSV files in the output folder
    """
    output_folder = Path("output")
    
    # Check if output folder exists
    if not output_folder.exists():
        print("Output folder does not exist, creating it...")
        output_folder.mkdir(parents=True, exist_ok=True)
        return
    
    # Find all CSV files in the output folder
    csv_files = list(output_folder.glob("*.csv"))
    
    if not csv_files:
        print("No old CSV files found in output folder")
        return
    
    # Delete each CSV file
    for csv_file in csv_files:
        try:
            csv_file.unlink()
            print(f"Deleted old CSV file: {csv_file.name}")
        except Exception as e:
            print(f"Error deleting {csv_file.name}: {e}")
    
    print(f"Cleaned up {len(csv_files)} old CSV file(s) from output folder")


def get_newest_csv():
    """
    Return the name of the newest CSV file in the 'inputs' folder

    Returns:
        str: The filename of the newest CSV file, or None if no CSV files found
    """
    inputs_folder = Path("inputs")

    # Check if inputs folder exists
    if not inputs_folder.exists():
        print("Warning: 'inputs' folder does not exist")
        return None

    # Get all CSV files in the inputs folder
    csv_files = list(inputs_folder.glob("*.csv"))

    if not csv_files:
        print("Warning: No CSV files found in 'inputs' folder")
        return None

    # Find the newest file based on modification time
    newest_file = max(csv_files, key=os.path.getmtime)

    print(f"Using newest CSV file: {newest_file.name}")
    return str(newest_file)


def get_items_to_list():
    """
    Get items to list from the newest CSV file in the inputs folder

    Returns:
        list: List of item dictionaries that meet the criteria
    """
    csvfile_path = get_newest_csv()

    # Fall back to input.csv if no file found in inputs folder
    if csvfile_path is None:
        print("Falling back to 'input.csv' in root directory")
        csvfile_path = "input.csv"

    try:
        with open(csvfile_path) as csvfile:
            reader = csv.DictReader(csvfile)
            items = []
            for row in reader:
                try:
                    item_number = int(row["Custom Label (SKU)"])
                except ValueError:
                    continue
                
                if item_number > LAST_ITEM_LISTED:
                    items.append(row)
            return items
    except FileNotFoundError:
        print(f"Error: Could not find file {csvfile_path}")
        return []
    except Exception as e:
        print(f"Error reading file {csvfile_path}: {e}")
        return []


def create_ebay_draft_csv(items, output_filename="output/ebay_draft_listings.csv"):
    """
    Create an eBay draft listings CSV file using the same format as output.csv

    Args:
        items: List of item dictionaries from get_items_to_list()
        output_filename: Name of the output CSV file
    """
    # Delete any old CSV files in the output folder before creating new one
    delete_old_csvs_in_output()
    
    # Define the header rows that match the output.csv format
    header_rows = [
        [
            "#INFO",
            "Version=0.0.2",
            "Template= eBay-draft-listings-template_US",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "#INFO Action and Category ID are required fields. 1) Set Action to Draft 2) Please find the category ID for your listings here: https://pages.ebay.com/sellerinformation/news/categorychanges.html",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "#INFO After you've successfully uploaded your draft from the Seller Hub Reports tab, complete your drafts to active listings here: https://www.ebay.com/sh/lst/drafts",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        ["#INFO", "", "", "", "", "", "", "", "", "", ""],
        [
            "Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)",
            "Custom label (SKU)",
            "Category ID",
            "Title",
            "UPC",
            "Price",
            "Quantity",
            "Item photo URL",
            "Condition ID",
            "Description",
            "Format",
        ],
    ]

    with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header rows
        for row in header_rows:
            writer.writerow(row)

        # Write the item data rows
        for item in items:
            # Extract data from item dictionary and format for eBay CSV
            sku = str(item.get("Custom Label (SKU)", ""))
            title = item.get("Title", "Default Title")
            price = (
                item.get("Price", "0").replace("$", "") if item.get("Price") else "0"
            )  # Remove $ sign
            quantity = item.get("Quantity", "1")
            condition_id = item.get("Condition ID", "NEW")
            description = item.get(
                "Description",
                " ",
            )

            # Create the data row for this item
            data_row = [
                "Draft",  # Action
                sku,  # Custom label (SKU)
                "47140",  # Category ID (you may want to customize this based on item type)
                title,  # Title
                "",  # UPC
                price,  # Price
                quantity,  # Quantity
                "",  # Item photo URL
                condition_id,  # Condition ID
                description,  # Description
                "FixedPrice",  # Format
            ]

            writer.writerow(data_row)

    print(f"eBay draft listings CSV created: {output_filename}")
    print(f"Total items processed: {len(items)}")


def main():
    # Delete old CSV files in the output folder
    delete_old_csvs_in_output()

    items = get_items_to_list()
    pprint(items)

    # Create the eBay draft listings CSV
    create_ebay_draft_csv(items)


if __name__ == "__main__":
    main()
