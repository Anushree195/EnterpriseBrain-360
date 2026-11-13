
import { useEffect, useMemo, useState } from "react";
import {
    getTickets,
    getCustomers,
    createTicket,
    updateTicket,
    deleteTicket,
    analyzeTicket,
} from "../services/api";
import "./TicketsPage.css";

// Format ticket creation date
function formatDate(value) {
    if (!value) return "—";

    return new Date(value).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

// Parse AI-generated resolution into separate sections
function parseResolutionRecommendation(value = "") {
    const text = value.replace(/\r/g, "").trim();

    const sectionPattern =
        /\b(Issue Summary|Recommended Actions|Additional Information)\s*:\s*/gi;

    const matches = [...text.matchAll(sectionPattern)];

    if (matches.length === 0) {
        return {
            summary: "",
            actions: [],
            additional: "",
            fallback: text,
        };
    }

    const sections = {};

    matches.forEach((match, index) => {
        const label = match[1].toLowerCase();
        const contentStart = match.index + match[0].length;

        const contentEnd =
            index + 1 < matches.length
                ? matches[index + 1].index
                : text.length;

        sections[label] = text
            .slice(contentStart, contentEnd)
            .trim();
    });

    const actions = (sections["recommended actions"] || "")
        .split(/(?:^|\s)\d+[.)]\s+/)
        .map(item => item.trim())
        .filter(Boolean);

    return {
        summary: sections["issue summary"] || "",
        actions,
        additional: sections["additional information"] || "",
        fallback: "",
    };
}

