import uuid


def generator(instance, filter='ref_no'):
    """
    It generate random codes and makes sure it does not exist in that object
    db table
    """
    code = str(uuid.uuid1().int)[:6]
    filter = { filter: code }
    if instance.__class__.objects.filter(**filter).exists():
        return generate_code(instance)

    return code
