import { useEffect, useState } from "react";
import "./App.css";

export interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  created_at: Date;
}
function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [userNameInput, setUserNameInput] = useState<string>("none");
  const [userAgeInput, setUserAgeInput] = useState<string>("none");
  const [userEmailInput, setUserEmailInput] = useState<string>("none");
  const [userIDInput, setUserIDInput] = useState<number>(0);
  useEffect(() => {
    fetch("http://127.0.0.1:5000/users")
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
      })
      .catch((err) => {
        console.error("Error fetching users:", err);
      });
  }, []);

  return (
    <>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Age</th>
          </tr>
        </thead>

        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.age}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Name</h3>
      <input
        type="text"
        value={userNameInput}
        onChange={(e) => setUserNameInput(e.target.value)}
      />

      <h3>Age</h3>
      <input
        type="number"
        value={userAgeInput}
        onChange={(e) => setUserAgeInput(e.target.value)}
      />

      <h3>Email</h3>
      <input
        type="email"
        value={userEmailInput}
        onChange={(e) => setUserEmailInput(e.target.value)}
      />

      <h3>ID</h3>
      <input
        type="number"
        value={userIDInput}
        onChange={(e) => setUserIDInput(Number(e.target.value))}
      />
      <button
        onClick={() => {
          fetch("http://127.0.0.1:5000/users", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: userNameInput,
              age: userAgeInput,
              email: userEmailInput,
              id: userIDInput,
              date: new Date().toISOString(),
            }),
          });
        }}
      >
        Add User
      </button>
    </>
  );
}

export default App;
