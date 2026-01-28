import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/data")
      .then((response) => response.json())
      .then((json) => setData(json));
  }, []);
  return (
    <>
      <h1>Hello, World!</h1>
      <h2>
        Data from Flask Backend: {data.length > 0 ? data[0].name : "No data"}
      </h2>
      <ol></ol>
    </>
  );
}

export default App;
