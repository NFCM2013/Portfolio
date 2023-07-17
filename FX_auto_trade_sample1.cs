// カスタム指標を読み込む
#include <MovingAverages.mqh>

// 外部パラメーターの設定
extern int fastMaPeriod = 20;  // 短期移動平均の期間
extern int slowMaPeriod = 50;  // 長期移動平均の期間
extern double lotSize = 0.1;   // トレードロットサイズ

// 初期化関数
int OnInit()
{
    // 初期化処理を実行するコードをここに追加
    return(INIT_SUCCEEDED);
}

// スタート関数
void OnStart()
{
    // 移動平均オブジェクトを作成する
    MovingAverages ma;
    
    // 短期移動平均を計算する
    double fastMa = ma.iMA(Symbol(), 0, fastMaPeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
    
    // 長期移動平均を計算する
    double slowMa = ma.iMA(Symbol(), 0, slowMaPeriod, 0, MODE_SMA, PRICE_CLOSE, 0);
    
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

// オーダー実行結果の処理関数
void OnTrade()
{
    // オーダー実行結果を処理するコードをここに追加
}

// タイマー処理関数
void OnTimer()
{
    // タイマーイベントに対する処理を実行するコードをここに追加
}

// カスタム関数など、必要に応じて追加の関数をここに記述することができます。
