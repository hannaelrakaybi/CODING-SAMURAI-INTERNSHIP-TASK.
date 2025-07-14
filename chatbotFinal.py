import random # For selecting random response 
import re  # For regular expression pattern matching 

class SupportBot:
    # Define setes of negative responses and exit commands
    negative_res = {'no', 'nope', 'nay', 'not a chance', 'sorry'}
    exit_commands = {'quit', 'pause', 'exit', 'goodbye', 'bye', 'farewell'}

    def __init__(self):
        # Dictionary of regex patterns to match user intents
        self.support_responses = {
            'ask_about_product': r'.*\b(product|item|goods)\b.*', # Matches product-related queries
            'technical_support': r'.*\b(technical|tech|support|help)\b.*', # Matches tech support queries
            'about_returns': r'.*\b(return|refund|exchange|policy)\b.*', # Matches retuen policy queries 
            'general_query': r'.*\b(help|support|question|query)\b.*' # Matches genral help queries 
        }
        # Dictionary of response templates for each intent
        self.responses = {
            'ask_about_product': [
                f"Our products are top-notch with excellent reviews, {{name}}!",
                "You can find all product details on our website at example.com/products."
            ],
            'technical_support': [
                "Please visit our support page at example.com/support for detailed assistance.",
                "For immediate help, call our tech support at 1-800-123-4567."
            ],
            'about_returns': [
                "We offer a 30-day return policy for all products.",
                "Please ensure items are in original condition for returns. More info at example.com/returns."
            ],
            'general_query': [
                "How else can I assist you today, {name}?",
                "Is there anything specific you'd like to know?"
            ],
            'no_match': [
                "I'm sorry {name}, I didn't understand that. Could you rephrase?",
                "My apologies, could you provide more details about your question?"
            ],
            'exit': [
                "Thank you for contacting us, {name}! Have a great day!",
                "We appreciate your time, {name}. Come back anytime!"
            ]
        }
        self.unrecognized_count = 0 # Counter for unrecognized inputs 
        self.max_unrecognized = 3 # Max unrecognized inputs before agent transfer 

    def greet(self):
        # Get user's name and provide initial greeting 
        self.name = input("Hello! Welcome to our customer support. What's your name?\n").strip()
        if not self.name:
            self.name = "Guest" # Default name if none provided
        #Ask if user needs help 
        will_help = input(f"Hi {self.name}, how can I assist you today?\n").strip().lower()
        if will_help in self.negative_res:
            # If user declines help, provide exit message
            print(random.choice(self.responses['exit']).format(name=self.name))
            return
        self.chat() # Start the chat loop

    def make_exit(self, reply):
        # Check if user wants to exit the conversation 
        if any(command in reply for command in self.exit_commands):
            confirm = input("Are you sure you want to exit? (yes/no) ").strip().lower()
            if confirm not in self.negative_res:
                # Confirm exit and provide exit message 
                print(random.choice(self.responses['exit']).format(name=self.name))
                return True
        return False

    def should_continue(self):
        # Ask if user wants to continue getting help 
        reply = input("Would you like help with anything else? (yes/no) ").strip().lower()
        return reply not in self.negative_res # Return True if user wants to continue 

    def chat(self):
        # Main chat loop for handling user queries 
        while True:
            reply = input(f"{self.name}, how can I help you? (or type 'exit' to quit): ").strip().lower()
            
            if not reply:
                print("Please provide a valid query.") # Handle empty input 
                continue
                
            if self.make_exit(reply):
                break # Exit chat if user confirms 
                
            response = self.match_reply(reply) # Get appropriate response 
            print(response)
            
            if not self.should_continue():
                # End chat if user doesn't want more help
                print(random.choice(self.responses['exit']).format(name=self.name))
                break

    def match_reply(self, reply):
        # Match user input to an intent using regex
        for intent, regex_pattern in self.support_responses.items():
            if re.search(regex_pattern, reply, re.IGNORECASE):
                self.unrecognized_count = 0  # Reset counter on recognized input
                return self.format_response(intent)
        # Handle unrecognized input  
        self.unrecognized_count += 1
        if self.unrecognized_count >= self.max_unrecognized:
            return "I'm having trouble understanding. Let me connect you to a live agent..."
        return self.format_response('no_match')

    def format_response(self, intent):
        # Format response with user's name 
        response = random.choice(self.responses[intent])
        return response.format(name=self.name)

if __name__ == "__main__":
    bot = SupportBot() # Create bot instance 
    bot.greet() # Start the bot 
