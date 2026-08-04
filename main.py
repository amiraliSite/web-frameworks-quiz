#ساخته شده توسط امیر علی 

import customtkinter as ctk
import tkinter as tk
import random
import math

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FrameworkQuiz(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔥 Web Frameworks Challenge")
        self.geometry("800x600")
        self.resizable(False, False)

        
        self.questions = [
            {
                "q": "What is the main advantage of React Server Components in Next.js 14?",
                "options": [
                    "Faster client-side routing",
                    "Zero bundle size for server-rendered components",
                    "Automatic CSS-in-JS optimization",
                    "Built-in database ORM integration"
                ],
                "answer": 1
            },
            {
                "q": "In Django, what is the key difference between select_related and prefetch_related?",
                "options": [
                    "select_related uses JOIN, prefetch_related uses separate queries",
                    "prefetch_related is always faster",
                    "select_related works only with ManyToMany fields",
                    "There is no difference, they are aliases"
                ],
                "answer": 0
            },
            {
                "q": "Why does Vue 3 Composition API outperform Options API in large-scale apps?",
                "options": [
                    "It uses Web Workers by default",
                    "Better tree-shaking and logic reuse without mixins",
                    "Automatic virtual DOM diffing optimization",
                    "Built-in state management replacement"
                ],
                "answer": 1
            },
            {
                "q": "FastAPI achieves high performance primarily through which mechanism?",
                "options": [
                    "Multi-threaded request handling",
                    "ASGI + async/await + Pydantic validation via Starlette",
                    "C extensions for route matching",
                    "In-memory caching layer built into the router"
                ],
                "answer": 1
            },
            {
                "q": "What problem does Svelte's compile-time approach solve compared to React/Vue runtime?",
                "options": [
                    "Eliminates the need for a build step",
                    "No virtual DOM overhead, direct DOM updates with minimal runtime",
                    "Automatic SSR without configuration",
                    "TypeScript support without extra tooling"
                ],
                "answer": 1
            }
        ]

        self.current_q = 0
        self.score = 0
        self.time_left = 20
        self.timer_running = False

        
        self.canvas = tk.Canvas(self, width=800, height=600, bg="#0f0f1a", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.particles = []
        for _ in range(80):
            self.particles.append({
                "x": random.randint(0, 800), "y": random.randint(0, 600),
                "r": random.uniform(1, 3),
                "dx": random.uniform(-0.5, 0.5), "dy": random.uniform(-0.5, 0.5),
                "color": random.choice(["#4a9eff", "#7c3aed", "#06b6d4", "#f43f5e"])
            })
        self.animate_bg()

        
        self.quiz_frame = ctk.CTkFrame(
            master=self,
            width=650,
            height=480,
            fg_color="#141423",
            corner_radius=20,
            border_width=1,
            border_color="#333333"
        )
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.quiz_frame.lift()
        self.quiz_frame.pack_propagate(False)

        self.timer_label = ctk.CTkLabel(
            master=self.quiz_frame, text="⏱ 20",
            font=("Arial", 28, "bold"), text_color="#f43f5e"
        )
        self.timer_label.pack(pady=(20, 5))

        self.question_label = ctk.CTkLabel(
            master=self.quiz_frame, text="",
            font=("Segoe UI", 18, "bold"), wraplength=590
        )
        self.question_label.pack(pady=(10, 25))

        self.buttons = []
        for i in range(4):
            btn = ctk.CTkButton(
                master=self.quiz_frame, text="", font=("Segoe UI", 15), height=48,
                fg_color="#1e1e2e", hover_color="#4a9eff",
                border_width=1, border_color="#333333",
                command=lambda idx=i: self.check_answer(idx)
            )
            btn.pack(pady=5, padx=40, fill="x")
            self.buttons.append(btn)

        self.result_label = ctk.CTkLabel(
            master=self.quiz_frame, text="", font=("Segoe UI", 22, "bold")
        )
        self.result_label.pack(pady=20)

        self.load_question()

    def animate_bg(self):
        self.canvas.delete("particle")
        for p in self.particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            if p["x"] < 0 or p["x"] > 800:
                p["dx"] *= -1
            if p["y"] < 0 or p["y"] > 600:
                p["dy"] *= -1
            self.canvas.create_oval(
                p["x"] - p["r"], p["y"] - p["r"],
                p["x"] + p["r"], p["y"] + p["r"],
                fill=p["color"], outline="", tags="particle"
            )
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                dx = self.particles[i]["x"] - self.particles[j]["x"]
                dy = self.particles[i]["y"] - self.particles[j]["y"]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < 100:
                    self.canvas.create_line(
                        self.particles[i]["x"], self.particles[i]["y"],
                        self.particles[j]["x"], self.particles[j]["y"],
                        fill="#4a9eff", width=0.5, tags="particle"
                    )
        self.after(16, self.animate_bg)

    def load_question(self):
        if self.current_q >= len(self.questions):
            self.show_final_result()
            return
        q = self.questions[self.current_q]
        self.question_label.configure(text=f"{self.current_q + 1}. {q['q']}")
        for i, btn in enumerate(self.buttons):
            btn.configure(text=q["options"][i], state="normal", fg_color="#1e1e2e")
        self.result_label.configure(text="")
        self.time_left = 20
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        self.timer_label.configure(text=f"⏱ {self.time_left}")
        self.timer_label.configure(
            text_color="#ff0040" if self.time_left <= 5 else "#f43f5e"
        )
        if self.time_left > 0:
            self.time_left -= 1
            self.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.handle_timeout()

    def check_answer(self, selected_idx):
        if not self.timer_running:
            return
        self.timer_running = False
        correct = self.questions[self.current_q]["answer"]
        if selected_idx == correct:
            self.score += 1
            self.buttons[selected_idx].configure(fg_color="#10b981")
            self.result_label.configure(text="✅ Correct!", text_color="#10b981")
        else:
            self.buttons[selected_idx].configure(fg_color="#ef4444")
            self.buttons[correct].configure(fg_color="#10b981")
            self.result_label.configure(text="❌ Wrong!", text_color="#ef4444")
        self.after(1500, self.next_question)

    def handle_timeout(self):
        correct = self.questions[self.current_q]["answer"]
        self.buttons[correct].configure(fg_color="#10b981")
        self.result_label.configure(text="⏰ Time's up!", text_color="#fbbf24")
        self.after(1500, self.next_question)

    def next_question(self):
        self.current_q += 1
        self.load_question()

    def show_final_result(self):
        self.timer_label.configure(text="")
        self.question_label.configure(text="🎉 Quiz Complete!")
        for btn in self.buttons:
            btn.pack_forget()
        pct = (self.score / len(self.questions)) * 100
        msg = f"Your Score: {self.score}/{len(self.questions)}\n({pct:.0f}%)"
        color = "#10b981" if pct >= 60 else "#ef4444"
        self.result_label.configure(text=msg, text_color=color, font=("Segoe UI", 28, "bold"))


if __name__ == "__main__":
    app = FrameworkQuiz()
    app.mainloop()
