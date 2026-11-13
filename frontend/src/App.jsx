
import { useEffect, useState } from "react";
import "./App.css";

import CustomersPage from "./pages/CustomersPage";
import TicketsPage from "./pages/TicketsPage";
import CopilotPage from "./pages/CopilotPage";
import KnowledgeHubPage from "./pages/KnowledgeHubPage";

import {
    getCustomers,
    getTickets,
    getKnowledgeStats
} from "./services/api";


const navigation = [
    { id: "overview", icon: "◫", label: "Overview" },
    { id: "customers", icon: "♙", label: "Customers" },
    { id: "tickets", icon: "▤", label: "Support Tickets" },
    { id: "copilot", icon: "✧", label: "AI Copilot" },
    { id: "knowledge", icon: "▧", label: "Knowledge Hub" },
];


function App() {
    const [activePage, setActivePage] = useState("overview");

    const activeNavigation = navigation.find(
        (item) => item.id === activePage
    );

    return (
        <div className="app-shell">

            {/* Sidebar */}
            <aside className="sidebar">

                <div className="brand">
                    <div className="brand-mark">E</div>

                    <div>
                        <h2>EnterpriseBrain</h2>
                        <span>360 Intelligence</span>
                    </div>
                </div>

                <div className="workspace-label">WORKSPACE</div>

                <nav className="navigation">
                    {navigation.map((item) => (
                        <button
                            key={item.id}
                            className={`nav-item ${
                                activePage === item.id ? "active" : ""
                            }`}
                            onClick={() => setActivePage(item.id)}
                        >
                            <span className="nav-icon">{item.icon}</span>
                            <span>{item.label}</span>

                            {item.id === "copilot" && (
                                <span className="new-label">AI</span>
                            )}
                        </button>
                    ))}
                </nav>

                <div className="sidebar-bottom">

                    <div className="system-status">
                        <span className="status-dot"></span>
                        Backend connected
                    </div>

                    <div className="profile">
                        <div className="avatar">A</div>

                        <div>
                            <strong>Admin User</strong>
                            <span>Support Workspace</span>
                        </div>

                        <span className="profile-menu">•••</span>
                    </div>

                </div>
            </aside>


            {/* Main content */}
            <main className="main-content">

                {/* Top navigation */}
                <header className="topbar">

                    <div className="breadcrumb">
                        <span>Workspace</span>
                        <span className="breadcrumb-divider">/</span>
                        <strong>{activeNavigation?.label}</strong>
                    </div>

                    <div className="topbar-right">

                        <span className="environment-label">LIVE DATA</span>

                        <button
                            className="icon-button"
                            aria-label="Notifications"
                        >
                            ♧
                        </button>

                        <div className="top-avatar">A</div>

                    </div>
                </header>


                {/* Page routing */}
                <div className="page-container">

                    {activePage === "overview" ? (
                        <OverviewPage onNavigate={setActivePage} />
                    ) : activePage === "customers" ? (
                        <CustomersPage />
                    ) : activePage === "tickets" ? (
                        <TicketsPage />
                    ) : activePage === "copilot" ? (
                        <CopilotPage />
                    ) : activePage === "knowledge" ? (
                        <KnowledgeHubPage />
                    ) : (
                        <PlaceholderPage
                            title={activeNavigation?.label}
                            onBack={() => setActivePage("overview")}
                        />
                    )}

                </div>

            </main>
        </div>
    );
}


/* --------------------------------------------------
   OVERVIEW DASHBOARD
-------------------------------------------------- */

