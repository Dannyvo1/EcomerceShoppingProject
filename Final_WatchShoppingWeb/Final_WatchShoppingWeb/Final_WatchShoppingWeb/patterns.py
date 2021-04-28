
"""
Define an interface for creating an object, but let subclasses decide
which class to instantiate. Factory Method lets a class defer
instantiation to subclasses.
"""

import abc
from abc import ABC
from Final_WatchShoppingWeb import db, _session
from Final_WatchShoppingWeb.customer.model import CustomerOrder
from Final_WatchShoppingWeb.models import addProduct
from Final_WatchShoppingWeb.products.models import Product

####factory pattern
class order_action(metaclass=abc.ABCMeta):
    """
    Declare the factory method, which returns an object of type Product.
    Creator may also define a default implementation of the factory
    method that returns a default ConcreteProduct object.
    Call the factory method to create a Product object.
    """
    @abc.abstractmethod
    def generat_data(self):
        pass


class Get_Order(order_action):
    
    def __init__(self, id, invoice, orders):
        self.id = id
        self.invoice = invoice
        self.orders = orders

    def generate_data(self):
        return CustomerOrder(customer_id = self.id, invoice = self.invoice, orders=self.orders)

class Get_order_byId(order_action):
    def generat_data(self):
        return 
    
class order_factory:
    def create_order(self, id, invoice, orders):
        self.id = id
        self.invoice = invoice
        self.orders = orders
        return Get_Order(self.id, self.invoice, self.orders).generat_data()

###Command pattern
class Command(metaclass=abc.ABCMeta):
    """
    The Command interface declares a method for executing a command.
    """

    @abc.abstractmethod
    def execute(self) -> None:
        pass

class searchcommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, word: str):
        self._word = word

    def execute(self):
        return addProduct.query.msearch(self._word, fields=['name', 'disc'], limit=6)

class viewdetailscommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, id: int):
        self._id = id

    def execute(self):
        return _session.query(Product).filter(Product.id == self._id).all()


class Invoker:
    """
    The Invoker is associated with one or several commands. It sends a request
    to the command.
    """

    _on_start = None
    _on_finish = None

    """
    Initialize commands.
    """

    def set_on_start(self, command: Command):
        self._on_start = command

    def set_on_finish(self, command: Command):
        self._on_finish = command

    def do_something_important(self):
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        
        if isinstance(self._on_start, Command):
            return self._on_start.execute()


        if isinstance(self._on_finish, Command):
            return self._on_finish.execute()
####