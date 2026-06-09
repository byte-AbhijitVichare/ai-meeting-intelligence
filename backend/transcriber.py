import whisper

model = whisper.load_model("tiny")

result = model.transcribe("meeting.mp3")

print(result["text"])