function TicketsPage() {
    const [tickets, setTickets] = useState([]);
    const [customers, setCustomers] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const [priorityFilter, setPriorityFilter] = useState("all");

    const [showCreateForm, setShowCreateForm] = useState(false);
    const [creating, setCreating] = useState(false);
    const [createError, setCreateError] = useState("");

    const [formData, setFormData] = useState({
        customer_id: "",
        subject: "",
        description: "",
        status: "open",
        priority: "medium",
    });

    const [analysis, setAnalysis] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [analysisError, setAnalysisError] = useState("");

    const [editingTicket, setEditingTicket] = useState(null);
    const [savingUpdate, setSavingUpdate] = useState(false);

    const [deletingId, setDeletingId] = useState(null);

    // Load tickets and customers
    async function loadData() {
        try {
            setLoading(true);
            setError("");

            const [ticketData, customerData] = await Promise.all([
                getTickets(),
                getCustomers(),
            ]);

            setTickets(ticketData);
            setCustomers(customerData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadData();
    }, []);

    // Ticket statistics
    const stats = useMemo(() => ({
        total: tickets.length,
        open: tickets.filter(t => t.status === "open").length,
        inProgress: tickets.filter(
            t => t.status === "in_progress"
        ).length,
        highPriority: tickets.filter(
            t => t.priority === "high" || t.priority === "urgent"
        ).length,
    }), [tickets]);

    // Search and filters
    const filteredTickets = useMemo(() => {
        const query = search.trim().toLowerCase();

        return tickets.filter(ticket => {
            const customer = customers.find(
                c => c.customer_id === ticket.customer_id
            );

            const matchesSearch = !query || [
                ticket.subject,
                ticket.description,
                customer?.name || "",
                String(ticket.ticket_id),
            ].some(value =>
                String(value).toLowerCase().includes(query)
            );

            const matchesStatus =
                statusFilter === "all" ||
                ticket.status === statusFilter;

            const matchesPriority =
                priorityFilter === "all" ||
                ticket.priority === priorityFilter;

            return matchesSearch && matchesStatus && matchesPriority;
        });
    }, [tickets, customers, search, statusFilter, priorityFilter]);

    // Create ticket
    async function handleCreateTicket(event) {
        event.preventDefault();
        setCreateError("");
        setSuccess("");

        try {
            setCreating(true);

            const newTicket = await createTicket({
                ...formData,
                customer_id: Number(formData.customer_id),
            });

            setTickets(previous => [newTicket, ...previous]);

            setFormData({
                customer_id: "",
                subject: "",
                description: "",
                status: "open",
                priority: "medium",
            });

            setShowCreateForm(false);
            setSuccess("Support ticket created successfully!");
        } catch (err) {
            setCreateError(err.message);
        } finally {
            setCreating(false);
        }
    }

    // Update ticket status or priority
    async function handleUpdateTicket(event) {
        event.preventDefault();

        try {
            setSavingUpdate(true);
            setError("");

            const updated = await updateTicket(
                editingTicket.ticket_id,
                {
                    status: editingTicket.status,
                    priority: editingTicket.priority,
                }
            );

            setTickets(previous =>
                previous.map(ticket =>
                    ticket.ticket_id === updated.ticket_id
                        ? updated
                        : ticket
                )
            );

            setEditingTicket(null);
            setSuccess("Ticket updated successfully!");
        } catch (err) {
            setError(err.message);
        } finally {
            setSavingUpdate(false);
        }
    }

    // Delete ticket
    async function handleDeleteTicket(ticketId) {
        const confirmed = window.confirm(
            `Are you sure you want to delete ticket #${ticketId}?`
        );

        if (!confirmed) return;

        try {
            setDeletingId(ticketId);
            setError("");

            await deleteTicket(ticketId);

            setTickets(previous =>
                previous.filter(ticket =>
                    ticket.ticket_id !== ticketId
                )
            );

            setSuccess("Ticket deleted successfully!");
            setAnalysis(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setDeletingId(null);
        }
    }

    // Run intelligent workflow analysis
    async function handleAnalyzeTicket(ticketId) {
        try {
            setAnalyzing(true);
            setAnalysisError("");
            setAnalysis(null);

            const result = await analyzeTicket(ticketId);

            setAnalysis(result);
        } catch (err) {
            setAnalysisError(err.message);
        } finally {
            setAnalyzing(false);
        }
    }

    // Get customer name
    function getCustomerName(customerId) {
        const customer = customers.find(
            c => c.customer_id === customerId
        );

        return customer?.name || `Customer #${customerId}`;
    }

    return (
        <section className="tickets-page">

            {/* Header */}
            <div className="tickets-heading">
                <div>
                    <div className="eyebrow">SUPPORT OPERATIONS</div>
                    <h1>Support Tickets</h1>
                    <p>
                        Manage customer issues and intelligent support workflows.
                    </p>
                </div>

                <button
                    className="ticket-create-button"
                    onClick={() => {
                        setCreateError("");
                        setShowCreateForm(true);
                    }}
                >
                    + Create Ticket
                </button>
            </div>

            {/* Success message */}
            {success && (
                <div className="ticket-success">
                    {success}
                </div>
            )}

            {/* Error message */}
            {error && (
                <div className="ticket-error">
                    {error}
                    <button onClick={() => setError("")}>
                        Dismiss
                    </button>
                </div>
            )}

            {/* Statistics */}
            <div className="ticket-stats-grid">
                <div className="panel ticket-stat-card">
                    <small>Total Tickets</small>
                    <strong>{stats.total}</strong>
                    <span>All support requests</span>
                </div>

                <div className="panel ticket-stat-card">
                    <small>Open Tickets</small>
                    <strong>{stats.open}</strong>
                    <span>Awaiting resolution</span>
                </div>

                <div className="panel ticket-stat-card">
                    <small>In Progress</small>
                    <strong>{stats.inProgress}</strong>
                    <span>Currently being handled</span>
                </div>

                <div className="panel ticket-stat-card">
                    <small>High / Urgent</small>
                    <strong>{stats.highPriority}</strong>
                    <span>Priority attention required</span>
                </div>
            </div>

            {/* Create Ticket Modal */}
            {showCreateForm && (
                <div className="ticket-modal-overlay">
                    <div className="ticket-modal">
                        <div className="ticket-modal-heading">
                            <div>
                                <h2>Create Support Ticket</h2>
                                <p>Register a new customer issue.</p>
                            </div>

                            <button
                                className="ticket-modal-close"
                                onClick={() => setShowCreateForm(false)}
                                type="button"
                            >
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleCreateTicket}>
                            <label>Customer *</label>

                            <select
                                required
                                value={formData.customer_id}
                                onChange={event =>
                                    setFormData({
                                        ...formData,
                                        customer_id: event.target.value,
                                    })
                                }
                            >
                                <option value="">Select customer</option>

                                {customers.map(customer => (
                                    <option
                                        key={customer.customer_id}
                                        value={customer.customer_id}
                                    >
                                        {customer.name} — {customer.email}
                                    </option>
                                ))}
                            </select>

                            <label>Ticket Subject *</label>

                            <input
                                required
                                minLength={3}
                                maxLength={200}
                                placeholder="Enter ticket subject"
                                value={formData.subject}
                                onChange={event =>
                                    setFormData({
                                        ...formData,
                                        subject: event.target.value,
                                    })
                                }
                            />

                            <label>Description *</label>

                            <textarea
                                required
                                minLength={5}
                                placeholder="Describe the customer issue..."
                                value={formData.description}
                                onChange={event =>
                                    setFormData({
                                        ...formData,
                                        description: event.target.value,
                                    })
                                }
                            />

                            <div className="ticket-form-row">
                                <div>
                                    <label>Priority</label>

                                    <select
                                        value={formData.priority}
                                        onChange={event =>
                                            setFormData({
                                                ...formData,
                                                priority: event.target.value,
                                            })
                                        }
                                    >
                                        <option value="low">Low</option>
                                        <option value="medium">Medium</option>
                                        <option value="high">High</option>
                                        <option value="urgent">Urgent</option>
                                    </select>
                                </div>

                                <div>
                                    <label>Status</label>

                                    <select
                                        value={formData.status}
                                        onChange={event =>
                                            setFormData({
                                                ...formData,
                                                status: event.target.value,
                                            })
                                        }
                                    >
                                        <option value="open">Open</option>
                                        <option value="in_progress">In Progress</option>
                                        <option value="resolved">Resolved</option>
                                        <option value="closed">Closed</option>
                                    </select>
                                </div>
                            </div>

                            {createError && (
                                <div className="ticket-form-error">
                                    {createError}
                                </div>
                            )}

                            <div className="ticket-modal-actions">
                                <button
                                    type="button"
                                    className="ticket-cancel-button"
                                    onClick={() => setShowCreateForm(false)}
                                    disabled={creating}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="ticket-create-button"
                                    disabled={
                                        creating || customers.length === 0
                                    }
                                >
                                    {creating ? "Creating..." : "Create Ticket"}
                                </button>
                            </div>

                            {customers.length === 0 && (
                                <p className="ticket-form-note">
                                    Create a customer before registering a ticket.
                                </p>
                            )}
                        </form>
                    </div>
                </div>
            )}

            {/* Edit Ticket Modal */}
            {editingTicket && (
                <div className="ticket-modal-overlay">
                    <div className="ticket-modal">
                        <div className="ticket-modal-heading">
                            <div>
                                <h2>
                                    Update Ticket #{editingTicket.ticket_id}
                                </h2>
                                <p>{editingTicket.subject}</p>
                            </div>

                            <button
                                className="ticket-modal-close"
                                type="button"
                                onClick={() => setEditingTicket(null)}
                            >
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleUpdateTicket}>
                            <label>Status</label>

                            <select
                                value={editingTicket.status}
                                onChange={event =>
                                    setEditingTicket({
                                        ...editingTicket,
                                        status: event.target.value,
                                    })
                                }
                            >
                                <option value="open">Open</option>
                                <option value="in_progress">In Progress</option>
                                <option value="resolved">Resolved</option>
                                <option value="closed">Closed</option>
                            </select>

                            <label>Priority</label>

                            <select
                                value={editingTicket.priority}
                                onChange={event =>
                                    setEditingTicket({
                                        ...editingTicket,
                                        priority: event.target.value,
                                    })
                                }
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="urgent">Urgent</option>
                            </select>

                            <div className="ticket-modal-actions">
                                <button
                                    type="button"
                                    className="ticket-cancel-button"
                                    onClick={() => setEditingTicket(null)}
                                    disabled={savingUpdate}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="ticket-create-button"
                                    disabled={savingUpdate}
                                >
                                    {savingUpdate
                                        ? "Saving..."
                                        : "Save Changes"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Ticket Directory */}
            <div className="panel ticket-directory">
                <div className="ticket-directory-heading">
                    <div>
                        <h2>Ticket Directory</h2>
                        <p>Support requests retrieved from PostgreSQL</p>
                    </div>

                    <span className="ticket-result-count">
                        {filteredTickets.length} results
                    </span>
                </div>

                {/* Search and filters */}
                <div className="ticket-filters">
                    <input
                        type="text"
                        placeholder="Search ticket, customer or description..."
                        value={search}
                        onChange={event => setSearch(event.target.value)}
                    />

                    <select
                        value={statusFilter}
                        onChange={event => setStatusFilter(event.target.value)}
                    >
                        <option value="all">All Statuses</option>
                        <option value="open">Open</option>
                        <option value="in_progress">In Progress</option>
                        <option value="resolved">Resolved</option>
                        <option value="closed">Closed</option>
                    </select>

                    <select
                        value={priorityFilter}
                        onChange={event => setPriorityFilter(event.target.value)}
                    >
                        <option value="all">All Priorities</option>
                        <option value="urgent">Urgent</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                </div>

                {/* Ticket table */}
                {loading ? (
                    <div className="ticket-empty">
                        Loading support tickets...
                    </div>
                ) : filteredTickets.length === 0 ? (
                    <div className="ticket-empty">
                        No support tickets match your filters.
                    </div>
                ) : (
                    <div className="ticket-table-wrapper">
                        <table className="ticket-table">
                            <thead>
                                <tr>
                                    <th>TICKET</th>
                                    <th>CUSTOMER</th>
                                    <th>SUBJECT</th>
                                    <th>PRIORITY</th>
                                    <th>STATUS</th>
                                    <th>CREATED</th>
                                    <th>ACTIONS</th>
                                </tr>
                            </thead>

                            <tbody>
                                {filteredTickets.map(ticket => (
                                    <tr key={ticket.ticket_id}>
                                        <td className="ticket-number">
                                            #{ticket.ticket_id}
                                        </td>

                                        <td>
                                            {getCustomerName(ticket.customer_id)}
                                        </td>

                                        <td className="ticket-subject">
                                            {ticket.subject}
                                        </td>

                                        <td>
                                            <span className={`priority ${ticket.priority}`}>
                                                {ticket.priority}
                                            </span>
                                        </td>

                                        <td>
                                            <span className={`ticket-status ${ticket.status}`}>
                                                {ticket.status.replace("_", " ")}
                                            </span>
                                        </td>

                                        <td>{formatDate(ticket.created_at)}</td>

                                        <td>
                                            <div className="ticket-actions">
                                                <button
                                                    title="Analyze ticket"
                                                    onClick={() =>
                                                        handleAnalyzeTicket(ticket.ticket_id)
                                                    }
                                                    disabled={analyzing}
                                                >
                                                    AI
                                                </button>

                                                <button
                                                    title="Edit ticket"
                                                    onClick={() =>
                                                        setEditingTicket({ ...ticket })
                                                    }
                                                >
                                                    Edit
                                                </button>

                                                <button
                                                    title="Delete ticket"
                                                    className="delete-ticket-button"
                                                    disabled={
                                                        deletingId === ticket.ticket_id
                                                    }
                                                    onClick={() =>
                                                        handleDeleteTicket(ticket.ticket_id)
                                                    }
                                                >
                                                    {deletingId === ticket.ticket_id
                                                        ? "..."
                                                        : "Delete"}
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* AI Workflow Analysis */}
            <div className="panel ticket-analysis-panel">
                <div className="ticket-directory-heading">
                    <div>
                        <div className="eyebrow">INTELLIGENT WORKFLOWS</div>
                        <h2>AI Ticket Analysis</h2>
                        <p>
                            Classification, priority recommendation and
                            knowledge-grounded resolution suggestions.
                        </p>
                    </div>
                </div>

                {analyzing && (
                    <div className="ticket-empty">
                        Analyzing ticket using the intelligent workflow engine...
                    </div>
                )}

                {analysisError && (
                    <div className="ticket-form-error">
                        {analysisError}
                    </div>
                )}

                {!analysis && !analyzing && !analysisError && (
                    <div className="analysis-placeholder">
                        <span>✧</span>
                        <p>
                            Select the AI button on any ticket to run its analysis.
                        </p>
                    </div>
                )}

                {analysis && (
                    <div className="analysis-results">

                        {/* Analyzed ticket */}
                        <div className="analysis-ticket-header">
                            <div>
                                <small>ANALYZED TICKET</small>

                                <h3>
                                    #{analysis.ticket.ticket_id} —{" "}
                                    {analysis.ticket.subject}
                                </h3>

                                <p>{analysis.ticket.description}</p>
                            </div>

                            <span className="ticket-status">
                                {(analysis.ticket.current_status || "open")
                                    .replace("_", " ")}
                            </span>
                        </div>

                        {/* Classification and priority */}
                        <div className="analysis-result-grid">
                            <div className="analysis-result-card">
                                <small>Classification</small>

                                <strong>
                                    {analysis.classification.category}
                                </strong>

                                <p>
                                    Matched:{" "}
                                    {analysis.classification.matched_keywords.join(", ") ||
                                        "No keyword matches"}
                                </p>
                            </div>

                            <div className="analysis-result-card">
                                <small>Recommended Priority</small>

                                <strong
                                    className={`priority-text ${analysis.priority_recommendation.recommended_priority}`}
                                >
                                    {analysis.priority_recommendation.recommended_priority}
                                </strong>

                                <p>
                                    {analysis.priority_recommendation.reasons.join(", ")}
                                </p>
                            </div>
                        </div>

                        {/* Resolution recommendation */}
                        <div className="resolution-result">
                            <div className="resolution-heading">
                                <h3>Resolution Recommendation</h3>

                                <span
                                    className={`resolution-status ${analysis.resolution_recommendation.status}`}
                                >
                                    {analysis.resolution_recommendation.status
                                        .replaceAll("_", " ")}
                                </span>
                            </div>

                            {(() => {
                                const parsed = parseResolutionRecommendation(
                                    analysis.resolution_recommendation.recommendation
                                );

                                // Fallback for unexpected LLM response format
                                if (parsed.fallback) {
                                    return (
                                        <div className="resolution-content">
                                            <p className="resolution-fallback">
                                                {parsed.fallback}
                                            </p>
                                        </div>
                                    );
                                }

                                return (
                                    <div className="resolution-content">

                                        {/* Issue Summary */}
                                        {parsed.summary && (
                                            <section className="resolution-section">
                                                <h4>Issue Summary</h4>
                                                <p>{parsed.summary}</p>
                                            </section>
                                        )}

                                        {/* Recommended Actions */}
                                        {parsed.actions.length > 0 && (
                                            <section className="resolution-section">
                                                <h4>Recommended Actions</h4>

                                                <ol className="resolution-actions-list">
                                                    {parsed.actions.map((action, index) => (
                                                        <li key={index}>
                                                            {action}
                                                        </li>
                                                    ))}
                                                </ol>
                                            </section>
                                        )}

                                        {/* Additional Information */}
                                        {parsed.additional && (
                                            <section className="resolution-section">
                                                <h4>Additional Information</h4>
                                                <p>{parsed.additional}</p>
                                            </section>
                                        )}
                                    </div>
                                );
                            })()}

                            {/* Knowledge Sources */}
                            {analysis.resolution_recommendation.sources?.length > 0 && (
                                <div className="analysis-sources">
                                    <strong>Knowledge Sources</strong>

                                    {analysis.resolution_recommendation.sources.map(
                                        (source, index) => (
                                            <div key={index}>
                                                Source {source.source_number}:{" "}
                                                {source.source}
                                                {" — Page "}
                                                {source.page_number}
                                            </div>
                                        )
                                    )}
                                </div>
                            )}
                        </div>

                        <p className="analysis-disclaimer">
                            Recommendations are advisory. Review them before
                            taking action on a support ticket.
                        </p>
                    </div>
                )}
            </div>
        </section>
    );
}

export default TicketsPage;
