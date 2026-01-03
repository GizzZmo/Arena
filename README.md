# Arena - AI Chess Training Platform

> A Python-based chess training environment where Google's Gemini AI learns to play chess by competing against Stockfish.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Phase%202%20Complete-success.svg)](ROADMAP.md)

## 🎯 Overview

**Arena** (also known as "Cyberchess") is an experimental platform that creates a learning environment for AI models. The system pits Google's Gemini AI against the Stockfish chess engine, collecting gameplay data for future model fine-tuning. This project explores AI learning through gameplay, feedback loops, and iterative improvement.

### Key Features

- 🤖 **AI vs Engine Gameplay**: Gemini (Black) learns by playing against Stockfish (White)
- 🔄 **Feedback Loop**: In-context learning with illegal move correction
- 📊 **Data Collection**: Automatic export to PGN format for training datasets
- ⚡ **Fast Iteration**: Quick games with configurable difficulty levels
- 🎓 **Educational**: Transparent code for learning AI/ML concepts

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Stockfish Chess Engine** - Download from [stockfishchess.org](https://stockfishchess.org/download/)
3. **Google Gemini API Key** - Get one from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/GizzZmo/Arena.git
cd Arena

# Install required Python packages
pip install python-chess google-generativeai
```

### Configuration

Edit `cyberchess.py` and update the configuration section:

```python
# Path to your Stockfish executable
STOCKFISH_PATH = "/path/to/stockfish"  # e.g., "C:/stockfish/stockfish.exe" on Windows

# Your Gemini API key
GOOGLE_API_KEY = "your_api_key_here"
```

### Run a Game

```bash
python cyberchess.py
```

Watch as Gemini and Stockfish battle it out! The game will be displayed in your terminal, and results will be saved to `training_data.pgn`.

## 📖 Documentation

- **[ROADMAP.md](ROADMAP.md)** - Project roadmap and future plans
- **Code Documentation** - Comprehensive docstrings in `cyberchess.py`
- **API References** - See inline comments for detailed explanations

## 🎮 How It Works

### The Training Process

1. **Arena Setup (Phase 1)**: Stockfish and Gemini are initialized with the chess board
2. **Gameplay (Phase 2)**: 
   - Stockfish (White) plays as the "teacher" at skill level 5
   - Gemini (Black) plays as the "student" learning from experience
   - If Gemini makes an illegal move, it receives feedback and retries
3. **Data Collection**: Each completed game is saved to `training_data.pgn`
4. **Fine-tuning (Phase 3 - Future)**: Accumulated games will be used to fine-tune Gemini

### Sample Game Output

```
--- CYBERCHESS: Stockfish (White) vs Gemini (Black) ---

Move 1
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R

Stockfish is thinking...
Stockfish played: e2e4
Gemini is thinking...
Gemini played: e7e5
...
```

## 🔄 Continuous Training

For overnight data collection, modify the main block to loop:

```python
if __name__ == "__main__":
    while True:
        finished_board = play_game()
        save_game_data(finished_board)
```

This will continuously generate games for your training dataset.

## 📊 Current Status

- ✅ **Phase 1**: Arena setup and gameplay mechanics - *Complete*
- ✅ **Phase 2**: Data collection and feedback loop - *Complete*
- 🎯 **Phase 3**: Model fine-tuning with Vertex AI - *Next Up*
- 📋 **Phase 4**: Continuous improvement loop - *Planned*
- 🚀 **Phase 5**: Advanced features and optimization - *Future*

See [ROADMAP.md](ROADMAP.md) for detailed plans.

## 🛠️ Technical Details

### Architecture

```
┌─────────────┐         ┌──────────────┐
│  Stockfish  │ ◄─────► │  Chess Board │
│  (Teacher)  │         │    (State)   │
└─────────────┘         └──────────────┘
                              ▲
                              │
                              ▼
                        ┌──────────────┐
                        │    Gemini    │
                        │  (Student)   │
                        └──────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │  PGN Export  │
                        │ (Training    │
                        │  Data)       │
                        └──────────────┘
```

### Dependencies

- **python-chess**: Chess game logic and board management
- **google-generativeai**: Gemini API interface
- **Stockfish**: External chess engine binary

### Key Components

- `get_gemini_move()`: AI move generation with retry logic
- `play_game()`: Game orchestration and execution
- `save_game_data()`: PGN export for training data

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🎮 Run games and share training data
- 💻 Submit pull requests

See [ROADMAP.md](ROADMAP.md) for areas where contributions are needed.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Stockfish Team** - For the powerful open-source chess engine
- **Google Gemini** - For the AI model capabilities
- **python-chess** - For the excellent chess library
- **Community Contributors** - Everyone who helps improve this project

## 📧 Contact

- **Author**: Jon Arve Ovesen (GizzZmo)
- **GitHub**: [GizzZmo/Arena](https://github.com/GizzZmo/Arena)
- **Issues**: [Report a bug or request a feature](https://github.com/GizzZmo/Arena/issues)

## 🔗 Resources

- [Stockfish Download](https://stockfishchess.org/download/)
- [Google AI Studio](https://aistudio.google.com/)
- [Python-chess Documentation](https://python-chess.readthedocs.io/)
- [Project Roadmap](ROADMAP.md)

---

*Built with ❤️ for AI research and education*
