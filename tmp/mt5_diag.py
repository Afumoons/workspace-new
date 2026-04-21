import MetaTrader5 as mt5
print('init', mt5.initialize())
print('version', mt5.version())
for s in ['XAUUSDm','XAUUSDc','BTCUSDm']:
    info = mt5.symbol_info(s)
    print('symbol', s, 'exists', info is not None)
    if info is not None:
        print('  visible', info.visible, 'select', mt5.symbol_select(s, True))
        print('  tick', mt5.symbol_info_tick(s))
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M15, 0, 5)
        print('  rates_none', rates is None, 'last_error', mt5.last_error())
mt5.shutdown()