function OverviewPage({ onNavigate }) {

    const [customers, setCustomers] = useState([]);
    const [tickets, setTickets] = useState([]);

    const [knowledgeStats, setKnowledgeStats] = useState({
        total_documents: 0,
        total_chunks: 0
    });

    const [loading, setLoading] = useState(true);
    const [errors, setErrors] = useState([]);

    useEffect(() => {
        let isMounted = true;

        async function loadDashboard() {

            setLoading(true);

            const results = await Promise.allSettled([
                getCustomers(),
                getTickets(),
                getKnowledgeStats()
            ]);

            if (!isMounted) return;

            const failedRequests = [];

            // Customers API
            if (results[0].status === "fulfilled") {

                const data = results[0].value;

                setCustomers(
                    Array.isArray(data)
                        ? data
                        : data?.customers || []
                );

            } else {
                failedRequests.push("Customers");
                console.error("Customers API failed:", results[0].reason);
            }


            // Tickets API
            if (results[1].status === "fulfilled") {

                const data = results[1].value;

                setTickets(
                    Array.isArray(data)
                        ? data
                        : data?.tickets || []
                );

            } else {
                failedRequests.push("Tickets");
                console.error("Tickets API failed:", results[1].reason);
            }


            // Knowledge Hub statistics API
            if (results[2].status === "fulfilled") {

                setKnowledgeStats(results[2].value);

            } else {
                failedRequests.push("Knowledge Hub");
                console.error("Knowledge Stats API failed:", results[2].reason);
            }

            setErrors(failedRequests);
            setLoading(false);
        }

        loadDashboard();

        return () => {
            isMounted = false;
        };

    }, []);


    // Map customer IDs to customer names
    const customerMap = {};

    customers.forEach((customer) => {
        customerMap[customer.customer_id] = customer.name;
    });


    // Count open and in-progress tickets
    const openTickets = tickets.filter((ticket) =>
        ["open", "in_progress"].includes(
            (ticket.status || "").toLowerCase()
        )
    ).length;


    // Count high and urgent priority tickets
    const highPriorityTickets = tickets.filter((ticket) =>
        ["high", "urgent"].includes(
            (ticket.priority || "").toLowerCase()
        )
    ).length;


    // Sort tickets by latest ticket ID
    const recentTickets = [...tickets]
        .sort((a, b) =>
            Number(b.ticket_id || 0) - Number(a.ticket_id || 0)
        )
        .slice(0, 5);


    // Format ticket ID
    function formatTicketId(id) {
        return `#TKT-${String(id).padStart(3, "0")}`;
    }


    // Format status and priority labels
    function formatLabel(value) {

        if (!value) return "—";

        return value
            .replaceAll("_", " ")
            .replace(/\b\w/g, (letter) => letter.toUpperCase());
    }


    return (
        <>

            {/* Welcome Section */}
            <section className="welcome-section">

                <div>
                    <div className="eyebrow">
                        ENTERPRISE CUSTOMER INTELLIGENCE
                    </div>

                    <h1>
                        Good afternoon, Admin <span>✦</span>
                    </h1>

                    <p>
                        Here's what's happening across your customer support workspace.
                    </p>
                </div>

                <button
                    className="primary-button"
                    onClick={() => onNavigate("tickets")}
                >
                    <span>＋</span> View support tickets
                </button>

            </section>


            {/* Dashboard Connection Status */}
            <div className="demo-notice">
                <span>ⓘ</span>

                {loading
                    ? "Loading live workspace data..."
                    : errors.length === 0
                        ? "Live dashboard — connected to PostgreSQL and ChromaDB."
                        : `Some dashboard data could not be loaded: ${errors.join(", ")}.`
                }
            </div>


            {/* Dashboard Metrics */}
            <section className="metrics-grid">

                <MetricCard
                    label="Total Customers"
                    value={loading ? "..." : customers.length}
                    detail="Registered customers"
                    icon="♙"
                    accent="blue"
                />

                <MetricCard
                    label="Open Tickets"
                    value={loading ? "..." : openTickets}
                    detail="Open and in-progress tickets"
                    icon="▤"
                    accent="purple"
                />

                <MetricCard
                    label="High Priority"
                    value={loading ? "..." : highPriorityTickets}
                    detail="High and urgent tickets"
                    icon="↗"
                    accent="orange"
                />

                <MetricCard
                    label="Knowledge Documents"
                    value={
                        loading
                            ? "..."
                            : knowledgeStats.total_documents ?? 0
                    }
                    detail={`${knowledgeStats.total_chunks ?? 0} indexed chunks`}
                    icon="▧"
                    accent="green"
                />

            </section>


            {/* Recent Tickets and Copilot */}
            <section className="content-grid">

                <div className="panel tickets-panel">

                    <div className="panel-header">

                        <div>
                            <h2>Recent Support Tickets</h2>
                            <p>Latest tickets from your database</p>
                        </div>

                        <button
                            className="text-button"
                            onClick={() => onNavigate("tickets")}
                        >
                            View all →
                        </button>

                    </div>


                    <div className="table-wrapper">

                        <table>

                            <thead>
                                <tr>
                                    <th>TICKET</th>
                                    <th>CUSTOMER</th>
                                    <th>SUBJECT</th>
                                    <th>PRIORITY</th>
                                    <th>STATUS</th>
                                </tr>
                            </thead>


                            <tbody>

                                {loading ? (

                                    <tr>
                                        <td colSpan="5">
                                            Loading support tickets...
                                        </td>
                                    </tr>

                                ) : recentTickets.length === 0 ? (

                                    <tr>
                                        <td colSpan="5">
                                            No support tickets found.
                                        </td>
                                    </tr>

                                ) : (

                                    recentTickets.map((ticket) => (

                                        <tr key={ticket.ticket_id}>

                                            <td className="ticket-id">
                                                {formatTicketId(ticket.ticket_id)}
                                            </td>

                                            <td>
                                                {customerMap[ticket.customer_id]
                                                    || `Customer #${ticket.customer_id}`}
                                            </td>

                                            <td>{ticket.subject}</td>

                                            <td>
                                                <span
                                                    className={`priority ${
                                                        (ticket.priority || "medium").toLowerCase()
                                                    }`}
                                                >
                                                    {formatLabel(ticket.priority)}
                                                </span>
                                            </td>

                                            <td>
                                                <span
                                                    className={`ticket-status ${
                                                        (ticket.status || "open")
                                                            .toLowerCase()
                                                            .replaceAll("_", "-")
                                                    }`}
                                                >
                                                    {formatLabel(ticket.status)}
                                                </span>
                                            </td>

                                        </tr>

                                    ))

                                )}

                            </tbody>

                        </table>

                    </div>


                    <div className="table-footer">

                        <span>
                            Showing {loading ? "..." : recentTickets.length} recent tickets
                        </span>

                        <button
                            className="text-button"
                            onClick={() => onNavigate("tickets")}
                        >
                            Explore tickets →
                        </button>

                    </div>

                </div>


                {/* AI Copilot Panel */}
                <div className="panel copilot-panel">

                    <div className="copilot-heading">

                        <div className="copilot-icon">✧</div>

                        <div>
                            <h2>AI Copilot</h2>
                            <p>Enterprise intelligence assistant</p>
                        </div>

                    </div>


                    <div className="copilot-message">

                        <span className="message-sparkle">✦</span>

                        <h3>Your enterprise knowledge, connected.</h3>

                        <p>
                            Ask questions about customers, support tickets and your
                            enterprise documentation.
                        </p>

                    </div>


                    <button
                        className="copilot-button"
                        onClick={() => onNavigate("copilot")}
                    >
                        Open AI Copilot <span>→</span>
                    </button>

                </div>

            </section>


            {/* Workflows and Architecture */}
            <section className="bottom-grid">

                <div className="panel insight-panel">

                    <div className="panel-header">

                        <div>
                            <h2>Intelligent Workflows</h2>
                            <p>Capabilities implemented in the backend</p>
                        </div>

                        <span className="live-tag">ENGINE READY</span>

                    </div>


                    <div className="workflow-list">

                        <WorkflowItem
                            icon="◎"
                            title="Ticket Classification"
                            description="Payment, Billing, Account, Technical and General"
                        />

                        <WorkflowItem
                            icon="↗"
                            title="Priority Recommendation"
                            description="Urgent, High, Medium and Low"
                        />

                        <WorkflowItem
                            icon="✧"
                            title="Resolution Recommendation"
                            description="Evidence-based suggestions using enterprise knowledge"
                        />

                    </div>

                </div>


                <div className="panel architecture-panel">

                    <div className="panel-header">

                        <div>
                            <h2>Platform Architecture</h2>
                            <p>Core technology stack</p>
                        </div>

                    </div>


                    <div className="technology-tags">

                        {[
                            "React",
                            "FastAPI",
                            "PostgreSQL",
                            "ChromaDB",
                            "Ollama",
                            "Python"
                        ].map((technology) => (

                            <span key={technology}>
                                {technology}
                            </span>

                        ))}

                    </div>


                    <div className="architecture-note">
                        <span className="status-dot"></span>
                        Local-first AI architecture
                    </div>

                </div>

            </section>


            {/* Footer */}
            <footer className="footer">

                <span>EnterpriseBrain 360</span>

                <span>
                    AI-Powered Enterprise Knowledge & Customer Intelligence Platform
                </span>

            </footer>

        </>
    );
}


