//+------------------------------------------------------------------+
//|                                              IchimokuPropFirm.mq5|
//|                   Ichimoku Kinko Hyo Trend EA + Prop Helper      |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, Afu & Clio"
#property version   "1.10"

#include <Trade/Trade.mqh>

//+------------------------------------------------------------------+
//| INPUT PARAMETERS                                                 |
//+------------------------------------------------------------------+
input string aa = "------------------SETTINGS----------------------";
input string BOT_NAME      = "Ichimoku Kinko Hyo Prop Firm EA";
input int    EXPERT_MAGIC  = 2026;
input ENUM_TIMEFRAMES TRADING_TIMEFRAME = PERIOD_M15;

input string bb = "----------------ICHIMOKU------------------------";
input int    TENKAN_PERIOD    = 9;
input int    KIJUN_PERIOD     = 26;
input int    SENKOU_B_PERIOD  = 52;

input string cc = "----------------RISK PROFILE--------------------";
input double RISK_PER_TRADE      = 1.0;   // Percent of equity per trade
input double KUMO_SL_BUFFER_MULT = 0.2;   // ATR multiplier for SL buffer
input double RR_TARGET            = 0.0;  // Risk-Reward TP multiple (0 = disabled)

input string dd = "-------------PROP FIRM CHALLENGE----------------";
input bool   isChallenge      = false;
input double PASS_CRITERIA    = 110100.0;
input double DAILY_LOSS_LIMIT = 4500.0;

input string ee = "-------------FILTERS & CONFIRM------------------";
input bool   USE_HTF_CONFIRM     = false;
input ENUM_TIMEFRAMES CONFIRM_TIMEFRAME = PERIOD_H1;
input bool   USE_TIME_FILTER     = false;
input int    START_HOUR          = 7;   // server time
input int    END_HOUR            = 23;  // server time
input bool   USE_ATR_FILTER      = false;
input double ATR_MIN             = 0.0; // 0 = disabled / no minimum

input string ff = "-----------------DEBUG-------------------------";
input bool   DEBUG_LOG = false;
input double CHIKOU_TOUCH_BUFFER_POINTS = 0.0; // extra tolerance around candle for "touch"

//+------------------------------------------------------------------+
//| GLOBAL VARIABLES                                                 |
//+------------------------------------------------------------------+
CTrade trade;
int    ichi_handle = INVALID_HANDLE;

//+------------------------------------------------------------------+
//| UTILITIES                                                        |
//+------------------------------------------------------------------+
void DebugPrint(string msg)
{
   if(DEBUG_LOG)
      Print(msg);
}

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   trade.SetExpertMagicNumber(EXPERT_MAGIC);
   trade.SetDeviationInPoints(10);

   ichi_handle = iIchimoku(_Symbol, TRADING_TIMEFRAME,
                           TENKAN_PERIOD, KIJUN_PERIOD, SENKOU_B_PERIOD);
   if(ichi_handle == INVALID_HANDLE)
   {
      Print("Failed to create Ichimoku handle");
      return(INIT_FAILED);
   }

   Print(BOT_NAME, " initialized!");
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   if(ichi_handle != INVALID_HANDLE)
      IndicatorRelease(ichi_handle);

   Print(BOT_NAME, " exited, exit code: ", reason);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   if(isChallenge)
   {
      if(isPassed())
      {
         ClearAll("Prop Firm Challenge Passed!");
         return;
      }
      else if(isDailyLimit())
      {
         ClearAll("Daily loss limit exceeded!");
         return;
      }
   }

   ExecuteTrade();
}

