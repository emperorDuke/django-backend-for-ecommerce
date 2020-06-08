
#promo there is a 5% off

PROMO = None

TAX = None

def calculate_bill(*order):

    try:
        q_set = order.items.all()
    raise Exception (
        'no ordered items'
    )

    prices = [item.product.price if not item.product.discount_price else item.product.discount_price for item in q_set]

    return total_price = sum(prices)







