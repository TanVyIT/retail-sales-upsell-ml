import sys
import os

# Đảm bảo Python nhận diện được thư mục src và ui
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()