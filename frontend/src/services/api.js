
const API_BASE_URL = "http://127.0.0.1:8000";

// Reusable response handler
async function handleResponse(response) {
    const data = response.status === 204
        ? null
        : await response.json();

    if (!response.ok) {
        let message = "Something went wrong while communicating with the server.";

        if (typeof data?.detail === "string") {
            message = data.detail;
        } else if (Array.isArray(data?.detail)) {
            message = data.detail
                .map((error) => {
                    const field = error.loc?.join(".");
                    return `${field ? field + ": " : ""}${error.msg}`;
                })
                .join("; ");
        }

        throw new Error(message);
    }

    return data;
}

// Reusable function for JSON API requests
async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
    });

    return handleResponse(response);
}

// 1. Fetch all customers
export function getCustomers() {
    return apiRequest("/customers/");
}

// 2. Fetch complete Customer 360 profile
export function getCustomerProfile(customerId) {
    return apiRequest(`/customers/${customerId}/profile`);
}

// 3. Create a new customer
export function createCustomer(customerData) {
    return apiRequest("/customers/", {
        method: "POST",
        body: JSON.stringify(customerData),
    });
}

// 4. Fetch all support tickets
export function getTickets() {
    return apiRequest("/tickets/");
}

// 5. Create a support ticket
export function createTicket(ticketData) {
    return apiRequest("/tickets/", {
        method: "POST",
        body: JSON.stringify(ticketData),
    });
}

// 6. Update a support ticket
export function updateTicket(ticketId, ticketData) {
    return apiRequest(`/tickets/${ticketId}`, {
        method: "PUT",
        body: JSON.stringify(ticketData),
    });
}

// 7. Delete a support ticket
export function deleteTicket(ticketId) {
    return apiRequest(`/tickets/${ticketId}`, {
        method: "DELETE",
    });
}

// 8. Analyze a ticket using intelligent workflows
export function analyzeTicket(ticketId) {
    return apiRequest(`/workflows/tickets/${ticketId}/analyze`);
}

// 9. Ask AI Copilot
export function askCopilot(questionData) {
    return apiRequest("/copilot/ask", {
        method: "POST",
        body: JSON.stringify(questionData),
    });
}

// 10. Upload PDF to Enterprise Knowledge Hub
export async function uploadDocument(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/knowledge/upload`, {
        method: "POST",
        body: formData,
    });

    return handleResponse(response);
}

// 11. Search enterprise knowledge
export function searchKnowledge(query, topK = 3) {
    const params = new URLSearchParams({
        query,
        top_k: String(topK),
    });

    return apiRequest(`/knowledge/search?${params.toString()}`);
}

// 12. Ask the Knowledge Hub AI
export function askKnowledge(question, topK = 3) {
    return apiRequest("/knowledge/ask", {
        method: "POST",
        body: JSON.stringify({
            question,
            top_k: topK,
        }),
    });
}

// 13. Fetch Knowledge Hub dashboard statistics
export function getKnowledgeStats() {
    return apiRequest("/knowledge/stats");
}
