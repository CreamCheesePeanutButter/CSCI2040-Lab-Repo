import React, { useState } from "react";
import "./portfolio.css";
import { useAuth } from "../context/AuthContext";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

type Holding = {
  companyName: string;
  symbol: string;
  shares: number;
  avgPrice: number;
  currentPrice: number;
};

type User = {
  username: string;
  portfolio: Holding[];
};

type PortfolioProps = {
  user: User | null;
  onTradeComplete?: () => void;
};

export function Portfolio({ user, onTradeComplete }: PortfolioProps) {
  const { user: authUser } = useAuth();
  const [sellRow, setSellRow] = useState<string | null>(null);
  const [sellQty, setSellQty] = useState("");
  const [sellLoading, setSellLoading] = useState(false);
  const [sellMsg, setSellMsg] = useState<{ symbol: string; msg: string; type: "success" | "error" } | null>(null);

  if (!user || user.portfolio.length === 0) {
    return <div className="portfolio-empty">You don't have any active trades</div>;
  }

  const handleSell = async (symbol: string) => {
    const qty = parseInt(sellQty, 10);
    if (!qty || qty < 1) {
      setSellMsg({ symbol, msg: "Enter a valid quantity.", type: "error" });
      return;
    }
    if (!authUser) return;
    setSellLoading(true);
    setSellMsg(null);
    try {
      const res = await fetch(`${API_URL}/user/${authUser.id}/sell`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_share: qty, stock_key: symbol }),
      });
      const data = await res.json();
      if (!res.ok) {
        setSellMsg({ symbol, msg: data.message ?? "Sell failed.", type: "error" });
      } else {
        setSellMsg({ symbol, msg: `Sold ${qty} share${qty > 1 ? "s" : ""}`, type: "success" });
        setSellRow(null);
        setSellQty("");
        onTradeComplete?.();
      }
    } catch {
      setSellMsg({ symbol, msg: "Network error.", type: "error" });
    } finally {
      setSellLoading(false);
    }
  };

  return (
    <div className="portfolio-container">
      <h2 className="portfolio-title">Portfolio</h2>

      <table className="portfolio-table">
        <thead>
          <tr>
            <th>Company Name</th>
            <th>Symbol</th>
            <th>Shares</th>
            <th>Avg Price</th>
            <th>Current Price</th>
            <th>Up/Down</th>
            <th>Sell</th>
          </tr>
        </thead>

        <tbody>
          {user.portfolio.map((holding) => {
            const profit = (holding.currentPrice - holding.avgPrice) * holding.shares;
            const isSelling = sellRow === holding.symbol;

            return (
              <tr key={holding.symbol}>
                <td>{holding.companyName}</td>
                <td>{holding.symbol}</td>
                <td>{holding.shares}</td>
                <td>${holding.avgPrice.toFixed(2)}</td>
                <td>${holding.currentPrice.toFixed(2)}</td>
                <td className={profit >= 0 ? "profit" : "loss"}>
                  {profit >= 0 ? "+" : ""}${profit.toFixed(2)}
                </td>
                <td className="portfolio-sell-cell">
                  {isSelling ? (
                    <div className="portfolio-sell-row">
                      <input
                        type="number"
                        className="portfolio-sell-input"
                        min="1"
                        max={holding.shares}
                        value={sellQty}
                        onChange={(e) => setSellQty(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSell(holding.symbol)}
                        placeholder="Qty"
                        autoFocus
                      />
                      <button
                        className="portfolio-sell-confirm"
                        onClick={() => handleSell(holding.symbol)}
                        disabled={sellLoading}
                      >
                        {sellLoading ? "..." : "Confirm"}
                      </button>
                      <button
                        className="portfolio-sell-cancel"
                        onClick={() => { setSellRow(null); setSellQty(""); setSellMsg(null); }}
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      className="portfolio-sell-btn"
                      onClick={() => { setSellRow(holding.symbol); setSellQty(""); setSellMsg(null); }}
                    >
                      Sell
                    </button>
                  )}
                  {sellMsg?.symbol === holding.symbol && (
                    <p className={`portfolio-sell-msg ${sellMsg.type === "error" ? "portfolio-sell-error" : "portfolio-sell-success"}`}>
                      {sellMsg.msg}
                    </p>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
