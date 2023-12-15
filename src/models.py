from sqlalchemy import Table, select, MetaData, Column, Integer, String, ForeignKey, Float, DATETIME
from sqlalchemy.orm import relationship, join, column_property, DeclarativeBase


class Base(DeclarativeBase):
    pass


metadata = MetaData()


class AppTables:
    ACCOUNT = 'account'
    TRANSACTION = 'transact'


class AccountModelColumns:
    """
    Class defining column names for the AccountModel.
    """
    CODE = 'account_code'
    NATURE = 'account_nature'


class TransactionModelColumns:
    """
    Class defining column names for the TransactionModel.
    """
    CODE = 'account_code'
    TYPE = 'transaction_type'
    AMOUNT = 'amount'
    DATE = 'transaction_date'


class TransactionType:
    """
    Enumeration defining transaction types.
    """
    DEBIT = 'debit'
    CREDIT = 'credit'


class AccountNature:
    """
    Enumeration defining account natures.
    """
    INCOME = 'income'
    EXPENSE = 'expense'


class Account(Base):
    __tablename__ = AppTables.ACCOUNT

    id = Column(Integer, primary_key=True)
    account_code = Column(Integer, index=True)
    account_nature = Column(String)
    transactions = relationship('Transaction')


class Transaction(Base):
    __tablename__ = AppTables.TRANSACTION

    id = Column(Integer, primary_key=True)
    account_code = Column(Integer, ForeignKey(f'{AppTables.ACCOUNT}.account_code'))
    transaction_type = Column(String)
    amount = Column(Float)
    transaction_date = Column(DATETIME, index=True)


transaction_account_join = join(Transaction, Account)


class TransactionWithAccount(Base):
    __table__ = transaction_account_join

    id = column_property(Transaction.id)
    account_code = column_property(Transaction.account_code, Account.account_code)
    transaction_type = Transaction.transaction_type
    amount = Transaction.amount
    transaction_date = Transaction.transaction_date
    account_nature = Account.account_nature
    acc_id = column_property(Account.id)

    def __str__(self):
        return (f'account_code = {self.account_code}, '
                f'transaction_type = "{self.transaction_type}", '
                f'amount = {self.amount}, '
                f'transaction_date = {self.transaction_date}, '
                f'account_nature = "{self.account_nature}"')

    def as_dict(self):
        obj = {
            'account_code': self.account_code,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'transaction_date': self.transaction_date,
            'account_nature': self.account_nature,
        }
        return obj
