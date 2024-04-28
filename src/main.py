import argparse
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='People Tracker Application')
    # Define the model argument
    parser.add_argument('--model', type=str, help='Path to the model file', default='models/yolov5s6.pt')
    # Parse arguments
    args = parser.parse_args()

    # Pass the model path to MainWindow
    app = QApplication([])
    window = MainWindow(model_path=args.model)
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
