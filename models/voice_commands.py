class VoiceCommandProcessor:
    def __init__(self):
        self.audio_available = False  # Always false for cloud deployment
        self.demo_commands = [
            "show students above 80",
            "create bar chart for marks", 
            "filter where age greater than 20"
        ]
        self.current_demo_index = 0

    def listen_and_recognize(self):
        """Return demo command for cloud environments."""
        # Cycle through demo commands
        demo_command = self.demo_commands[self.current_demo_index]
        self.current_demo_index = (self.current_demo_index + 1) % len(self.demo_commands)
        return demo_command

    def process_command(self, text: str):
        """Process voice command text and return action dict."""
        text = text.lower()
        import re
        
        if "show students above" in text or "marks above" in text:
            match = re.search(r"above (\d+)", text)
            if match:
                threshold = float(match.group(1))
                return {"action": "filter", "conditions": [("Marks", ">", threshold)], "logic": "AND"}
        elif "create bar chart for" in text:
            match = re.search(r"bar chart for (\w+)", text)
            if match:
                column = match.group(1)
                return {"action": "chart", "column": column}
        elif "filter where" in text and "greater than" in text:
            match = re.search(r"filter where (\w+) greater than (\d+)", text)
            if match:
                column = match.group(1)
                threshold = float(match.group(2))
                return {"action": "filter", "conditions": [(column, ">", threshold)], "logic": "AND"}
        return {"action": "unknown"}

    def get_status_message(self):
        """Get status message about voice command availability."""
        return "📝 Demo Mode: Click to see sample voice commands in action"
