import speech_recognition as sr

class Model_speech_recognition:
    def __init__(self):
        # obtain audio from the microphone
        self.r = sr.Recognizer()
        

    def partnerSpeechInputRecognition(self):
        with sr.Microphone() as source:
            print("Say something!")
            self.r.adjust_for_ambient_noise(source)
            self.audio = self.r.listen(source)
        result = ''
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            result = self.r.recognize_google(self.audio)
            print("Google Speech Recognition thinks you said " + result)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            result = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            result = "Could not request results from Google Speech Recognition service; {0}".format(e)

        return result

if __name__ == '__main__':
    speechRecognition = Model_speech_recognition()
    speechRecognition.partnerSpeechInputRecognition()
    