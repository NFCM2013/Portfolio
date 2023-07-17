// 外部パラメーターの設定
extern int rsiPeriod = 14;      // RSIの期間
extern int overboughtLevel = 70;   // オーバーボートレベル
extern int oversoldLevel = 30;     // オーバーソルドレベル
extern double lotSize = 0.1;   // トレードロットサイズ

// スタート関数
void OnStart()
{
    // RSI値を計算する
    double rsi = iRSI(Symbol(), 0, rsiPeriod, PRICE_CLOSE, 0);
    
    // オーバーボート/オーバーソルドの判断
    if (rsi > overboughtLevel)
    {
        // オーバーボートの場合、売り注文を出す
        OrderSend(Symbol(), OP_SELL, lotSize, Bid, 3, Bid + StopLoss*Point, Bid - TakeProfit*Point);
    }
    else if (rsi < oversoldLevel)
    {
        // オーバーソルドの場合、買い注文を出す
        OrderSend(Symbol(), OP_BUY, lotSize, Ask, 3, Ask - StopLoss*Point, Ask + TakeProfit*Point);
    }
}
