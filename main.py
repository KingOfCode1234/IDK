import multiprocessing
import wave
import pyaudio

print("Importing DONE")

class Music:
    def __init__(self):
        self.music_list_LOAD = ["Plateau.wav", "compiled.wav"]
        self.LOAD_next = iter(self.music_list_LOAD)
        self.Process_Music = None
        self.current_audio = ""
        self.p = None

    def stop(self):
        if self.Process_Music is not None:
            self.Process_Music.terminate()
            self.Process_Music = None
            if self.p is not None:
                self.p.terminate()
                self.p = None

    def next(self, next_audio):
        self.stop()
        self.current_audio = next_audio
        self.Process_Music = multiprocessing.Process(target=self.play_process, name="Music")
        self.Process_Music.start()
              
    def get_from_directory(self, directory):
        import os
        for root, dirs, files in os.walk('music', topdown=True):
            self.music_list_LOAD.append(files)
            
        
    def play(self):
        self.p = pyaudio.PyAudio()
        wf = wave.open(self.current_audio, 'rb')
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        wf.close()
        stream.stop_stream()
        stream.close()

    def _play_process(self):
        self.play()

    def start(self):
        self.current_audio = next(self.LOAD_next)
        self.Process_Music = multiprocessing.Process(target=self._play_process, name="Music")
        self.Process_Music.start()
        print(self.current_audio)
        
        while self.Process_Music is not None and self.Process_Music.is_alive():
            user = input("Say stop to quit:")
            if "stop" == user:
                self.stop()
                break
            if "next" == user:
                self.next(next(self.LOAD_next))
