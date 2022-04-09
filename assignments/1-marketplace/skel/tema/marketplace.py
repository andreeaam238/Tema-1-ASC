"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock, currentThread


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = []
        self.consumers = []
        self.products = {}
        self.producer_lock = Lock()
        self.consumer_lock = Lock()
        self.product_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producer_lock:
            producer_id = len(self.producers)
            self.producers.append({})

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if sum(self.producers[producer_id].values()) == self.queue_size_per_producer:
            return False

        if product not in self.producers[producer_id]:
            self.producers[producer_id][product] = 1
            self.products[product] = producer_id
        else:
            with self.product_lock:
                self.producers[producer_id][product] += 1

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.consumer_lock:
            cart_id = len(self.consumers)
            self.consumers.append([])

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.product_lock:
            for producer in self.producers:
                if product in producer.keys() and producer[product] > 0:
                    self.consumers[cart_id].append(product)
                    self.producers[self.producers.index(producer)][product] -= 1
                    return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.product_lock:
            if product in self.consumers[cart_id]:
                self.consumers[cart_id].remove(product)
                self.producers[self.products[product]][product] += 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        order = []

        for product in self.consumers[cart_id]:
            order.append(product)
            print(currentThread().getName() + " bought " + str(product))

        self.consumers[cart_id] = []

        return order
