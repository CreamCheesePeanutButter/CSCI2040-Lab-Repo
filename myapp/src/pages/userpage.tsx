import { useEffect, useState, useCallback } from "react";
import "./userpage.css";
import { ProfileBar } from "../component/profilebar";
import { Portfolio } from "../component/portfolio";
import { TradeHistory } from "../component/tradehistory";
import { useAuth } from "../context/AuthContext";
import { useRefresh } from "../context/RefreshContext";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

type Holding = {
  companyName: string;
  symbol: string;
  shares: number;
  avgPrice: number;
  currentPrice: number;
};

type Trade = {
  symbol: string;
  shares: number;
  price: number;
  total: number;
  type: "BUY" | "SELL";
  date: string;
};

function Userpage() {
  const { user } = useAuth();
  const { refreshKey } = useRefresh();
  const [activeTab, setActiveTab] = useState<"portfolio" | "history">("portfolio");
  const [portfolio, setPortfolio] = useState<Holding[]>([]);
  const [history, setHistory] = useState<Trade[]>([]);
  const [profileUser, setProfileUser] = useState<{
    username: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    balance?: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(() => {
    if (!user) return;
    Promise.all([
      fetch(`${API_URL}/user/${user.id}/info`).then((r) => r.json()),
      fetch(`${API_URL}/user/${user.id}/portfolio`).then((r) => r.json()),
      fetch(`${API_URL}/user/${user.id}/history`).then((r) => r.json()),
    ]).then(([infoData, portfolioData, historyData]) => {
      const u = infoData.users?.[0];
      if (u) {
        setProfileUser({
          username: u.username,
          firstName: u.first_name,
          lastName: u.last_name,
          email: u.email,
          balance: u.available_funds,
        });
      }
      setPortfolio(portfolioData.portfolio ?? []);
      setHistory(historyData.history ?? []);
    }).finally(() => setLoading(false));
  }, [user]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60_000);
    return () => clearInterval(interval);
  }, [fetchData, refreshKey]);

  if (!user) return <div className="portfolio-empty">Please log in.</div>;
  if (loading) return <div className="portfolio-empty">Loading...</div>;

  return (
    <>
      <ProfileBar
        user={profileUser}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      <div style={{ marginLeft: "250px" }}>
        {activeTab === "portfolio" ? (
          <Portfolio
            user={{ username: user.username, portfolio }}
            onTradeComplete={fetchData}
          />
        ) : (
          <TradeHistory history={history} />
        )}
      </div>
    </>
  );
}

export default Userpage;
