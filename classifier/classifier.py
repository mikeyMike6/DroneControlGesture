import tensorflow as tf
import numpy as np
import os

class Classifier(object):
    def __init__(
            self,
            # do testów, normalnie nie używac pełnej ściezki
            # _model_path=os.path.join(os.getcwd(), 'classifier.tflite'),
            _model_path=r'C:\Users\siwie\Kivy\Lab2\classifier.tflite',
            _num_threads=1):
        # ładowanie modelu tflite
        self.interpreter=tf.lite.Interpreter(model_path=_model_path, num_threads=_num_threads)
        print(self.interpreter)
        # alokacja tensorów
        self.interpreter.allocate_tensors()

        # tensory warstwy wejściowej i wyjściowej
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(self, landmarks):
        input_details_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_index, np.array([landmarks], dtype=np.float32))
        self.interpreter.invoke()

        output_details_index = self.output_details[0]['index']
        result = self.interpreter.get_tensor(output_details_index)

        result_index = np.argmax(np.squeeze(result))
        return result_index

