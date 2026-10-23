from .store_init import store_init
from .store_add import store_add
from .store_emails import store_emails

class Store:

    __init__ = store_init
    add = store_add
    emails = store_emails
