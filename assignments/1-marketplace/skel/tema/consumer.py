"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            for operation in cart:
                operation_type = operation['type']
                quantity = operation['quantity']
                product = operation['product']

                for _ in range(quantity):
                    if operation_type == 'add':
                        while not self.marketplace.add_to_cart(cart_id, product):
                            time.sleep(self.retry_wait_time)
                    elif operation_type == 'remove':
                        self.marketplace.remove_from_cart(cart_id, product)

            self.marketplace.place_order(cart_id)
