from math import ceil
from datetime import datetime

def calculate_points(receipt):
    try:
        points = 0

        # Rule 1: One point for every alphanumeric character in the retailer name
        points += sum(c.isalnum() for c in receipt['retailer'])
        # print("1", points)

        # Rule 2: 50 points if the total is a round dollar amount with no cents
        total = float(receipt['total'])
        if total.is_integer():
            points += 50
        # print("2", points)

        # Rule 3: 25 points if the total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25
        # print("3", points)

        # Rule 4: 5 points for every two items on the receipt
        print(len(receipt['items']))
        points += (len(receipt['items']) // 2) * 5
        # print("4", points)

        # Rule 5: Points based on item description length and price
        for item in receipt['items']:
            description_length = len(item['shortDescription'].strip())
            if description_length % 3 == 0:
                item_price = float(item['price'])
                points += ceil(item_price * 0.2)
        # print("5", points)

        # Rule 6: 6 points if the day in the purchase date is odd
        purchase_date = receipt['purchaseDate']
        if purchase_date.day % 2 != 0:
            points += 6
        # print("6", points)

        # Rule 7: 10 points if the time is between 2:00pm and 4:00pm
        purchase_time = receipt['purchaseTime']
        if purchase_time >= datetime.strptime("14:00", "%H:%M").time() and purchase_time <= datetime.strptime("16:00", "%H:%M").time():
            points += 10
        # print("7", points)

        return points

    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid receipt data: {e}")


def prepare_receipt_data(receipt):
    """
    Prepare the receipt data in the format required for point calculation.
    """
    return {
        "retailer": receipt.retailer,
        "purchaseDate": receipt.purchase_date,
        "purchaseTime": receipt.purchase_time,
        "total": receipt.total,
        "items": [
            {"shortDescription": item.short_description, "price": item.price}
            for item in receipt.items.all()
        ],
    }
