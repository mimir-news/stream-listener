# Standard library
from abc import ABCMeta, abstractmethod
from typing import List

# Internal modules
from app import db
from app.models import Stock


class StockRepo(metaclass=ABCMeta):
    """Interface for storage and retrieval of Stock entinties."""

    @abstractmethod
    def get_all(self, include_inactive: bool = False) -> List[Stock]:
        """Gets stored Stocks either only active of all.

        :return: List of all stored stocks.
        """

    @abstractmethod
    def save(self, stock: Stock) -> None:
        """Stores a new stock.

        :param stock: Stock to store.
        """


class SQLStockRepo(StockRepo):
    """StockRepo implemented against a SQL database."""

    def get_all(self, include_inactive: bool = False) -> List[Stock]:
        if include_inactive:
            return db.session.query(Stock).all()
        return db.session.query(Stock).filter(Stock.is_active == True).all()


    def save(self, stock: Stock) -> None:
        db.session.add(stock)
        db.session.commit()