//+------------------------------------------------------------------+
//| MAIN TRADE EXECUTION                                             |
//+------------------------------------------------------------------+
void ExecuteTrade()
{
   if(!BarOpen())
      return;

   // Time filter (server time)
   if(USE_TIME_FILTER)
   {
      MqlDateTime dt;
      TimeToStruct(TimeCurrent(), dt);
      int hour = dt.hour;
      if(START_HOUR <= END_HOUR)
      {
         if(hour < START_HOUR || hour > END_HOUR)
         {
            DebugPrint("Time filter blocking trading");
            return;
         }
      }
      else
      {
         // window wraps midnight (e.g., 22 -> 2)
         if(!(hour >= START_HOUR || hour <= END_HOUR))
         {
            DebugPrint("Time filter (wrapped) blocking trading");
            return;
         }
      }
   }

   // ATR filter
   if(USE_ATR_FILTER && ATR_MIN > 0.0)
   {
      double atr_now = ATR(14, 1, TRADING_TIMEFRAME);
      if(atr_now < ATR_MIN)
      {
         DebugPrint("ATR filter blocking trading, ATR=" + DoubleToString(atr_now, 5));
         return;
      }
   }

   // Manage existing positions first (Ichimoku-based exit)
   int long_positions  = PositionManaging(POSITION_TYPE_BUY);
   int short_positions = PositionManaging(POSITION_TYPE_SELL);

   // Only one side at a time
   if(long_positions > 0 || short_positions > 0)
      return;

   bool bullish = IsBullishIchimokuSignal();
   bool bearish = IsBearishIchimokuSignal();

   // Higher timeframe confirmation if enabled
   if(USE_HTF_CONFIRM)
   {
      if(bullish && !IsHTFAlignedBullish())
         bullish = false;
      if(bearish && !IsHTFAlignedBearish())
         bearish = false;
   }

   if(bullish)
   {
      DebugPrint("Bullish Ichimoku signal -> attempting long entry");
      OpenBullishPosition();
   }
   else if(bearish)
   {
      DebugPrint("Bearish Ichimoku signal -> attempting short entry");
      OpenBearishPosition();
   }
}

//+------------------------------------------------------------------+
//| ICHIMOKU UTILITIES                                               |
//+------------------------------------------------------------------+

bool LoadIchimokuBuffers(double &tenkan[], double &kijun[], double &spanA[], double &spanB[], double &chikou[])
{
   if(ichi_handle == INVALID_HANDLE)
      return(false);

   int bars_needed = 200; // enough history for shifts
   if(CopyBuffer(ichi_handle, 0, 0, bars_needed, tenkan) <= 0) return(false);
   if(CopyBuffer(ichi_handle, 1, 0, bars_needed, kijun)  <= 0) return(false);
   if(CopyBuffer(ichi_handle, 2, 0, bars_needed, spanA)  <= 0) return(false);
   if(CopyBuffer(ichi_handle, 3, 0, bars_needed, spanB)  <= 0) return(false);
   if(CopyBuffer(ichi_handle, 4, 0, bars_needed, chikou) <= 0) return(false);

   return(true);
}

// Check bullish Ichimoku entry rules on the last closed bar
bool IsBullishIchimokuSignal()
{
   double tenkan[], kijun[], spanA[], spanB[], chikou[];
   if(!LoadIchimokuBuffers(tenkan, kijun, spanA, spanB, chikou))
      return(false);

   int shift = 1; // last closed bar
   if(shift >= ArraySize(tenkan) || shift >= ArraySize(kijun) ||
      shift >= ArraySize(spanA)  || shift >= ArraySize(spanB))
      return(false);

   // 1) Tenkan above Kijun
   double tenkan_val = tenkan[shift];
   double kijun_val  = kijun[shift];
   if(!(tenkan_val > kijun_val))
      return(false);

   // 2) Price currently inside Kumo + Kumo bullish
   double close_val = iClose(_Symbol, TRADING_TIMEFRAME, shift);
   double spanA_now = spanA[shift];
   double spanB_now = spanB[shift];
   double kumo_top  = MathMax(spanA_now, spanB_now);
   double kumo_bot  = MathMin(spanA_now, spanB_now);

   // cloud orientation: bullish
   if(!(spanA_now > spanB_now))
      return(false);

   // price inside cloud: spanB < price < spanA
   if(!(close_val < kumo_top && close_val > kumo_bot))
      return(false);

   // 3) Future Kumo also bullish (if data exists ahead)
   int future_index = shift + 26;
   if(future_index < ArraySize(spanA) && future_index < ArraySize(spanB))
   {
      double spanA_future = spanA[future_index];
      double spanB_future = spanB[future_index];
      if(!(spanA_future > spanB_future))
         return(false);
   }

   // 4) Chikou span free from past price (above historic high)
   int chikou_index = shift + 26;
   int total_bars   = Bars(_Symbol, TRADING_TIMEFRAME);
   if(chikou_index < total_bars && chikou_index < ArraySize(chikou))
   {
      double chikou_val = chikou[chikou_index];
      double past_high  = iHigh(_Symbol, TRADING_TIMEFRAME, chikou_index);
      if(!(chikou_val > past_high))
         return(false); // not free
   }

   return(true);
}

