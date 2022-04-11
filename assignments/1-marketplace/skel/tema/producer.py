"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        # Register the producer in the marketplace
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        # Cycle through the products that the producer is able to produce and try to add them to the marketplace
        while True:
            for product in self.products:
                quantity = product[1]

                for _ in range(quantity):
                    # If the producer's array is full then he has to wait until he tries to republish it
                    while not self.marketplace.publish(self.producer_id, product[0]):
                        time.sleep(self.republish_wait_time)

                    # The product has been added to the marketplace and the producer has to wait until he can produce a
                    # new product
                    time.sleep(product[2])
