import speech_recognition
#### V1 - fonksiyon
def speech_tr():
    mic = speech_recognition.Microphone()
    kayit = speech_recognition.Recognizer()

    with mic as audio_file:
        kayit.adjust_for_ambient_noise(audio_file)
        audio = kayit.listen(audio_file)
        try:
            return kayit.recognize_google(audio, language="tr-TR")
        except: #speech_recognition.UnknownValueError
            return "Anlaşılamadı. Lütfen tekrar deneyin."
    

#### V3 - fonksiyon(ingilizce)
def speech_en():
    mic = speech_recognition.Microphone()
    kayit = speech_recognition.Recognizer()

    with mic as audio_file:

        kayit.adjust_for_ambient_noise(audio_file)
        audio = kayit.listen(audio_file)
        try:
            return kayit.recognize_google(audio, language="en-GB")
        except: #speech_recognition.UnknownValueError
            return "Anlaşılamadı. Lütfen tekrar deneyin."
    
    
if __name__ =="__main__":
    print("Lütfen konuşun")
    a = speech_tr()
    print(a)
