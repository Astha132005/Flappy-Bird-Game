
# 🐦 Flappy Bird Clone - Python (Pygame)

A fully functional **Flappy Bird** clone developed using **Python** with `pygame`, `random`, `sys`, `os`, and `enum`. This game includes custom graphics, sound effects, dynamic obstacles, score tracking, and high score saving — all packed in a responsive game loop.

---

## 🎮 Game Highlights

- Smooth **gravity-based physics** and bird animations
- **Randomized pipes** with adaptive difficulty
- Responsive **controls with sound effects**
- State-driven game flow using Python’s `Enum`
- **Score tracking** and persistent **high score** system
- Retro-inspired **pixel-style graphics** (customizable)
- Three clean states: **Menu**, **Playing**, **Game Over**

---

## 🛠️ Technologies Used

- `pygame` – graphics, audio, event handling
- `random` – for pipe positioning
- `enum.Enum` – to manage game states
- `os`, `sys` – system interaction and exiting

---

## 📁 Folder Structure

```

flappy-bird/
│
├── assets/
│   ├── bird.png
│   ├── pipe.png
│   ├── background.png
│   ├── flap.wav
│   ├── hit.wav
│   └── point.wav
│
├── high\_score.txt         # Auto-created after first run
├── flappy\_bird.py         # Main game script
└── README.md

````

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/flappy-bird-python.git
cd flappy-bird-python
````

### 2️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install pygame
```

> 🔎 Check if pygame is installed successfully:

```bash
python -m pygame.examples.aliens
```

---

## ▶️ Running the Game

Run the main script:

```bash
python flappy_bird.py
```

### Controls

* **SPACE**: Flap the bird
* **SPACE (in Menu)**: Start game
* **SPACE (in Game Over)**: Restart game
* **ESC / X**: Close the game window

---

## 📊 Game Logic Overview

* **Bird Class**: Controls movement, physics, rotation, flap action, and collision
* **Pipe Class**: Handles obstacle generation, scrolling, and scoring
* **GameState Enum**: Manages transitions between Menu, Playing, and Game Over
* **Game Loop**: Updates frame, processes input, and handles rendering

---

## 📌 Save System

High score is saved in a file named `high_score.txt` inside the main directory. It will be created automatically after the first playthrough.

---

## 🧠 Learning Outcomes

* Real-time game development using `pygame`
* Structured object-oriented programming
* Efficient sprite handling, collision detection, and event management
* File I/O for persistent score storage
* Frame-rate and input optimization

---

## 🔈 Sound Credits

All sound effects used are custom or free assets from open libraries. Replace them in the `assets/` folder as needed.

---

## 👩‍💻 Author

**Astha Dakhinray**
🎓 B.Tech in CSE | Passionate Python & Game Developer
🔗 [LinkedIn](https://www.linkedin.com/in/astha-dakhinray-02b0852a0/) | [Instagram](https://www.instagram.com/reyalistic.me?igsh=a2lmMWFuamE3MHJn)

---


