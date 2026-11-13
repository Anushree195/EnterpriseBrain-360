
import { useEffect, useMemo, useState } from "react";
import {
    getCustomers,
    getCustomerProfile,
    createCustomer,
} from "../services/api";
import "./CustomersPage.css";

function formatDate(value) {
    if (!value) return "—";

    return new Date(value).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

function CustomersPage() {
    const [customers, setCustomers] = useState([]);
    const [selectedCustomer, setSelectedCustomer] = useState(null);
    const [profile, setProfile] = useState(null);

    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);
    const [profileLoading, setProfileLoading] = useState(false);
    const [error, setError] = useState("");

    // Add customer form state
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [creating, setCreating] = useState(false);
    const [createError, setCreateError] = useState("");
    const [createSuccess, setCreateSuccess] = useState("");

    const [formData, setFormData] = useState({
        name: "",
        email: "",
        company: "",
    });

    // Load all customers
    useEffect(() => {
        async function loadCustomers() {
            try {
                setLoading(true);
                setError("");

                const data = await getCustomers();

                setCustomers(data);

                if (data.length > 0) {
                    setSelectedCustomer(data[0]);
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadCustomers();
    }, []);

    // Load complete Customer 360 profile
    useEffect(() => {
        if (!selectedCustomer) {
            setProfile(null);
            return;
        }

        let cancelled = false;

        async function loadProfile() {
            try {
                setProfileLoading(true);
                setProfile(null);
                setError("");

                const data = await getCustomerProfile(
                    selectedCustomer.customer_id
                );

                if (!cancelled) {
                    setProfile(data);
                }
            } catch (err) {
                if (!cancelled) {
                    setError(err.message);
                }
            } finally {
                if (!cancelled) {
                    setProfileLoading(false);
                }
            }
        }

        loadProfile();

        return () => {
            cancelled = true;
        };
    }, [selectedCustomer]);

    // Search customers by name, email or company
    const filteredCustomers = useMemo(() => {
        const query = search.trim().toLowerCase();

        if (!query) return customers;

        return customers.filter((customer) =>
            [
                customer.name,
                customer.email,
                customer.company || "",
            ].some((value) =>
                value.toLowerCase().includes(query)
            )
        );
    }, [customers, search]);

    // Create a new customer
    async function handleCreateCustomer(event) {
        event.preventDefault();

        setCreateError("");
        setCreateSuccess("");

        try {
            setCreating(true);

            const newCustomer = await createCustomer({
                name: formData.name.trim(),
                email: formData.email.trim(),
                company: formData.company.trim() || null,
            });

            // Update the directory
            setCustomers((previous) => [
                ...previous,
                newCustomer,
            ]);

            // Automatically select the new customer
            setSelectedCustomer(newCustomer);

            // Reset form
            setFormData({
                name: "",
                email: "",
                company: "",
            });

            setShowCreateForm(false);
            setCreateSuccess("Customer created successfully!");

        } catch (err) {
            setCreateError(err.message);
        } finally {
            setCreating(false);
        }
    }

    function openCreateForm() {
        setCreateError("");
        setCreateSuccess("");
        setFormData({
            name: "",
            email: "",
            company: "",
        });
        setShowCreateForm(true);
    }

    return (
        <section className="customers-page">

            {/* Page heading */}
            <div className="customers-heading">
                <div>
                    <div className="eyebrow">
                        CUSTOMER INTELLIGENCE
                    </div>

                    <h1>Customers</h1>

                    <p>
                        Manage customer profiles, support tickets and
                        interaction history.
                    </p>
                </div>

                <div className="customers-heading-actions">
                    <div className="customer-count">
                        <span>{customers.length}</span>
                        <small>Total Customers</small>
                    </div>

                    <button
                        className="add-customer-button"
                        onClick={openCreateForm}
                    >
                        + Add Customer
                    </button>
                </div>
            </div>

            {/* Success message */}
            {createSuccess && (
                <div className="customer-success">
                    {createSuccess}
                </div>
            )}

            {/* Add Customer Modal */}
            {showCreateForm && (
                <div className="customer-modal-overlay">
                    <div className="customer-modal">

                        <div className="modal-heading">
                            <div>
                                <h2>Add New Customer</h2>
                                <p>
                                    Create a customer profile in
                                    EnterpriseBrain 360.
                                </p>
                            </div>

                            <button
                                type="button"
                                className="modal-close"
                                onClick={() => setShowCreateForm(false)}
                                aria-label="Close form"
                            >
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleCreateCustomer}>
                            <label htmlFor="customer-name">
                                Customer Name *
                            </label>

                            <input
                                id="customer-name"
                                type="text"
                                required
                                minLength={1}
                                placeholder="Enter customer name"
                                value={formData.name}
                                onChange={(event) =>
                                    setFormData({
                                        ...formData,
                                        name: event.target.value,
                                    })
                                }
                            />

                            <label htmlFor="customer-email">
                                Email Address *
                            </label>

                            <input
                                id="customer-email"
                                type="email"
                                required
                                placeholder="customer@example.com"
                                value={formData.email}
                                onChange={(event) =>
                                    setFormData({
                                        ...formData,
                                        email: event.target.value,
                                    })
                                }
                            />

                            <label htmlFor="customer-company">
                                Company Name
                            </label>

                            <input
                                id="customer-company"
                                type="text"
                                placeholder="Enter company name (optional)"
                                value={formData.company}
                                onChange={(event) =>
                                    setFormData({
                                        ...formData,
                                        company: event.target.value,
                                    })
                                }
                            />

                            {createError && (
                                <div className="customer-form-error">
                                    {createError}
                                </div>
                            )}

                            <div className="modal-actions">
                                <button
                                    type="button"
                                    className="modal-cancel"
                                    onClick={() => setShowCreateForm(false)}
                                    disabled={creating}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="add-customer-button"
                                    disabled={creating}
                                >
                                    {creating
                                        ? "Creating..."
                                        : "Create Customer"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* API error */}
            {error && (
                <div className="customer-error">
                    {error}
                    <button
                        onClick={() => window.location.reload()}
                    >
                        Retry
                    </button>
                </div>
            )}

            <div className="customer-workspace">

                {/* Customer Directory */}
                <div className="customer-directory panel">

                    <div className="directory-header">
                        <div>
                            <h2>Customer Directory</h2>
                            <p>
                                {filteredCustomers.length} customers found
                            </p>
                        </div>
                    </div>

                    <input
                        className="customer-search"
                        type="text"
                        placeholder="Search name, email or company..."
                        value={search}
                        onChange={(event) =>
                            setSearch(event.target.value)
                        }
                    />

                    {loading ? (
                        <div className="customer-message">
                            Loading customers...
                        </div>
                    ) : filteredCustomers.length === 0 ? (
                        <div className="customer-message">
                            {customers.length === 0
                                ? "No customers available yet."
                                : "No customers match your search."}
                        </div>
                    ) : (
                        <div className="customer-list">
                            {filteredCustomers.map((customer) => (
                                <button
                                    key={customer.customer_id}
                                    className={`customer-list-item ${
                                        selectedCustomer?.customer_id ===
                                        customer.customer_id
                                            ? "selected"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setSelectedCustomer(customer)
                                    }
                                >
                                    <div className="customer-avatar">
                                        {customer.name
                                            .charAt(0)
                                            .toUpperCase()}
                                    </div>

                                    <div className="customer-list-info">
                                        <strong>{customer.name}</strong>
                                        <span>{customer.email}</span>
                                        <small>
                                            {customer.company || "No company"}
                                        </small>
                                    </div>

                                    <span className="customer-chevron">
                                        ›
                                    </span>
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* Customer 360 Profile */}
                <div className="customer-details">

                    {!selectedCustomer ? (
                        <div className="panel customer-empty">
                            Select a customer to view their profile.
                        </div>
                    ) : profileLoading ? (
                        <div className="panel customer-empty">
                            Loading customer profile...
                        </div>
                    ) : profile ? (
                        <>

                            {/* Profile Card */}
                            <div className="panel customer-profile-card">
                                <div className="profile-main">
                                    <div className="profile-large-avatar">
                                        {profile.name
                                            .charAt(0)
                                            .toUpperCase()}
                                    </div>

                                    <div>
                                        <div className="eyebrow">
                                            CUSTOMER PROFILE
                                        </div>

                                        <h2>{profile.name}</h2>

                                        <p>{profile.email}</p>

                                        <span className="company-label">
                                            {profile.company || "No company"}
                                        </span>
                                    </div>
                                </div>

                                <div className="profile-meta">
                                    <div>
                                        <small>Customer ID</small>
                                        <strong>
                                            #{profile.customer_id}
                                        </strong>
                                    </div>

                                    <div>
                                        <small>Customer Since</small>
                                        <strong>
                                            {formatDate(profile.created_at)}
                                        </strong>
                                    </div>
                                </div>
                            </div>

                            {/* Customer Statistics */}
                            <div className="customer-stats">
                                <div className="panel customer-stat-card">
                                    <small>Total Tickets</small>
                                    <strong>
                                        {profile.tickets.length}
                                    </strong>
                                </div>

                                <div className="panel customer-stat-card">
                                    <small>Interactions</small>
                                    <strong>
                                        {profile.interactions.length}
                                    </strong>
                                </div>
                            </div>

                            {/* Support Ticket History */}
                            <div className="panel history-panel">
                                <div className="history-heading">
                                    <div>
                                        <h2>Support Ticket History</h2>
                                        <p>
                                            Tickets associated with this customer
                                        </p>
                                    </div>

                                    <span>
                                        {profile.tickets.length}
                                    </span>
                                </div>

                                {profile.tickets.length === 0 ? (
                                    <p className="history-empty">
                                        No support tickets found.
                                    </p>
                                ) : (
                                    <div className="history-list">
                                        {profile.tickets.map((ticket) => (
                                            <div
                                                className="history-item"
                                                key={ticket.ticket_id}
                                            >
                                                <div className="history-item-top">
                                                    <strong>
                                                        {ticket.subject}
                                                    </strong>

                                                    <span
                                                        className={`priority ${ticket.priority}`}
                                                    >
                                                        {ticket.priority}
                                                    </span>
                                                </div>

                                                <p>{ticket.description}</p>

                                                <div className="history-meta">
                                                    <span>
                                                        Ticket #{ticket.ticket_id}
                                                    </span>

                                                    <span>{ticket.status}</span>

                                                    <span>
                                                        {formatDate(ticket.created_at)}
                                                    </span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* Interaction History */}
                            <div className="panel history-panel">
                                <div className="history-heading">
                                    <div>
                                        <h2>Interaction History</h2>
                                        <p>
                                            Customer communication timeline
                                        </p>
                                    </div>

                                    <span>
                                        {profile.interactions.length}
                                    </span>
                                </div>

                                {profile.interactions.length === 0 ? (
                                    <p className="history-empty">
                                        No interactions recorded.
                                    </p>
                                ) : (
                                    <div className="history-list">
                                        {profile.interactions.map(
                                            (interaction) => (
                                                <div
                                                    className="history-item"
                                                    key={interaction.interaction_id}
                                                >
                                                    <div className="history-item-top">
                                                        <strong>
                                                            {interaction.interaction_type.toUpperCase()}
                                                        </strong>

                                                        <small>
                                                            {formatDate(interaction.created_at)}
                                                        </small>
                                                    </div>

                                                    <p>
                                                        {interaction.summary}
                                                    </p>

                                                    {interaction.ticket_id && (
                                                        <span className="interaction-ticket">
                                                            Ticket #{interaction.ticket_id}
                                                        </span>
                                                    )}
                                                </div>
                                            )
                                        )}
                                    </div>
                                )}
                            </div>

                        </>
                    ) : (
                        <div className="panel customer-empty">
                            Customer profile could not be loaded.
                        </div>
                    )}
                </div>
            </div>
        </section>
    );
}

export default CustomersPage;
