from typing import List, Dict, Callable
import logging
from email_agent import EmailAgent

class AgentAction:
    def __init__(self, name: str, function: Callable, description: str):
        self.name = name
        self.function = function
        self.description = description

class AgentPipeline:
    def __init__(self):
        self.available_actions: Dict[str, AgentAction] = {}
        self.action_history: List[Dict] = []
        self.email_agent = EmailAgent()
        
        # Register actions in init
        self.register_default_actions()
        
    def register_action(self, name: str, function: Callable, description: str):
        """Register a new action the agent can perform"""
        self.available_actions[name] = AgentAction(name, function, description)
        
    def execute_action(self, action_name: str, **kwargs):
        """Execute a registered action"""
        if action_name in self.available_actions:
            action = self.available_actions[action_name]
            try:
                result = action.function(**kwargs)
                self.action_history.append({
                    'action': action_name,
                    'params': kwargs,
                    'success': True,
                    'result': result
                })
                logging.info(f"Action {action_name} executed with result: {result}")
                return result
            except Exception as e:
                logging.error(f"Error executing action {action_name}: {e}")
                self.action_history.append({
                    'action': action_name,
                    'params': kwargs,
                    'success': False,
                    'error': str(e)
                })
                return None
        else:
            logging.error(f"Action {action_name} not found in available actions: {list(self.available_actions.keys())}")
        return None

    def send_email(self, to: str, subject: str, body: str):
        """Send an email using Gmail API"""
        logging.info("Pipeline sending email...")
        return self.email_agent.send_email(to, subject, body)

    def register_default_actions(self):
        """Register the default set of actions"""
        self.register_action(
            "send_email",
            self.send_email,  # Use the instance method directly
            "Send an email to specified recipient"
        )

# Example usage:
def search_web(query: str):
    # Web search logic here
    pass

def control_lights(command: str):
    # Smart home control logic here
    pass

# Initialize pipeline
pipeline = AgentPipeline()

# Register available actions
pipeline.register_action(
    "search_web",
    search_web,
    "Search the web for information"
)

pipeline.register_action(
    "control_lights",
    control_lights,
    "Control smart home lighting"
) 