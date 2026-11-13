
import { getCustomers } from "./api";

async function testCustomerAPI() {
    try {
        const customers = await getCustomers();

        console.log("Customer API connected successfully!");
        console.log("Customers:", customers);
    } catch (error) {
        console.error("API connection failed:", error.message);
    }
}

testCustomerAPI();
