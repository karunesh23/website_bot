"""
Existing Customer Workflow
"""


class ExistingCustomerWorkflow:

    def start(self):

        return {
            "step": "email",
            "message": (
                "Please enter your registered email "
                "or phone number."
            )
        }

    def ticket_found(self, ticket):

        return {
            "status": ticket.status,
            "ticket": ticket.ticket_number
        }

    def ticket_not_found(self):

        return {
            "message": (
                "No ticket was found. "
                "Would you like to create a new one?"
            )
        }