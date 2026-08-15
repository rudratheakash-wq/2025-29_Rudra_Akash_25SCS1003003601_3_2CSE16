
import random
import re
from datetime import datetime


class RuleBasedChatbot:
    """A chatbot that matches user input against a list of regex rules."""

    def __init__(self, name="RuleBot"):
        self.name = name
        self.user_name = None

        # Each rule is a tuple: (regex pattern, list of possible responses)
        # Patterns are checked in order, top to bottom, and the first
        # match wins. {0} in a response gets replaced with a captured
        # group from the regex (e.g. the user's name).
        self.rules = [
            # Greetings
            (r"\b(hi|hello|hey|good morning|good evening)\b",
             ["Hello! How can I help you today?",
              "Hi there! What's on your mind?",
              "Hey! Nice to hear from you."]),

            # Asking the bot's name
            (r"\bwhat('?s| is) your name\b",
             [f"I'm {self.name}, your friendly rule-based chatbot.",
              f"You can call me {self.name}."]),

            # User introduces themselves: "my name is X" / "I am X" / "I'm X"
            (r"\bmy name is (\w+)", "SET_NAME"),
            (r"\bi\s?'?am\s+(\w+)", "SET_NAME"),
            (r"\bi'?m (\w+)", "SET_NAME"),

            # How are you
            (r"\bhow are you\b",
             ["I'm just a program, but I'm running smoothly! How about you?",
              "Doing great, thanks for asking! And you?"]),

            # Asking about the bot's capabilities
            (r"\bwhat can you do\b|\bhelp\b",
             ["I can chat with you, tell you the time/date, tell a joke, "
              "or just talk about how you're feeling. Try saying "
              "'joke', 'time', or 'date'!"]),

            # Time and date
            (r"\btime\b",
             lambda m: f"The current time is {datetime.now().strftime('%H:%M:%S')}."),
            (r"\bdate\b|\btoday'?s date\b",
             lambda m: f"Today's date is {datetime.now().strftime('%B %d, %Y')}."),

            # Feelings
            (r"\bi feel (sad|down|unhappy|depressed)\b",
             ["I'm sorry to hear that. Do you want to talk about it?",
              "That sounds tough. I'm here if you want to talk."]),
            (r"\bi feel (happy|great|good|excited)\b",
             ["That's wonderful to hear!",
              "Awesome! Keep that energy going."]),

            # Jokes
            (r"\bjoke\b",
             ["Why don't scientists trust atoms? Because they make up everything!",
              "I told my computer I needed a break, and it said 'no problem, "
              "I'll go to sleep.'",
              "Why do programmers prefer dark mode? Because light attracts bugs."]),

            # Thanks
            (r"\b(thanks|thank you)\b",
             ["You're welcome!", "Anytime!", "Glad I could help."]),

            # Farewell
            (r"\b(bye|goodbye|exit|quit|see you)\b",
             ["EXIT"]),

            # Yes/No small talk
            (r"^\s*(yes|yeah|yep)\s*$",
             ["Great!", "Good to know."]),
            (r"^\s*(no|nope|nah)\s*$",
             ["Alright, no worries.", "Okay, understood."]),
        ]

        self.fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting! Tell me more.",
            "Hmm, I don't have a rule for that yet. Try asking something else.",
            "Sorry, I didn't quite get that. Can you say it differently?",
        ]

    def _match(self, user_input):
        """Check user_input against all rules and return a response string,
        or the special marker 'EXIT' to end the conversation."""
        text = user_input.lower().strip()

        for pattern, response in self.rules:
            match = re.search(pattern, text)
            if not match:
                continue

            # Special handling: capture and remember the user's name
            if response == "SET_NAME":
                self.user_name = match.group(1).capitalize()
                return f"Nice to meet you, {self.user_name}!"

            # Special handling: dynamic responses (e.g. time/date) via lambda
            if callable(response):
                return response(match)

            # Special handling: exit keyword
            if response == ["EXIT"]:
                return "EXIT"

            # Otherwise pick a random reply from the list of options
            reply = random.choice(response)
            if self.user_name:
                reply = reply.replace("{0}", self.user_name)
            return reply

        return random.choice(self.fallback_responses)

    def get_response(self, user_input):
        if not user_input.strip():
            return "Please type something so I can respond!"
        return self._match(user_input)

    def chat(self):
        """Run an interactive command-line chat loop."""
        print(f"{self.name}: Hi! I'm {self.name}, a rule-based chatbot. "
              f"Type 'bye' to end our chat.\n")

        while True:
            user_input = input("You: ")
            response = self.get_response(user_input)

            if response == "EXIT":
                farewell = f"{self.name}: Goodbye"
                farewell += f", {self.user_name}!" if self.user_name else "!"
                print(farewell)
                break

            print(f"{self.name}: {response}")


if __name__ == "__main__":
    bot = RuleBasedChatbot(name="RuleBot")
    bot.chat()
