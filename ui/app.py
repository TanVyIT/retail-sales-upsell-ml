
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RetailApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Retail Intelligence System")
        self.geometry("1360x800")
        self.minsize(1100, 700)
        self.configure(fg_color="#0B1220")

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#111C2E"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="RETAIL",
            font=("Arial", 28, "bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=25, pady=(30, 0))

        ctk.CTkLabel(
            self.sidebar,
            text="BUSINESS INTELLIGENCE",
            font=("Arial", 10, "bold"),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=27, pady=(0, 35))

        menu_items = [
            "Tổng quan",
            "Phân tích kinh doanh",
            "Chiến lược kinh doanh",
            "Machine Learning"
        ]

        for item in menu_items:
            button = ctk.CTkButton(
                self.sidebar,
                text=item,
                height=45,
                anchor="w",
                fg_color="transparent",
                hover_color="#263B59",
                text_color="#E2E8F0",
                font=("Arial", 13),
                command=lambda name=item: self.change_page(name)
            )
            button.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            self.sidebar,
            text="RETAIL SALES ANALYTICS\nVersion 1.0",
            text_color="#64748B",
            font=("Arial", 10),
            justify="left"
        ).pack(side="bottom", anchor="w", padx=25, pady=25)

    def create_main_content(self):
        self.main_content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#0B1220"
        )
        self.main_content.pack(side="right", fill="both", expand=True)

        self.page_title = ctk.CTkLabel(
            self.main_content,
            text="Tổng quan kinh doanh",
            font=("Arial", 28, "bold"),
            text_color="#F8FAFC"
        )
        self.page_title.pack(anchor="w", padx=35, pady=(35, 5))

        self.page_description = ctk.CTkLabel(
            self.main_content,
            text="Hệ thống phân tích hoạt động kinh doanh chuỗi siêu thị",
            font=("Arial", 13),
            text_color="#94A3B8"
        )
        self.page_description.pack(anchor="w", padx=37, pady=(0, 25))

        self.welcome_panel = ctk.CTkFrame(
            self.main_content,
            fg_color="#142238",
            corner_radius=15,
            height=180
        )
        self.welcome_panel.pack(fill="x", padx=35, pady=10)
        self.welcome_panel.pack_propagate(False)

        ctk.CTkLabel(
            self.welcome_panel,
            text="RETAIL BUSINESS ANALYTICS",
            font=("Arial", 21, "bold"),
            text_color="#60A5FA"
        ).pack(anchor="w", padx=25, pady=(30, 10))

        ctk.CTkLabel(
            self.welcome_panel,
            text="Phân tích dữ liệu bán hàng và hỗ trợ ra quyết định kinh doanh.",
            font=("Arial", 14),
            text_color="#E2E8F0"
        ).pack(anchor="w", padx=25)

    def change_page(self, page_name):
        self.page_title.configure(text=page_name)
        self.page_description.configure(
            text="RETAIL BUSINESS INTELLIGENCE SYSTEM"
        )


if __name__ == "__main__":
    app = RetailApp()
    app.mainloop()
