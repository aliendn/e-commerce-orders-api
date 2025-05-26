import boto3

table = boto3.resource("dynamodb").Table("Orders")

def save_order(order_id, customer, items):
    return table.put_item(Item={
        "order_id": order_id,
        "customer": customer,
        "items": items
    })

def get_order(order_id):
    response = table.get_item(Key={"order_id": order_id})
    return response.get("Item")
