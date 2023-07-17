// 外部パラメーターの設定
extern int fastMaPeriod = 20;  // 短期移動平均の期間
extern int slowMaPeriod = 50;  // 長期移動平均の期間
extern double lotSize = 0.1;   // トレードロットサイズ

// スタート関数
void OnStart()
{
    // 移動平均オブジェクトを作成する
    double fastMa = iMA(Symbol(), 0, fastMaPeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
    double slowMa = iMA(Symbol(), 0, slowMaPeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
    
    // トレンドの方向を判断する
    if (fastMa > slowMa)
    {
        // 上昇トレンドの場合、買い注文を出す
        OrderSend(Symbol(), OP_BUY, lotSize, Ask, 3, Ask - StopLoss*Point, Ask + TakeProfit*Point);
    }
    else if (fastMa < slowMa)
    {
        // 下降トレンドの場合、売り注文を出す
        OrderSend(Symbol(), OP_SELL, lotSize, Bid, 3, Bid + StopLoss*Point, Bid - TakeProfit*Point);
    }
}
