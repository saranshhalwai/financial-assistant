import { useState } from 'react'
import { Textarea } from "./components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { Button } from "./components/ui/button"
import { Alert, AlertDescription, AlertTitle } from "./components/ui/alert"

function AnalysisCard({ title, content }) {
  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {typeof content === "object" && content !== null ? (
          <pre className="whitespace-pre-wrap text-sm">
            {JSON.stringify(content, null, 2)}
          </pre>
        ) : (
          <p>{String(content ?? "No data available")}</p>
        )}
      </CardContent>
    </Card>
  )
}


function App() {
  const [symbol, setSymbol] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  async function analyzeStock() {
    setError("");
    setAnalysis(null);

    if (!symbol.trim()) {
      setError("Please enter a stock symbol.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol })
      });

      if (!response.ok) {
        throw new Error("Failed to analyze stock.");
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="w-screen mx-auto mt-10">
      <Card>
        <CardHeader>
          <CardTitle>Stock Analyzer</CardTitle>
          <CardDescription>Enter a stock symbol to analyze.</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="Enter stock symbol, e.g. AAPL"
            className="w-full"
          />
          <Button onClick={analyzeStock} className="mt-3">Analyze</Button>

          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {analysis && (
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(analysis).map(([key, value]) => (
                <AnalysisCard
                  key={key}
                  title={key.replace(/_/g, " ")}
                  content={value}
                />
              ))}
            </div>
          )}

        </CardContent>
      </Card>
    </div>
  )
}

export default App
