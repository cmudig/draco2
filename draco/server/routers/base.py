from abc import ABC, abstractmethod

from fastapi import APIRouter

from draco import Draco


class BaseDracoRouter(APIRouter, ABC):
    """
    Abstract :code:`APIRouter` declaring a group of endpoints
    which might make use of an underlying :code:`Draco` instance,
    injectable via the constructor.

    `Read more about APIRouter
    <https://fastapi.tiangolo.com/advanced/custom-request-and-route/?h=apiroute>`_
    """

    def __init__(self, draco: Draco, **kwargs):
        """
        :param draco: the underlying :code:`Draco` instance
                      to be used by the router endpoints.
        :param kwargs: keyword arguments to be passed
                       to the :code:`APIRouter` constructor.
        """
        super().__init__(**kwargs)
        self.draco = draco

    @staticmethod
    @abstractmethod
    def _register(router: "BaseDracoRouter"):
        """
        Template method to be used to declare the actual endpoints of the router.
        Declared endpoints get registered to the enclosing
        :code:`FastAPI` instance automatically. Derived classes should
        override this method to declare their endpoints.

        :param router: the router instance to be used to declare the endpoints.
        """
        raise NotImplementedError  # pragma: no cover

    def register(self):
        """
        Convenience method to register the endpoints of the router
        by calling the :code:`_register` method.
        """
        self._register(self)
