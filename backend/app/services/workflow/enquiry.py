"""
New Enquiry Workflow
"""


class EnquiryWorkflow:

    STEPS = [
        "name",
        "email",
        "phone",
        "service",
        "notes",
        "confirmation"
    ]

    def start(self):

        return {
            "step": "name",
            "message": "Welcome to ITC India. Please enter your full name."
        }

    def next_step(self, current_step):

        if current_step not in self.STEPS:
            return None

        index = self.STEPS.index(current_step)

        if index + 1 >= len(self.STEPS):
            return None

        return self.STEPS[index + 1]