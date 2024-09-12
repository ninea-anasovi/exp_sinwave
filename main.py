import sys
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel, QPushButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class SinWavePlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initial parameters
        self.amplitude = 1
        self.exp_value = 1
        self.frequency = 1

        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Add a plot canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Add sliders for amplitude, exponent, and frequency
        self.amplitude_slider = self.create_slider(0, 10, self.amplitude * 10, "Amplitude")
        self.exp_slider = self.create_slider(1, 100, self.exp_value * 10, "Exponent")
        self.frequency_slider = self.create_slider(1, 1000, self.frequency * 10, "Frequency")

        layout.addWidget(QLabel("Amplitude"))
        layout.addWidget(self.amplitude_slider)
        layout.addWidget(QLabel("Exponent"))
        layout.addWidget(self.exp_slider)
        layout.addWidget(QLabel("Frequency"))
        layout.addWidget(self.frequency_slider)

        # Add a button to play sound
        self.play_button = QPushButton("Play Sound")
        self.play_button.clicked.connect(self.play_sound)
        layout.addWidget(self.play_button)

        # Initial plot
        self.update_plot()

    def create_slider(self, min_val, max_val, init_val, label):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        slider.valueChanged.connect(self.update_plot)
        return slider

    def update_plot(self):
        # Update parameters from slider values
        self.amplitude = self.amplitude_slider.value() / 10
        self.exp_value = self.exp_slider.value() / 10
        self.frequency = self.frequency_slider.value() / 10

        # Generate the data
        x = np.linspace(0, 10, 1000)
        y = self.amplitude * np.sin(self.frequency * x) * np.exp(-self.exp_value * x)

        # Clear the plot and draw the new sine wave
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title(f"Amplitude: {self.amplitude}, Exponent: {self.exp_value}, Frequency: {self.frequency}")
        self.ax.set_xlabel("ამპლიტუდა")
        self.ax.set_ylabel("სიხშირე")

        # Refresh the canvas
        self.canvas.draw()

    def play_sound(self):
        # Generate sound data for 1 second
        duration = 1  # seconds
        sample_rate = 44100  # samples per second
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        y = self.amplitude * np.sin(2 * np.pi * self.frequency * 100 * t) * np.exp(-self.exp_value * t)

        # Play the sound using sounddevice
        sd.play(y, sample_rate)
        sd.wait()  # Wait until the sound finishes playing


# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SinWavePlotter()
    window.show()
    sys.exit(app.exec_())
