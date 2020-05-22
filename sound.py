import numpy as np
import sounddevice as sd
import logging

MME = 0
sd.default.channels = 2
sd.default.dtype = 'int16'
sd.default.latency = 'low'
sd.default.samplerate = 48000

class PCMStream:
    def __init__(self):
        self.stream = None
        
    def read(self, num_bytes):
        # frame is 4 bytes
        frames = int(num_bytes / 4)
        data = self.stream.read(frames)[0]

        # convert to pcm format
        return data.tobytes()

    def change_device(self, num):
        try:
            if (self.stream is not None):
                self.stream.stop()
                self.stream.close()

            self.stream = sd.InputStream(device=num)
            self.stream.start()
            
        except:
            logging.exception('Error on change_device')
            
    def query_devices(self, hard_refresh=False):
        try:
            # portaudio limitation, have to reinit to get hardware changes
            if (hard_refresh):
                if (self.stream is not None):
                    self.stream.stop()
                    self.stream.close()

                sd._terminate()
                sd._initialize()

            options = {}

            for index, item in enumerate(sd.query_devices()):
                # pip version only supports MME api
                if (item.get('max_input_channels') > 0 and item.get('hostapi') == MME):
                    options[item.get('name')] = index

            return options
            
        except:
            logging.exception('Error on query_devices')