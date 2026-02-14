import speech_recognition as sr

class VoiceCommandProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_available = self._check_audio_availability()

    def _check_audio_availability(self):
        """Check if audio recording is available in the environment."""
        try:
            import sounddevice
            import pyaudio
            return True
        except ImportError:
            return False

    def listen_and_recognize(self):
        """Record audio and recognize speech if available, otherwise return demo text."""
        if not self.audio_available:
            # Return demo command for cloud environments
            return "show students above 80"
        
        try:
            import sounddevice as sd
            import numpy as np
            from scipy.io.wavfile import write
            
            # Record audio
            fs = 44100  # Sample rate
            seconds = 5  # Duration of recording
            print("Listening... (Speak now)")
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished
            
            # Save to WAV file
            write('output.wav', fs, recording)
            
            # Recognize speech
            with sr.AudioFile('output.wav') as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
                
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return "show students above 80"  # Fallback demo command

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
            # More flexible parsing for filter commands
            match = re.search(r"filter where (\w+) greater than (\d+)", text)
            if match:
                column = match.group(1)
                threshold = float(match.group(2))
                return {"action": "filter", "conditions": [(column, ">", threshold)], "logic": "AND"}
        return {"action": "unknown"}

    def get_status_message(self):
        """Get status message about voice command availability."""
        if self.audio_available:
            return "🎤 Voice commands available - Click and speak your command"
        else:
            return "📝 Voice commands unavailable in cloud environment - Demo mode activated"