/* --------------------------------------------------
   METRIC CARD
-------------------------------------------------- */

function MetricCard({ label, value, detail, icon, accent }) {

    return (

        <div className="metric-card">

            <div className="metric-top">

                <span>{label}</span>

                <div className={`metric-icon ${accent}`}>
                    {icon}
                </div>

            </div>

            <h2>{value}</h2>

            <p>{detail}</p>

        </div>

    );
}


/* --------------------------------------------------
   WORKFLOW ITEM
-------------------------------------------------- */

function WorkflowItem({ icon, title, description }) {

    return (

        <div className="workflow-item">

            <div className="workflow-icon">{icon}</div>

            <div>
                <strong>{title}</strong>
                <p>{description}</p>
            </div>

            <span className="workflow-check">✓</span>

        </div>

    );

}


/* --------------------------------------------------
   PLACEHOLDER PAGE
-------------------------------------------------- */

function PlaceholderPage({ title, onBack }) {

    return (

        <div className="placeholder-page">

            <div className="eyebrow">ENTERPRISEBRAIN 360</div>

            <h1>{title}</h1>

            <p>
                This workspace will be implemented and connected to the FastAPI
                backend in the upcoming frontend stages.
            </p>

            <button
                className="primary-button"
                onClick={onBack}
            >
                ← Back to overview
            </button>

        </div>

    );

}


export default App;