// Check bearish Ichimoku entry rules on the last closed bar
bool IsBearishIchimokuSignal()
{
   double tenkan[], kijun[], spanA[], spanB[], chikou[];
   if(!LoadIchimokuBuffers(tenkan, kijun, spanA, spanB, chikou))
      return(false);

   int shift = 1;
   if(shift >= ArraySize(tenkan) || shift >= ArraySize(kijun) ||
      shift >= ArraySize(spanA)  || shift >= ArraySize(spanB))
      return(false);

   // 1) Tenkan below Kijun
   double tenkan_val = tenkan[shift];
   double kijun_val  = kijun[shift];
   if(!(tenkan_val < kijun_val))
      return(false);

   // 2) Price currently inside Kumo + Kumo bearish
   double close_val = iClose(_Symbol, TRADING_TIMEFRAME, shift);
   double spanA_now = spanA[shift];
   double spanB_now = spanB[shift];
   double kumo_top  = MathMax(spanA_now, spanB_now);
   double kumo_bot  = MathMin(spanA_now, spanB_now);

   // cloud orientation: bearish
   if(!(spanA_now < spanB_now))
      return(false);

   // price inside cloud (spanA < spanB now, so cloud inverted visually)
   if(!(close_val > kumo_bot && close_val < kumo_top))
      return(false);

   // 3) Future Kumo also bearish (if data exists ahead)
   int future_index = shift + 26;
   if(future_index < ArraySize(spanA) && future_index < ArraySize(spanB))
   {
      double spanA_future = spanA[future_index];
      double spanB_future = spanB[future_index];
      if(!(spanA_future < spanB_future))
         return(false);
   }

   // 4) Chikou span free from past price (below historic low)
   int chikou_index = shift + 26;
   int total_bars   = Bars(_Symbol, TRADING_TIMEFRAME);
   if(chikou_index < total_bars && chikou_index < ArraySize(chikou))
   {
      double chikou_val = chikou[chikou_index];
      double past_low   = iLow(_Symbol, TRADING_TIMEFRAME, chikou_index);
      if(!(chikou_val < past_low))
         return(false); // not free
   }

   return(true);
}

// Higher timeframe confirmation (simplified: cloud orientation + price location)
bool IsHTFAlignedBullish()
{
   int handle = iIchimoku(_Symbol, CONFIRM_TIMEFRAME,
                          TENKAN_PERIOD, KIJUN_PERIOD, SENKOU_B_PERIOD);
   if(handle == INVALID_HANDLE)
      return(false);

   double spanA[], spanB[];
   int bars_needed = 100;
   if(CopyBuffer(handle, 2, 0, bars_needed, spanA) <= 0 ||
      CopyBuffer(handle, 3, 0, bars_needed, spanB) <= 0)
   {
      IndicatorRelease(handle);
      return(false);
   }

   int shift = 1;
   if(shift >= ArraySize(spanA) || shift >= ArraySize(spanB))
   {
      IndicatorRelease(handle);
      return(false);
   }

   double spanA_now = spanA[shift];
   double spanB_now = spanB[shift];
   double close_val = iClose(_Symbol, CONFIRM_TIMEFRAME, shift);
   double kumo_top  = MathMax(spanA_now, spanB_now);

   bool ok = (spanA_now > spanB_now && close_val > kumo_top);
   IndicatorRelease(handle);
   return(ok);
}

