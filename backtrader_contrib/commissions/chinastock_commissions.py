import backtrader as bt


class ChinaStockCommissionScheme(bt.CommInfoBase):
    '''
    https://www.zhihu.com/question/59369402
    股票交易费用包括三部分：
    1.印花税：成交金额的1‰,只有卖出时收取。
    2.过户费(仅上海股票收取)：每1000股收取1元，不足1000股按1元收取。
    3.券商交易佣金：最高为成交金额的3‰，最低5元起，单笔交易佣金不满5元按5元收取
    异地通讯费：由各券商自行决定收不收。 股票买进费用：
    1.佣金0.015%-0.3%，根据你的证券公司决定，但是佣金最低收取标准是5元。比如你买了1000元，实际佣金应该是3元，但是不到5元都按照5元收取。
    2.过户费(仅仅限于沪市)。每一千股收取1元，就是说你买卖一千股都要交1元。 股票卖出费用：
    1.印花税0.1%
    2.佣金0.015%-0.3%，根据你的证券公司决定，但是拥挤最低收取标准是5元。比如你买了1000元股票，实际佣金应该是3元，但是不到5元都按照5元收取。
    3.过户费(仅仅限于沪市)。每一千股收取1元，就是说你买卖一千股都要交1元。
    以上就是“股票交易手续费怎么计算?”的具体介绍。股票交易除了买卖股票的价格之外，还会收取佣金、过户费、印花税等等，所以你买入股票的成本价并不是你的成交价，是包含了佣金等手续费之后的价格，因此会有一个成本价。

    作者：雍雪友
    链接：https://www.zhihu.com/question/59369402/answer/164606606
    来源：知乎
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

    成交金额的1‰,只有卖出时收取。,                                                       -- 印花税，只有卖的时候收取
    每1000股收取1元，不足1000股按1元收取,                                                -- 过户费，买卖都收取，
    最高为成交金额的3‰，最低5元起，单笔交易佣金不满5元按5元收取 异地通讯费：由各券商自行决定收不收。 -- 券商交易佣金
    '''
    params = (
        ('tax_duty_per_trade_amount', 1/1000),
        ('exchange_fee_per_thousand_share', 1.0),
        ('exchange_fee_per_thousand_share_least', 1.0),
        ('broker_duty_per_trade_amount', 3/1000),
        ('broker_duty_per_trade_amount_least', 5.0),
        ('commission', 0),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
    )

    def _getcommission(self, size, price, pseudoexec):
        '''
        If size is greater than 0, this indicates a long / buying of shares.
        If size is less than 0, it idicates a short / selling of shares.
        '''
        if size > 0: #买
            tax_duty = 0
            exchange_fee = max(abs(size) * self.p.exchange_fee_per_thousand_share/1000,
                                      self.p.exchange_fee_per_thousand_share_least)
            broker_duty = max(abs(size) * price * self.p.broker_duty_per_trade_amount, self.p.broker_duty_per_trade_amount_least)
            return tax_duty + exchange_fee + broker_duty
        elif size < 0: #卖
            tax_duty = abs(size) * price * self.p.tax_duty_per_trade_amount
            exchange_fee = max(abs(size) * self.p.exchange_fee_per_thousand_share/1000,
                                      self.p.exchange_fee_per_thousand_share_least)
            broker_duty = max(abs(size) * price * self.p.broker_duty_per_trade_amount, self.p.broker_duty_per_trade_amount_least)
            return tax_duty + exchange_fee + broker_duty
        else:
            return 0  # just in case for some reason the size is 0.
