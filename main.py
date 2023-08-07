import pandas as pd

class SMAStrategy:
    def __init__(self, index_data, option_data):
        self.index_data = "F:\Codes\Bhavi Project\lanknifty_data.csv"
        self.option_data = "F:\Codes\Bhavi Project\option_contract_data.xlsx"
        self.active_trade = None
        self.trades = []
        self.stop_loss = -20  
        self.target = 30  
    
    def calculate_sma(self, data, window):
        pass
    
    def is_trade_within_time_window(self, timestamp):
        start_time = pd.Timestamp(timestamp.date()) + pd.Timedelta(hours=9, minutes=30)
        end_time = pd.Timestamp(timestamp.date()) + pd.Timedelta(hours=15)
        return start_time <= timestamp <= end_time
    
    def is_trade_possible(self, timestamp):
        if self.active_trade is not None:
            return False
        return self.is_trade_within_time_window(timestamp)
    
    def execute_trade(self, trade_type, timestamp, price):
        if trade_type == 'Long':
            self.active_trade = {'type': 'Long', 'entry_time': timestamp, 'entry_price': price}
        elif trade_type == 'Short':
            self.active_trade = {'type': 'Short', 'entry_time': timestamp, 'entry_price': price}
    
    def record_trade(self, trade):
        self.trades.append(trade)
        trade_df = pd.DataFrame(self.trades)
        trade_df.to_csv('trades.csv', index=False)
    
    def check_exit_conditions(self, timestamp, price):
        if self.active_trade is None:
            return False
        
        trade_type = self.active_trade['type']
        entry_price = self.active_trade['entry_price']
        current_price = price
        
        if trade_type == 'Long':
            if current_price - entry_price >= self.target or current_price - entry_price <= self.stop_loss:
                return True
        elif trade_type == 'Short':
            if entry_price - current_price >= self.target or entry_price - current_price <= self.stop_loss:
                return True
        
        return False
    
    def exit_trade(self, timestamp, price):
        trade_type = self.active_trade['type']
        entry_time = self.active_trade['entry_time']
        entry_price = self.active_trade['entry_price']
        exit_price = price
        profit_loss = exit_price - entry_price if trade_type == 'Long' else entry_price - exit_price
        
        exit_trade = {
            'type': trade_type,
            'entry_time': entry_time,
            'entry_price': entry_price,
            'exit_time': timestamp,
            'exit_price': exit_price,
            'profit_loss': profit_loss
        }
        
        self.record_trade(exit_trade)
        self.active_trade = None
    
    def run_strategy(self):
        for timestamp, row in self.index_data.iterrows():
            if self.is_trade_possible(timestamp):
                if self.active_trade is not None and self.check_exit_conditions(timestamp, row['current_closing']):
                    self.exit_trade(timestamp, row['current_closing'])
            elif self.active_trade is not None and timestamp.time() == pd.Timestamp('15:00:00').time():
                self.exit_trade(timestamp, row['current_closing'])
    
    def analyze_results(self):
        pass

def main():
    
    index_data = pd.read_csv("F:\Codes\Bhavi Project\lanknifty_data.csv")  
    option_data = pd.read_excel('F:\Codes\Bhavi Project\option_contract_data.xlsx') 
    
    strategy = SMAStrategy(index_data, option_data)
    strategy.run_strategy()
    strategy.analyze_results()

if __name__ == "__main__":
    main()
