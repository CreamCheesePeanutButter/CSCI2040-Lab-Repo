from tracker.trade import TradeHistory, Trade
from datetime import datetime
from db import get_db
class User:
    _l_name = ""
    _f_name = ""
    _tot_fund = 0
    _invested_fund = 0
    _free_fund = 0
    
    def __init__(self, userID, l_name, f_name, free_fund):
        self._id = userID
        self._l_name = l_name
        self._f_name = f_name
        self._free_fund = free_fund
        self._history_trade = TradeHistory(userID)

    def to_dict(self):
        return {
            "userID" :self._id,
            "l_name" : self._l_name,
            "f_name": self._f_name,
            "available_fund" : self._free_fund,
        }                   
    
    @staticmethod
    def from_dict(data):
        return User(data["user_id"], data["l_name"], data["f_name"], data["available_funds"])


    def get_l_name(self):
        return self._l_name
    def get_f_name(self):
        return self._f_name
    def get_tot_fund(self):
        return self._tot_fund
    def get_invested_fund(self):
        return self._invested_fund
    def get_free_fund(self):
        return self._free_fund
    from datetime import datetime
from db import get_db

def buy(self, num_stock, price, stock_key):
    pay_amount = num_stock * price

    if self._free_fund < pay_amount:
        return False

    # Update object values
    self._free_fund -= pay_amount
    self._invested_fund += pay_amount

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # Update only this user
        cursor.execute(
            """
            UPDATE user
            SET available_funds = %s,
                invested_funds = %s
            WHERE userID = %s
            """,
            (self._free_fund, self._invested_fund, self._id)
        )

        # Insert trade record
        cursor.execute(
            """
            INSERT INTO TradeTable
            (userID, stock_symbol, number_of_shares, price, transaction_date, transaction_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                self._id,
                stock_key,
                num_stock,
                price,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "BUY"
            )
        )

        db.commit()
        return True

    except Exception as e:
        db.rollback()
        print("Error:", e)
        return False

    finally:
        cursor.close()

    

        

    # when sold the buy is 0 
 
    