bool IsHTFAlignedBearish()
{
   int handle = iIchimoku(_Symbol, CONFIRM_TIMEFRAME,
                          TENKAN_PERIOD, KIJUN_PERIOD, SENKOU_B_PERIOD);
   if(handle == INVALID_HANDLE)
      return(false);

   double spanA[], spanB[];
   int bars_needed = 100;
   if(CopyBuffer(handle, 2, 0, bars_needed, spanA) <= 0 ||
      CopyBuffer(handle, 3, 0, bars_needed, spanB) <= 0)
   {
      IndicatorRelease(handle);
      return(false);
   }

   int shift = 1;
   if(shift >= ArraySize(spanA) || shift >= ArraySize(spanB))
   {
      IndicatorRelease(handle);
      return(false);
   }

   double spanA_now = spanA[shift];
   double spanB_now = spanB[shift];
   double close_val = iClose(_Symbol, CONFIRM_TIMEFRAME, shift);
   double kumo_bot  = MathMin(spanA_now, spanB_now);

   bool ok = (spanA_now < spanB_now && close_val < kumo_bot);
   IndicatorRelease(handle);
   return(ok);
}

//+------------------------------------------------------------------+
//| OPEN LONG POSITION                                               |
//+------------------------------------------------------------------+
void OpenBullishPosition()
{
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double atr = ATR(14, 1, TRADING_TIMEFRAME);

   double tenkan[], kijun[], spanA[], spanB[], chikou[];
   if(!LoadIchimokuBuffers(tenkan, kijun, spanA, spanB, chikou))
      return;

   int shift = 1;
   if(shift >= ArraySize(spanA) || shift >= ArraySize(spanB))
      return;

   double spanA_now = spanA[shift];
   double spanB_now = spanB[shift];
   double kumo_bot  = MathMin(spanA_now, spanB_now);

   // SL below Kumo with ATR buffer
   double sl_price = kumo_bot - KUMO_SL_BUFFER_MULT * atr;
   double sl_value = ask - sl_price;
   if(sl_value <= 0)
      return;

   double tp_price = 0.0;
   if(RR_TARGET > 0.0)
   {
      double risk = sl_value;
      tp_price = ask + RR_TARGET * risk;
   }

   double lot_size   = CalculateLotSize(sl_value, ask);
   double max_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);

   while(lot_size > max_volume)
   {
      trade.Buy(max_volume, _Symbol, ask, sl_price, tp_price, "Ichimoku long (partial)");
      lot_size -= max_volume;
   }

   if(lot_size > 0)
      trade.Buy(lot_size, _Symbol, ask, sl_price, tp_price, "Ichimoku long");
}

