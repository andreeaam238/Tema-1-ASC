"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from collections import deque
from threading import Lock, currentThread
import logging
from logging.handlers import RotatingFileHandler


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
        self.producers = deque()
        self.consumers = deque()
        self.product_producer_mapping = {}
        self.available_products = deque()
        self.producer_lock = Lock()
        self.consumer_lock = Lock()
        self.product_lock = Lock()
        self.produce_lock = Lock()

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = RotatingFileHandler('marketplace.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)8s: %(message)s')
        handler.setFormatter(formatter)
        logging.Formatter.converter = time.gmtime
        logger.addHandler(handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        logger = logging.getLogger()
        logger.info("register producer")

        with self.producer_lock:
            producer_id = len(self.producers)
            self.producers.append(0)

        logger.info("registered producer %d", producer_id)
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
        logger = logging.getLogger()
        logger.info("publish %s by %d", str(product), producer_id)

        if self.producers[producer_id] == self.queue_size_per_producer:
            logger.info("publishing %s by producer %d failed", str(product), producer_id)
            return False

        with self.produce_lock:
            self.producers[producer_id] += 1
            self.product_producer_mapping[product] = producer_id
            self.available_products.append(product)

        logger.info("publishing %s by producer %d succeeded", str(product), producer_id)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        logger = logging.getLogger()
        logger.info("new cart")

        with self.consumer_lock:
            cart_id = len(self.consumers)
            self.consumers.append(deque())

        logger.info("added cart %d", cart_id)
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
        logger = logging.getLogger()
        logger.info("add to cart %d %s", cart_id, str(product))

        with self.produce_lock:
            if product not in self.available_products:
                logger.info("adding %s to cart %d failed", str(product), cart_id)
                return False

            self.available_products.remove(product)

        self.consumers[cart_id].append(product)

        logger.info("adding %s to cart %d succeeded", str(product), cart_id)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        logger = logging.getLogger()
        logger.info("remove from cart %d %s", cart_id, str(product))

        if product in self.consumers[cart_id]:
            self.consumers[cart_id].remove(product)
            self.available_products.append(product)
            logger.info("removing %s from cart %d succeeded", str(product), cart_id)
        else:
            logger.info("removing %s from cart %d failed", str(product), cart_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        logger = logging.getLogger()
        logger.info("place order from cart %d", cart_id)

        with self.produce_lock:
            for product in self.consumers[cart_id]:
                self.producers[self.product_producer_mapping[product]] -= 1
                print(currentThread().getName() + " bought " + str(product))

        logger.info("cart %d placed an order", cart_id)
        return self.consumers[cart_id]
