def inventory_health(stock, reorder):

    if stock < reorder:
        return "Reorder Required"

    elif stock > reorder * 3:
        return "Overstock"

    else:
        return "Healthy"