//+------------------------------------------------------------------+
//| OPEN SHORT POSITION                                              |
//+------------------------------------------------------------------+
void OpenBearishPosition()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double atr = ATR(14, 1, TRADING_TIMEFRAME);

   double tenkan[], kijun[], spanA[], spanB[], chikou[];
   if(!LoadIchimokuBuffers(tenkan, kijun, spanA, spanB, chikou))
      return;

   int shift = 1;
   if(shift >= ArraySize(spanA) || shift >= ArraySize(spanB))
      return;

   double spanA_now = spanA[shift];
   double spanB_now = spanB[shift];
   double kumo_top  = MathMax(spanA_now, spanB_now);

   // SL above Kumo with ATR buffer
   double sl_price = kumo_top + KUMO_SL_BUFFER_MULT * atr;
   double sl_value = sl_price - bid;
   if(sl_value <= 0)
      return;

   double tp_price = 0.0;
   if(RR_TARGET > 0.0)
   {
      double risk = sl_value;
      tp_price = bid - RR_TARGET * risk;
   }

   double lot_size   = CalculateLotSizeSell(sl_value, bid);
   double max_volume = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);

   while(lot_size > max_volume)
   {
      trade.Sell(max_volume, _Symbol, bid, sl_price, tp_price, "Ichimoku short (partial)");
      lot_size -= max_volume;
   }

   if(lot_size > 0)
      trade.Sell(lot_size, _Symbol, bid, sl_price, tp_price, "Ichimoku short");
}

//+------------------------------------------------------------------+
//| Manage existing positions (Ichimoku-based exit)                  |
//+------------------------------------------------------------------+
int PositionManaging(ENUM_POSITION_TYPE position_type)
{
   int positions = 0;

   double tenkan[], kijun[], spanA[], spanB[], chikou[];
   bool have_ichi = LoadIchimokuBuffers(tenkan, kijun, spanA, spanB, chikou);

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong posTicket = PositionGetTicket(i);
      if(PositionSelectByTicket(posTicket))
      {
         if(PositionGetString(POSITION_SYMBOL) == _Symbol &&
            PositionGetInteger(POSITION_MAGIC)  == EXPERT_MAGIC &&
            PositionGetInteger(POSITION_TYPE)   == position_type)
         {
            positions++;

            if(have_ichi)
            {
               // Close when Chikou touches price (no longer free)
               if(IsChikouTouchingPrice(chikou))
               {
                  DebugPrint("Closing position due to Chikou touching price");
                  trade.PositionClose(posTicket);
                  positions--;
               }
            }
         }
      }
   }

   return(MathMax(positions, 0));
}

// Check if Chikou span is touching past price (no longer free)
bool IsChikouTouchingPrice(double &chikou[])
{
   int shift = 1;
   int chikou_index = shift + 26;

   int total_bars = Bars(_Symbol, TRADING_TIMEFRAME);
   if(chikou_index >= total_bars || chikou_index >= ArraySize(chikou))
      return(false);

   double buf  = CHIKOU_TOUCH_BUFFER_POINTS * _Point;
   double chikou_val = chikou[chikou_index];
   double past_high  = iHigh(_Symbol, TRADING_TIMEFRAME, chikou_index) + buf;
   double past_low   = iLow(_Symbol, TRADING_TIMEFRAME, chikou_index)  - buf;

   // Consider "touching" when Chikou is inside the (buffered) past candle's range
   if(chikou_val <= past_high && chikou_val >= past_low)
      return(true);

   return(false);
}

//+------------------------------------------------------------------+
//| SUPPORTING FUNCTIONS (reused / adapted from propfirm.mq5)        |
//+------------------------------------------------------------------+

double ATR(int period, int shift, ENUM_TIMEFRAMES timeframe)
{
   int handle = iATR(_Symbol, timeframe, period);
   if(handle == INVALID_HANDLE)
      return(0.0);

   double value[];
   if(CopyBuffer(handle, 0, shift, 1, value) <= 0)
      return(0.0);

   return(value[0]);
}

// Calculate lot size for BUY based on risk % of equity per trade
double CalculateLotSize(double sl_value, double price)
{
   double lots = 0.0;
   double loss = 0.0;

   double balance  = AccountInfoDouble(ACCOUNT_EQUITY);
   double sl_price = price - sl_value;

   if(OrderCalcProfit(ORDER_TYPE_BUY, _Symbol, 1.0, price, sl_price, loss))
   {
      double lotstep    = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
      double risk_money = RISK_PER_TRADE * balance / 100.0;
      double margin     = 0.0;

      lots = risk_money / MathAbs(loss);
      lots = MathFloor(lots / lotstep) * lotstep;

      double minlot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
      double maxlot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);

      if(lots < minlot)
         lots = minlot;

      if(OrderCalcMargin(ORDER_TYPE_BUY, _Symbol, lots, price, margin))
      {
         double free_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
         if(free_margin < 0)
            lots = 0;
         else if(free_margin < margin)
         {
            lots = lots * free_margin / margin;
            lots = MathFloor(lots / lotstep - 1) * lotstep;
         }
      }
   }

   return(MathMax(lots, SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN)));
}

