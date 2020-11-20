import backtrader as bt


class USDCommissionScheme(bt.CommInfoBase):
    '''
    https://www.itiger.com/help/detail/ussf?lang=en_US
    $0.0039/share, at least 0.99 per trade,             Trading commission by TigerBrokers
    $0.00396/share, at least 0.99 per trade,            External Ageency fee and trading activity fee by Exteral agency
    0.0000207 * total trading amount,                   SEC memebership fee(only charged upon issuance of sales voucher)
    $0.004/share, at least $1 per trade ,               Platform fee by TigerBrokers;
    '''
    params = (
        ('trading_commission_duty_per_share', 0.0039),
        ('trading_commission_least_per_trade', 0.99),
        ('external_agency_duty_per_share', 0.00396),
        ('external_agency_least_per_trade', 0.99),
        ('membership_fee_per_trade_amount', 0.0000207),
        ('platform_fee_duty_per_share', 0.004),
        ('platform_fee_least_per_trade', 1.00),
        ('commission', 0),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
    )

    def _getcommission(self, size, price, pseudoexec):
        '''
        If size is greater than 0, this indicates a long / buying of shares.
        If size is less than 0, it idicates a short / selling of shares.
        '''
        if size > 0:
            trading_commission = max(size * self.p.trading_commission_duty_per_share,
                                     self.p.trading_commission_least_per_trade)
            external_agency_fee = max(size * self.p.external_agency_duty_per_share,
                                      self.p.external_agency_least_per_trade)
            platform_fee = max(size * self.p.platform_fee_duty_per_share, self.p.platform_fee_least_per_trade)
            return trading_commission + external_agency_fee + platform_fee
        elif size < 0:
            trading_commission = max(abs(size) * self.p.trading_commission_duty_per_share,
                                     self.p.trading_commission_least_per_trade)
            external_agency_fee = max(abs(size) * self.p.external_agency_duty_per_share,
                                      self.p.external_agency_least_per_trade)
            platform_fee = max(abs(size) * self.p.platform_fee_duty_per_share, self.p.platform_fee_least_per_trade)
            membership_fee = price * abs(size) * self.p.membership_fee_per_trade_amount
            return trading_commission + external_agency_fee + platform_fee + membership_fee
        else:
            return 0  # just in case for some reason the size is 0.


class HKDCommissionScheme(bt.CommInfoBase):
    '''
    https://www.itiger.com/help/detail/hksf?lang=en_US
    0.03%*trading value                                                             Trading commission by TigerBrokers
    0.005% * trading value + HKD0.5                                                 Trading fee, Hong Kong Exchanges and Clearing Limited (“HKEX”)
    0.002% * trading value (at least HKD2 and at most HKD100)                       Settlement and delivery cost, HKEX
    0.0027% * trading value ,                                                       Transaction levy, HKEX
    0.1% * trading value (amount less than HKD1 will also be counted as HKD1),      Stamp duty,Hong Kong Special Administrative Region Government (“GovHK”)
    HKD15                                                                           Platform fee by Tiger Brokers
    - Currency in HKD.
    '''
    params = (
        ('trading_commission_percent', 0.03 / 100),
        ('trading_fee_percent', 0.005 / 100),
        ('trading_fee_amount', 0.5),
        ('settlement_and_delivery_cost_percent', 0.002 / 100),
        ('settlement_and_delivery_cost_at_least', 2),
        ('settlement_and_delivery_cost_at_most', 100),
        ('transaction_levy_percent', 0.0027 / 100),
        ('stamp_duty_percent', 0.1 / 100),
        ('stamp_duty_at_least', 1),
        ('platform_fee', 15),
        ('commission', 0),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
    )

    def _getcommission(self, size, price, pseudoexec):
        '''
        If size is greater than 0, this indicates a long / buying of shares.
        If size is less than 0, it idicates a short / selling of shares.
        '''
        trading_value = abs(size) * price
        trading_commission = trading_value * self.p.trading_commission_percent
        trading_fee = trading_value * self.p.trading_fee_percent + self.p.trading_fee_amount
        settlement_and_delivery_cost_p = trading_value * self.p.settlement_and_delivery_cost_percent
        settlement_and_delivery_cost = min(
            max(settlement_and_delivery_cost_p, self.p.settlement_and_delivery_cost_at_least),
            self.p.settlement_and_delivery_cost_at_most)
        transaction_levy = trading_value* self.p.transaction_levy_percent
        stamp_duty = max(trading_value * self.p.stamp_duty_percent, self.p.stamp_duty_at_least)
        platform_fee = self.p.platform_fee
        return trading_commission + trading_fee + settlement_and_delivery_cost + transaction_levy + stamp_duty + platform_fee
