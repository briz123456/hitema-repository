import { useEffect, useState } from "react";

export default function App() {
  const [message, setMessage] = useState("Chargement...");
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setMessage(data.message))
      .catch((err) => setError(`API injoignable (${err.message})`));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", display: "grid", placeItems: "center", minHeight: "100vh", margin: 0 }}>
      <h1>{error ?? message}</h1>
    </main>
  );
}
