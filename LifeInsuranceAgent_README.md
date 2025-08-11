# LifeInsuranceAgent – SignalWire Agents SDK Example

## Table of Contents
- [Introduction](#introduction)
- [Functions, Tools, and Capabilities](#functions-tools-and-capabilities)
  - [fetch_policy_info](#fetch_policy_info)
  - [create_caller_profile](#create_caller_profile)
  - [transfer_caller](#transfer_caller)
  - [Example AgentBase Class](#example-agentbase-class)
  - [Example SWMLService Class](#example-swmlservice-class)
- [Environment Variables](#environment-variables)
- [SignalWire Resource Setup Guide](#signalwire-resource-setup-guide)
- [Sample Queries & Responses](#sample-queries--responses)
- [Conclusion](#conclusion)
- [Appendix](#appendix)

---

## Introduction
The **LifeInsuranceAgent** is a conversational AI assistant for the fictional **Hierophant Insurance Incorporated (HII)**, implemented using the **SignalWire Agents SDK for Python**. It operates as a virtual frontline customer service representative (CSR), handling policy inquiries, advisement scheduling, and beneficiary claim escalations with a structured, AI-driven workflow.

This agent leverages:
- **AgentBase** for AI personality and SWAIG function registration.
- **SWMLService** for deterministic telephony call flows.
- **DataMap** for mapping AI function parameters to external API calls and telephony actions.

---

## Functions, Tools, and Capabilities

### fetch_policy_info
Provides access to stored knowledge for life insurance FAQs and policy details.  
**Abbreviated Implementation:**
```python
self.add_skill("datasphere", {
    "space_name": "my-space.signalwire.com",
    "project_id": "12345",
    "token": "my_api_token",
    "document_id": "abcd1234",
    "tool_name": "fetch_policy_info"
})
```
**Implementation Notes:**
- Use `datasphere` for retrieving searchable content.

---

### create_caller_profile
Records a caller’s details for advisement scheduling.  
**Abbreviated Implementation:**
```python
create_caller_profile = (
    DataMap("create_caller_profile")
    .purpose("Create a profile of the caller containing their contact information.")
    .parameter("caller_first_name", "string", "First name given by the caller.")
    .parameter("caller_last_name", "string", "Last name given by the caller.")
    .parameter("caller_phone_number", "string", "Phone number given by the caller.")
    .parameter("caller_policy_interest", "string", "Policy interest of the caller.")
    .webhook("GET", "https://my-server.com/create_caller_profile?...params...")
    .output(SwaigFunctionResult("Returned response: ${message}"))
)
self.register_swaig_function(create_caller_profile.to_swaig_function())
```
**Implementation Notes:**
- Return clear success/failure messages to the caller.

---

### transfer_caller
Escalates the call to a living life insurance agent for processing claims.  
**Abbreviated Implementation:**
```python
transfer_caller = (
    DataMap("transfer_caller")
    .description("Forward the call to a licensed life insurance agent.")
    .parameter("caller_first_name", "string", "First name of caller.", required=True)
    .parameter("insured_last_name", "string", "Last name of insured.", required=True)
    .parameter("insured_policy_type", "string", "Policy type of insured.", required=True)
    .expression(
        test_value="transfer",
        pattern="(?i).*\btransfer\b.*",
        output=SwaigFunctionResult("Call transfer initiated...")
        .add_actions([
            {"say": "Please stand by while I transfer your call."},
            {"SWML": {"sections": {"main": [{"connect": {"parallel": [{"to": "+15551234567"}]}}]}}},
            {"stop": True}
        ])
    )
)
self.register_swaig_function(transfer_caller.to_swaig_function())
```
**Implementation Notes:**
- `expression()` enables matching spoken input to trigger telephony routing.

---

### Example AgentBase Class
**Abbreviated from `LifeInsuranceAgent`:**
```python
class LifeInsuranceAgent(AgentBase):
    def __init__(self):
        super().__init__(name="Jackie", route="/agent", port="0.0.0.0", port=3000, use_pom=True,
                         basic_auth=("user", "pass"))
        self.add_language(name="English", code="en-US", voice="rime.astra", model="arcana")
        self.prompt_add_section("Name and Personality", body="You are Jackie, a CSR for HII.")
        # Register skills and functions...
```
**Implementation Notes:**
- Use `add_language()` to configure voice and model parameters for speech synthesis.
- Define personality and workflow structure in logical prompt sections.

---

### Example SWMLService Class
**Abbreviated from `ConfirmService`:**
```python
class ConfirmService(SWMLService):
    def __init__(self):
        super().__init__(name="confirm", route="/confirm", host="0.0.0.0", port=2000
                         basic_auth=("user", "pass"))
        self.build_confirm_document()

    def build_confirm_document(self):
        self.reset_document()
        self.add_verb("play", {"url": "say:Incoming beneficiary claim call..."})
        self.add_verb("prompt", {"play": "say:Press 1 to accept."})
        self.add_verb("switch", {
            "variable": "prompt_value",
            "case": {
                "1": [{"play": "say:Connecting you now."}]
            },
            "default": [{"play": "say:Goodbye."}, {"hangup": {}}]
        })
```
**Implementation Notes:**
- `prompt` verbs can use speech hints as well as DTMF to improve recognition accuracy.
- `switch` enables branching call logic based on recognized input.
- Always provide fallback actions for unrecognized input.

---

## Environment Variables
```ini
SIGNALWIRE_PROJECT=12345
SIGNALWIRE_TOKEN=my_api_token
SIGNALWIRE_SPACE_NAME=my-space.signalwire.com

AGENT_USERNAME=user
AGENT_PASSWORD=pass
AGENT_PORT=3000

CONFIRM_USERNAME=user
CONFIRM_PASSWORD=pass
CONFIRM_PORT=2000
```
**Implementation Notes:**
- Store credentials in `.env` and load them at runtime.
- Avoid hardcoding sensitive values into source code.

---

## SignalWire Resource Setup Guide
1. Create a SignalWire Space and note the **Project ID**, **Auth Token**, and **Space Name**.
2. Purchase or configure a phone number to handle inbound calls.
3. Set the number’s webhook to `/agent` and `/confirm` routes.
4. Deploy in a Python environment with `signalwire-agents` installed.

**Implementation Notes:**
- Use HTTPS for webhook endpoints to ensure secure communication.
- Configure basic authentication for additional endpoint protection.

**Design Best Practices:**
- Break conversation logic into discrete `prompt_add_section()` calls for maintainability.
- Store business logic in modular SWAIG functions that can be independently tested.
- Use secure authentication for all external API requests.

---

## Sample Queries & Responses
```
User: "Tell me about your life insurance policies."
AI: "We offer Term, Whole, Universal, and Variable Universal policies..."
```
```
User: "I want to schedule an advisement."
AI: "Sure! May I have your first and last name?"
```
**Implementation Notes:**
- Keep responses short and actionable.
- Refrain from asking more than one question at a time to promote clarity.

---

## Conclusion
The **LifeInsuranceAgent** is a pre-production example of a SignalWire AI telephony integration. By combining structured AI prompts, SWAIG-powered tools, and SWML-driven call control, it delivers an efficient and professional customer service experience over the phone.