// Calculate lot size for SELL based on risk % of equity per trade
double CalculateLotSizeSell(double sl_value, double price)
{
   double lots = 0.0;
   double loss = 0.0;

   double balance  = AccountInfoDouble(ACCOUNT_EQUITY);
   double sl_price = price + sl_value; // for short, SL above entry

   if(OrderCalcProfit(ORDER_TYPE_SELL, _Symbol, 1.0, price, sl_price, loss))
   {
      double lotstep    = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
      double risk_money = RISK_PER_TRADE * balance / 100.0;
      double margin     = 0.0;

      lots = risk_money / MathAbs(loss);
      lots = MathFloor(lots / lotstep) * lotstep;

      double minlot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
      double maxlot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);

      if(lots < minlot)
         lots = minlot;

      if(OrderCalcMargin(ORDER_TYPE_SELL, _Symbol, lots, price, margin))
      {
         double free_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
         if(free_margin < 0)
            lots = 0;
         else if(free_margin < margin)
         {
            lots = lots * free_margin / margin;
            lots = MathFloor(lots / lotstep - 1) * lotstep;
         }
      }
   }

   return(MathMax(lots, SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN)));
}

// Check if new bar is created
bool BarOpen()
{
   static datetime m_prev_bar = 0;
   datetime bar_time = iTime(_Symbol, TRADING_TIMEFRAME, 0);
   if(bar_time == m_prev_bar)
      return(false);

   m_prev_bar = bar_time;
   return(true);
}

// Delete all pending orders and exit all positions
void ClearAll(string message)
{
   Comment(message);

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong orderTicket = OrderGetTicket(i);
      if(OrderSelect(orderTicket))
         trade.OrderDelete(orderTicket);
   }

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong posTicket = PositionGetTicket(i);
      trade.PositionClose(posTicket);
   }
}

// Check if we have achieved profit target
bool isPassed()
{
   return(AccountInfoDouble(ACCOUNT_EQUITY) > PASS_CRITERIA);
}

// Check if we are about to violate maximum daily loss
bool isDailyLimit()
{
   MqlDateTime date_time;
   TimeToStruct(TimeCurrent(), date_time);
   int current_day   = date_time.day;
   int current_month = date_time.mon;
   int current_year  = date_time.year;

   double current_balance = AccountInfoDouble(ACCOUNT_BALANCE);

   HistorySelect(0, TimeCurrent());
   int orders = HistoryDealsTotal();

   double PL = 0.0;
   for(int i = orders - 1; i >= 0; i--)
   {
      ulong ticket = HistoryDealGetTicket(i);
      if(ticket == 0)
      {
         Print("HistoryDealGetTicket failed, no trade history");
         break;
      }

      double profit = HistoryDealGetDouble(ticket, DEAL_PROFIT);
      if(profit != 0)
      {
         MqlDateTime deal_time;
         TimeToStruct(HistoryDealGetInteger(ticket, DEAL_TIME), deal_time);

         if(deal_time.day == current_day &&
            deal_time.mon == current_month &&
            deal_time.year == current_year)
            PL += profit;
         else
            break;
      }
   }

   double starting_balance = current_balance - PL;
   double current_equity   = AccountInfoDouble(ACCOUNT_EQUITY);
   return(current_equity < starting_balance - DAILY_LOSS_LIMIT);
}
