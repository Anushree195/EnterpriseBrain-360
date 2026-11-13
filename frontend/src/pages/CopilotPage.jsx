
import { useEffect, useState } from "react";
import { getCustomers, askCopilot } from "../services/api";
import "./CopilotPage.css";

function CopilotPage() {
    const [customers, setCustomers] = useState([]);
    const [customerId, setCustomerId] = useState("");
    const [question, setQuestion] = useState("");

    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);
    const [customersLoading, setCustomersLoading] = useState(true);

    const [error, setError] = useState("");

    // Load available customers
    useEffect(() => {
        async function loadCustomers() {
            try {
                const data = await getCustomers();
                setCustomers(data);
            } catch (err) {
                setError(`Could not load customers: ${err.message}`);
            } finally {
                setCustomersLoading(false);
            }
        }

        loadCustomers();
    }, []);

    // Ask the AI Copilot
    async function handleAskCopilot(event) {
        event.preventDefault();

        if (!question.trim()) {
            setError("Please enter a question.");
            return;
        }

        try {
            setLoading(true);
            setError("");
            setResponse(null);

            // Build request without customer_id for general queries
            const requestData = {
                question: question.trim(),
                ...(customerId
                    ? { customer_id: Number(customerId) }
                    : {}),
            };

            const result = await askCopilot(requestData);

            setResponse(result);

        } catch (err) {
            console.error("Copilot API error:", err);

            setError(
                err.message ||
                "Unable to generate an answer. Please check the backend server."
            );

        } finally {
            setLoading(false);
        }
    }

    // Clear question and response
    function handleClear() {
        setQuestion("");
        setResponse(null);
        setError("");
    }

    // Get selected customer name
    function getSelectedCustomerName() {
        const customer = customers.find(
            item => item.customer_id === Number(customerId)
        );

        return customer?.name || "";
    }

    return (
        <section className="copilot-page">

            {/* Page Header */}
            <div className="copilot-heading">
                <div>
                    <div className="eyebrow">
                        ENTERPRISE INTELLIGENCE
                    </div>

                    <h1>AI Copilot</h1>

                    <p>
                        Ask questions about enterprise knowledge and
                        customer interactions using context-aware AI.
                    </p>
                </div>

                <div className="copilot-model-badge">
                    <span className="copilot-status-dot"></span>
                    Local AI · Ollama
                </div>
            </div>

            {/* Copilot Introduction */}
            <div className="copilot-welcome panel">
                <div className="copilot-welcome-icon">
                    <span>✧</span>
                </div>

                <div>
                    <h2>Your Enterprise AI Assistant</h2>

                    <p>
                        Get answers from your enterprise documents
                        and customer records. Responses are generated
                        using retrieved context and your local AI model.
                    </p>
                </div>
            </div>

            {/* Question Form */}
            <div className="panel copilot-query-panel">

                <div className="copilot-section-heading">
                    <div>
                        <h2>Ask a Question</h2>

                        <p>
                            Choose a query type and enter your question.
                        </p>
                    </div>
                </div>

                <form onSubmit={handleAskCopilot}>

                    {/* Query Context */}
                    <label htmlFor="copilot-customer">
                        Query Context
                    </label>

                    <select
                        id="copilot-customer"
                        value={customerId}
                        onChange={event => {
                            setCustomerId(event.target.value);
                            setResponse(null);
                            setError("");
                        }}
                        disabled={customersLoading || loading}
                    >
                        <option value="">
                            General Enterprise Knowledge
                        </option>

                        {customers.map(customer => (
                            <option
                                key={customer.customer_id}
                                value={customer.customer_id}
                            >
                                {customer.name} — {customer.company || customer.email}
                            </option>
                        ))}
                    </select>

                    <p className="copilot-field-hint">
                        Select a customer to include their Customer 360
                        profile, tickets and interactions. Leave unselected
                        for general enterprise questions.
                    </p>

                    {/* Question */}
                    <label htmlFor="copilot-question">
                        Your Question
                    </label>

                    <textarea
                        id="copilot-question"
                        rows="5"
                        placeholder="Example: What are the common causes of payment failures?"
                        value={question}
                        onChange={event => setQuestion(event.target.value)}
                        disabled={loading}
                    />

                    {/* Form Actions */}
                    <div className="copilot-form-footer">

                        <span>
                            {customerId
                                ? `Customer context: ${getSelectedCustomerName()}`
                                : "General knowledge mode"}
                        </span>

                        <div className="copilot-form-actions">

                            <button
                                type="button"
                                className="copilot-clear-button"
                                onClick={handleClear}
                                disabled={loading}
                            >
                                Clear
                            </button>

                            <button
                                type="submit"
                                className="copilot-ask-button"
                                disabled={loading || !question.trim()}
                            >
                                {loading
                                    ? "Thinking..."
                                    : "✧ Ask Copilot"}
                            </button>

                        </div>
                    </div>

                </form>
            </div>

            {/* Error Message */}
            {error && (
                <div className="copilot-error">
                    <span>{error}</span>

                    <button
                        type="button"
                        onClick={() => setError("")}
                    >
                        Dismiss
                    </button>
                </div>
            )}

            {/* Loading State */}
            {loading && (
                <div className="panel copilot-loading">

                    <div className="copilot-loader"></div>

                    <h3>Analyzing your question...</h3>

                    <p>
                        Retrieving enterprise knowledge and preparing
                        a context-aware response.
                    </p>

                </div>
            )}

            {/* AI Response */}
            {response && !loading && (
                <div className="panel copilot-response-panel">

                    <div className="copilot-response-heading">

                        <div>
                            <div className="eyebrow">
                                AI GENERATED RESPONSE
                            </div>

                            <h2>Copilot Answer</h2>
                        </div>

                        <span
                            className={`copilot-knowledge-status ${
                                response.knowledge_status || "unknown"
                            }`}
                        >
                            {(response.knowledge_status || "unknown")
                                .replaceAll("_", " ")}
                        </span>

                    </div>

                    {/* Original Question */}
                    <div className="copilot-question-summary">

                        <small>YOUR QUESTION</small>

                        <p>
                            {response.question || question}
                        </p>

                        {response.customer_id && (
                            <span>
                                Customer ID: {response.customer_id}
                            </span>
                        )}

                    </div>

                    {/* Generated Answer */}
                    <div className="copilot-answer">

                        <h3>
                            <span>✧</span> Answer
                        </h3>

                        <p>
                            {response.answer ||
                                "The Copilot did not return an answer."}
                        </p>

                    </div>

                    {/* Knowledge Sources */}
                    {response.sources?.length > 0 ? (
                        <div className="copilot-sources">

                            <h3>Knowledge Sources</h3>

                            <div className="copilot-source-list">

                                {response.sources.map((source, index) => (
                                    <div
                                        className="copilot-source-item"
                                        key={index}
                                    >
                                        <div className="copilot-source-icon">
                                            <span>PDF</span>
                                        </div>

                                        <div>
                                            <strong>
                                                {source.source ||
                                                    `Source ${source.source_number || index + 1}`}
                                            </strong>

                                            <p>
                                                Page {source.page_number ?? "—"}
                                            </p>
                                        </div>
                                    </div>
                                ))}

                            </div>
                        </div>
                    ) : (
                        <div className="copilot-no-sources">
                            No supporting document sources were returned
                            for this response.
                        </div>
                    )}

                    {/* Disclaimer */}
                    <div className="copilot-disclaimer">
                        AI-generated responses are advisory. Verify
                        important information against the original
                        enterprise records and documentation.
                    </div>

                </div>
            )}

            {/* Empty State */}
            {!response && !loading && !error && (
                <div className="copilot-empty-state">

                    <span>✧</span>

                    <h3>Ready to assist</h3>

                    <p>
                        Your AI-generated answers will appear here.
                        Start by asking a question above.
                    </p>

                </div>
            )}

        </section>
    );
}

export default CopilotPage;
