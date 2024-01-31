import elevenlabs

audio = elevenlabs.generate(
    text = "Welcome, courageous warrior, to the enchanting medieval realm where your destiny unfolds. Embrace the unknown, shape your character, and decide the path that will define your legend. The kingdom eagerly awaits your noble choice. May your journey be filled with epic tales and legendary feats!",
    voice = "Daniel"
)

elevenlabs.save(audio, "assets/Sound/audio.mp3")