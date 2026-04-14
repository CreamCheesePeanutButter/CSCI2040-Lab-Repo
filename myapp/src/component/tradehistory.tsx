import "./tradehistory.css";

type Trade = {
  symbol: string;
  shares: number;
  price: number;
  total: number;
  type: "BUY" | "SELL";
  date: string;
};

type TradeHistoryProps = {
  history: Trade[];
  userId: number;
};

export function TradeHistory({ history, userId }: TradeHistoryProps) {
  if (history.length === 0) {
    return <div className="th-empty">No trades yet</div>;
  }

  return (
    <div className="th-container">
      <h2 className="th-title">Trade History</h2>

      <a
        className="th-a"
        href={`http://localhost:5000/user/${userId}/generate-history-download`}
      >
        Export Trade History
      </a>

      <table className="th-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Symbol</th>
            <th>Type</th>
            <th>Shares</th>
            <th>Price</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {history.map((t, i) => (
            <tr key={i}>
              <td className="th-date">{t.date}</td>
              <td className="th-symbol">{t.symbol}</td>
              <td>
                <span
                  className={`th-badge ${t.type === "BUY" ? "th-buy" : "th-sell"}`}
                >
                  {t.type}
                </span>
              </td>
              <td>{t.shares}</td>
              <td>${t.price.toFixed(2)}</td>
              <td>${t.total.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
