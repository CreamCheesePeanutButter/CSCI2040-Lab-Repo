import React from "react";
import "./profilebar.css";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";


type User = {
    username: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    balance?: number;
 };

type ProfileBarProps = {
  user: User | null;
  activeTab: "portfolio" | "history";
  onTabChange: (tab: "portfolio" | "history") => void;
};

export function ProfileBar({ user, activeTab, onTabChange }: ProfileBarProps) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="profile-bar">

      <div className="profile-top">
        <h2 className="username">{user?.username ?? "—"}</h2>
        {(user?.firstName || user?.lastName) && (
          <p className="subtext">{user.firstName} {user.lastName}</p>
        )}
        {user?.email && <p>{user.email}</p>}
        {user?.balance != null && (
          <p className="profile-balance">${user.balance.toFixed(2)} available</p>
        )}
      </div>

      <div className="profile-bottom">

        <button
          className={activeTab === "portfolio" ? "active" : ""}
          onClick={() => onTabChange("portfolio")}
        >
          Portfolio
        </button>

        <button
          className={activeTab === "history" ? "active" : ""}
          onClick={() => onTabChange("history")}
        >
          Trade History
        </button>

        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>

      </div>
    </div>
  );
}