from signalwire_agents import AgentBase
from signalwire_agents.core.function_result import SwaigFunctionResult
from signalwire_agents.core.data_map import DataMap
from signalwire_agents.core.swml_service import SWMLService
import threading

class LifeInsuranceAgent(AgentBase):
    def __init__(self):
        super().__init__(
            name="Jackie",
            route="/agent",
            host="0.0.0.0",
            port=8000,
            use_pom=True,
            basic_auth=("username", "password")  # Replace with your credentials
        )

        self.add_language(
            name="English",
            code="en-US",
            voice="rime.astra",
            model="arcana"
        )

        self.prompt_add_section("Name and Personality", body="Your name is Jackie and you are a loquacious frontline Customer Support Representative (CSR) for Hierophant Insurance Incorporated (HII), a nationwide provider of life insurance policies in the United States.")

        self.prompt_add_section("Call Handling",
                                body="As a CSR for HII, your aim is to provide assistance to both new and returning policyholders with their life insurance inquiries, including:",
                                bullets=[
                                    "Policy Overview",
                                    "Advisement Scheduling",
                                    "Beneficiary Claim Processing"
                                ])
        
        self.prompt_add_section("Conversation Flow", body="Follow the outlined workflows in each respective subsection to ensure your conversation with the caller evolves naturally.")                            
        self.prompt_add_subsection(parent_title="Conversation Flow",
                                   title="Greeting",
                                   body="Open the conversation with an affable introduction:",
                                   bullets=[
                                       "Greet the caller.",
                                       "Briefly describe who you are and what your mission is.",
                                       "Present the caller with the Menu."
                                   ])
        self.prompt_add_subsection(parent_title="Conversation Flow",
                                   title="Menu",
                                   body="Present the caller with your Menu of functionalities:",
                                   bullets=[
                                       "Policy Overview: Learn general information about the life insurance policies offered by Hierophant and asnwer Frequently Asked Questions (FAQ).",
                                       "Advisement Scheduling: Minimize your premiums and maximize your policy's Cash Value by planning an advisement session with one of Hierophant's authorized salespeople.",
                                       "Beneficiary Claim Processing: Speak with one of Hierophant's local, licensed life insurance agents to process your Death Benefit claim."
                                   ])
        self.prompt_add_subsection(parent_title="Conversation Flow",
                                   title="Closing",
                                   body="Bring your conversation with the caller to a gracious end:",
                                   bullets=[
                                       "Ask the caller if their life insurance needs have been satisfactorily addressed.",
                                       "If yes: offer a genial farewell, then hang up the call.",
                                       "If no: apologize for the misunderstanding or inconvenience, then return to the Menu."
                                   ])
        
        self.prompt_add_section("Policy Overview",
                                body="Answer frequently asked life insurance questions (FAQ) and provide general information about the major policy types offered by HII.",
                                bullets=[
                                    "Use the `fetch_policy_info` skill.",
                                    "If the caller has a follow-up question, rerun the skill to search for relevant answers."
                                ])
        self.prompt_add_subsection(parent_title="Policy Overview",
                                   title="Guidelines",
                                   body="Adhere to the following guidelines when discussing HII's life insurance policies:",
                                   bullets=[
                                       "Policy Types: Provide the caller with an example of HII's major policy types (e.g., Term, Whole, Universal, and Variable Universal).",
                                       "Success: Offer advisement scheduling or beneficiary claim processing.",
                                       "Failure: Inform the caller and apologize for the inconvenience. Retry the function."
                                   ])
        
        self.prompt_add_section("Advisement Scheduling",
                                body="Record the caller's contact details for a future advisement session with an authorized life insurnace salesperson.",
                                bullets=[
                                    "Ask the caller for their First Name.",
                                    "Ask the caller for their Last Name",
                                    "Ask the caller for their Phone Number.",
                                    "Ask the caller for their preferred Policy Interest.",
                                    "Use the `create_caller_profile` function."
                                ],
                                numbered_bullets=True)
        self.prompt_add_subsection(parent_title="Advisement Scheduling",
                                   title="Guidelines",
                                   body="Adhere to the following guidelines when gathering the caller's contact information:",
                                   bullets=[
                                       "Last Name: Instruct the caller to spell out their Last Name, one character at a time.",
                                       "Phone Number: Advise the caller that their phone number should be 10 digits in length, including the area code.",
                                       "Policy Interest: Provide the caller with an example of HII's major policy types.",
                                       "Validation: Confirm the accuracy of your interpretation by repeating the collected Last Name, Phone Number, and Policy Interest.",
                                       "Formatting: Ensure the Phone Number is expressed in e.164 format, which includes the country code and is prefixed with a plus sign (e.g., +1234567890).",
                                       "Success: Proceed to Closing.",
                                       "Failure: Inform the caller and apologize for the inconvenience. Return to the Menu."
                                   ])
        
        self.prompt_add_section("Beneficiary Claim Processing",
                                body="Escalate the caller's beneficiary claim to a local, licensed life insurance agent for processing.",
                                bullets=[
                                    "Ask the caller for the insured's Last Name.",
                                    "Ask the caller for the claim's Policy Type.",
                                    "Use the `transfer_caller` function to forward the phone call."
                                ])
        self.prompt_add_subsection(parent_title="Beneficiary Claim Processing",
                                   title="Guidelines",
                                   body="Adhere to the following guidelines when gathering the caller's claim details:",
                                   bullets=[
                                       "Last Name: Instruct the caller to spell out the insured's Last Name, one character at a time.",
                                       "Policy Type: Provide the caller with an example of HII's major policy types.",
                                       "Validation: Confirm the accuracy of your interpretation by repeating the collected Last Name and Policy Type."
                                       "Success: Proceed to Closing.",
                                       "Failure: Inform the caller that all available agents are busy at this time. Return to the Menu."
                                   ])
        
        self.set_post_prompt("""
                             Analyze the conversation and extract:
                             1. Main topics discussed.
                             2. Action items or follow-ups needed.
                             3. Whether the user's questions were answered satisfactorily.
                             """)
        self.set_post_prompt_url("https://<YOUR-WEBHOOK>")
        
        # Basic single instance
        self.add_skill("datasphere", {
                        "space_name": "<YOUR-SPACE-NAME>",
                        "project_id": "<YOUR-PROJECT-ID>",
                        "token": "<YOUR-API-TOKEN>",
                        "document_id": "<YOUR-DOCUMENT-ID>",
                        "tool_name": "fetch_policy_info"
                        })
        
        create_caller_profile = (DataMap('create_caller_profile')
            .purpose('Create a profile of the caller containing their contact information.')
            .parameter('caller_first_name', 'string', 'The First Name given by the caller.')
            .parameter('caller_last_name', 'string', 'The Last Name given by the caller.')
            .parameter('caller_phone_number', 'number', 'The Phone Number given by the caller.')
            .parameter('caller_policy_interest', 'string', 'The Policy Interest the caller wishes to explore quoting.')
            .webhook('GET', 'https://<YOUR-SERVER>/create_caller_profile?caller_first_name=${enc:args.caller_first_name}&caller_last_name=${enc:args.caller_last_name}&caller_phone_number=${enc:args.caller_phone_number}&caller_policy_interest=${lc:enc:args.caller_policy_interest}')
            .body({'filters': {'active': False}})
            .output(SwaigFunctionResult('Returned response: ${message}')
                    .update_global_data(
                        {'caller_first_name': '${caller_first_name}', 'caller_policy_interest': '${caller_policy_interest}'}
                    ))
            .error_keys(['error'])
        )
        # Register with agent
        self.register_swaig_function(create_caller_profile.to_swaig_function())
        
        transfer_caller = (DataMap('transfer_caller')
            .description('Forward the call to a local, licensed life insurance agent.')
            .parameter('caller_first_name', 'string', 'The First Name given by the caller.', required=True)
            .parameter('insured_last_name', 'string', 'The Last Name of the insured.', required=True)
            .parameter('insured_policy_type', 'string', 'The Policy Type of the insured.', required=True)
            .expression(
                test_value='transfer',
                pattern='(?i).*\\btransfer\\b.*',
                output=(
                    SwaigFunctionResult("Call transfer initiated...")
                    .toggle_functions([
                        {"name": "create_caller_profile", "enabled": True}
                    ])
                    .add_actions([
                        {"say": "Please stand by while I transfer your call."},
                        {
                            "SWML": {
                                "sections": {
                                    "main": [
                                        {
                                            "connect": {
                                                "headers": [
                                                    {
                                                        "name": "x-CALLER_FIRST_NAME",
                                                        "value": "${args.caller_first_name}"
                                                    },
                                                    {
                                                        "name": "x-INSURED_LAST_NAME",
                                                        "value": "${args.insured_last_name}"
                                                    },
                                                    {
                                                        "name": "x-INSURED_POLICY_TYPE",
                                                        "value": "${args.insured_policy_type}"
                                                    }
                                                ],
                                                "confirm": "https://username:password@<YOUR-SERVER>/confirm",
                                                "parallel": [
                                                    {"to": "<YOUR-PSTN-NUMBER>"},
                                                    {"to": "sip:<YOUR-SIP-ADDRESS>.sip.signalwire.com"}
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "stop": True
                        }
                    ])
                )
            )
        )
        self.register_swaig_function(transfer_caller.to_swaig_function())

class ConfirmService(SWMLService):
    def __init__(self, host="0.0.0.0", port=2000):
        super().__init__(
            name="confirm",
            route="/confirm",
            host=host,
            port=port,
            basic_auth=("username", "password")  # Replace with your credentials
        )
        
        # Build the SWML document
        self.build_voicemail_document()
    
    def build_voicemail_document(self):
        """Build the voicemail SWML document"""
        # Reset the document
        self.reset_document()
        
        # Add play verb for greeting
        self.add_verb("play", {
            "url": "say:Hi, you are receiving a call from Hierophant Insurance Incorporated's automated Beneficiary Claim Processing service. The beneficiary, ${call.headers[1]['value']}, is interested in submitting a ${call.headers[3]['value']} life insurance claim for policyholder ${call.headers[2]['value']}."
        })
        
        # Prompt the caller to accept the incoming call
        self.add_verb("prompt", {
            "play": "say:If you wish to speak with the caller, please say the words CONNECT or YES aloud. To decline the call, feel free to hang up after this message.",
            "speech_hints": ["connect", "yes"]
        })
        
        # React to the caller’s response
        self.add_verb("switch", {
            "variable": "prompt_value",
            "default": [
                {
                    "play": "say:You have chosen to decline the call. Goodbye!",
                },
                {
                    "hangup": {}
                }
            ],
            "case": {
                "connect": [
                    {
                        "play": "say:You have chosen to accpet the call. Patching you through to the caller now."
                    }
                ],
                "yes": [
                    {
                        "play": "say:You have chosen to accept the call. Patching you through to the caller now."
                    }
                ]
            }
        })
        
        self.log.debug("confirm_document_built")

def main():
    agent = LifeInsuranceAgent()
    confirm_service = ConfirmService()

    # Start LifeInsuranceAgent in a separate thread
    agent_thread = threading.Thread(target=agent.run)
    agent_thread.start()
    print("LifeInsuranceAgent started.")

    # Start ConfirmService in a separate thread
    voicemail_thread = threading.Thread(target=confirm_service.serve)
    voicemail_thread.start()
    print("ConfirmService started.")

    # Optional: Join threads if you want the main thread to wait for them
    agent_thread.join()
    voicemail_thread.join()
    print("Both services are running.")

if __name__ == "__main__":
    main() 
