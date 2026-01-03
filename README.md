# Arena

This is the **"Arena" prototype**. This script sets up the environment where Stockfish (The Teacher) plays against Gemini (The Student).

It includes a feedback loop: if Gemini tries to make an illegal move, the script catches it, tells Gemini *why* it was illegal, and asks it to try again (In-context correction).

### Prerequisites
Before running the code, you need three things:
1.  **Python Libraries:** Run this in your terminal:
    ```bash
    pip install python-chess google-generativeai
    ```
2.  **Stockfish Engine:** Download the Stockfish executable for your OS (Windows/Mac/Linux) from [stockfishchess.org](https://stockfishchess.org/download/). Note the path to where you save it.
3.  **Gemini API Key:** Get one from Google AI Studio.
4.  **Environment variables:** Configure once so you do not edit code:
    ```bash
    export STOCKFISH_PATH="/full/path/to/stockfish"
    export GOOGLE_API_KEY="your_gemini_key"
    # optional: how many games to run per session and where to store PGNs
    export ARENA_GAMES=5
    export ARENA_OUTPUT_DIR="data"
    ```

### The Python Code (`cyberchess.py`)

Create a file named `cyberchess.py` and paste this code in. **Make sure to set `STOCKFISH_PATH` and `GOOGLE_API_KEY` (env vars recommended).**

```python
import chess
import chess.engine
import chess.pgn
import google.generativeai as genai
import time
import datetime

# --- CONFIGURATION ---
# REPLACE THIS with the path to your downloaded stockfish file
# Windows example: "C:/Users/Jon/Downloads/stockfish/stockfish-windows-x86-64.exe"
# Mac example: "/opt/homebrew/bin/stockfish"
STOCKFISH_PATH = "YOUR_STOCKFISH_PATH_HERE" 

# REPLACE THIS with your Google Gemini API Key
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Setup Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Using Flash for speed

def get_gemini_move(board, retries=3):
    """
    Sends the board state to Gemini and asks for a move.
    Includes a retry loop for illegal moves.
    """
    legal_moves = [move.uci() for move in board.legal_moves]
    
    # We provide the FEN (Board State) and the list of legal moves to help Gemini
    # ground its reasoning and avoid hallucinations.
    prompt = f"""
    You are playing a game of Chess against Stockfish. You are playing Black.
    
    Current Board Position (FEN): {board.fen()}
    
    Here is the list of legally possible moves you can make:
    {', '.join(legal_moves)}
    
    Your goal is to survive and learn. Analyze the board.
    Pick the best move from the legal list above.
    
    IMPORTANT: Reply ONLY with the move in UCI format (e.g., e7e5). Do not write any other text.
    """

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            move_str = response.text.strip().replace("\n", "").replace(" ", "")
            
            # clean up common formatting issues if Gemini adds markdown
            move_str = move_str.replace("`", "") 

            move = chess.Move.from_uci(move_str)

            if move in board.legal_moves:
                return move
            else:
                print(f" > Gemini tried illegal move: {move_str}. Retrying...")
                # Add feedback to the next prompt (In-Context Learning)
                prompt += f"\n\nERROR: {move_str} is not a legal move. Please choose strictly from the provided list."
        
        except Exception as e:
            print(f" > Error parsing Gemini response: {e}")
            prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."

    # If Gemini fails 3 times, we make a random move to keep the game going (fallback)
    print(" > Gemini failed to produce a legal move. Making random move.")
    import random
    return random.choice(list(board.legal_moves))

def play_game():
    # Initialize Board and Stockfish
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
    # Set Stockfish skill level (Lower it initially so Gemini has a chance)
    # Skill level 0 is weak, 20 is Grandmaster. Let's start at 5.
    engine.configure({"Skill Level": 5})

    print("--- CYBERCHESS: Stockfish (White) vs Gemini (Black) ---")
    
    game_moves = []
    
    while not board.is_game_over():
        print(f"\nMove {board.fullmove_number}")
        print(board)
        
        if board.turn == chess.WHITE:
            # --- STOCKFISH TURN ---
            print("Stockfish is thinking...")
            # Limit Stockfish to 0.1 seconds so it plays fast
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
            print(f"Stockfish played: {result.move.uci()}")
            game_moves.append(result.move)
            
        else:
            # --- GEMINI TURN ---
            print("Gemini is thinking...")
            move = get_gemini_move(board)
            board.push(move)
            print(f"Gemini played: {move.uci()}")
            game_moves.append(move)

    # --- GAME OVER ---
    print("\n--- GAME OVER ---")
    print(f"Result: {board.result()}")
    
    engine.quit()
    return board

def save_game_data(board):
    """
    Saves the game to a PGN file. 
    This is the dataset we will use later to FINE TUNE Gemini.
    """
    pgn_game = chess.pgn.Game.from_board(board)
    pgn_game.headers["Event"] = "Cyberchess Dojo"
    pgn_game.headers["White"] = "Stockfish Level 5"
    pgn_game.headers["Black"] = "Gemini 1.5 Flash"
    pgn_game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")

    with open("training_data.pgn", "a") as f:
        f.write(str(pgn_game) + "\n\n")
    print("Game saved to 'training_data.pgn'")

if __name__ == "__main__":
    # In a real app, you would loop this: while True: play_game()
    finished_board = play_game()
    save_game_data(finished_board)
```

> The repository version of `cyberchess.py` includes a session runner that honors `ARENA_GAMES`/`ARENA_OUTPUT_DIR`, validates configuration, and writes timestamped PGNs automatically—use the shipped file when in doubt.

### How to use this for "Learning"

The script above handles **Phase 1 (The Arena)** and **Phase 2 (Data Collection)**.

Here is how you handle the learning part:

1.  **Run automated sessions:** `ARENA_GAMES=10 ARENA_OUTPUT_DIR=data python cyberchess.py` will run 10 games back-to-back and drop per-game PGNs plus an aggregated `training_data.pgn` in the chosen directory. Leave it running overnight for growth.
2.  **Accumulate Data:** Each game is timestamped and annotated with ply count, duration, and termination reason so you can filter later.
3.  **The Analysis:** Gemini will lose almost every game at first. But occasionally, it will survive 20 or 30 moves.
4.  **Fine Tuning (The Next Step):** Once you have 1,000 games in that PGN file, you can upload that file to Google Vertex AI to create a **Fine-Tuned Model**. You then update the script to use `model = genai.GenerativeModel('your-finetuned-model-name')`.

Do you have the Stockfish binary downloaded, or do you need help finding the right version for your computer?

## Documentation & Wiki

The GitHub Wiki tracks practical details that should stay short and easy to scan:
- **Setup & Configuration:** Stockfish install paths, engine skill presets, and how to set `GOOGLE_API_KEY`.
- **Running Arena Sessions:** Example commands, troubleshooting illegal-move retries, and saving PGN outputs.
- **Data Management:** How to rotate or archive `training_data.pgn` and tips for fine-tuning inputs.
- **FAQ:** Common errors (engine not found, API auth) and quick fixes.

Best practices for pages:
- Lead with a 3–7 step checklist and copy/paste commands.
- Keep configuration values in one place; reference `.env` keys instead of repeating secrets.
- Add a short “Last verified on (date) with version (x.y)” note for commands that can drift.
- Prefer links to upstream docs instead of duplicating long explanations.

## Roadmap

1. **Phase 1 – Arena Loop (Completed):** Stockfish vs. Gemini with illegal-move feedback and PGN logging. ✅ Definition of done: stable loop with reproducible setup docs.
2. **Phase 2 – Data Growth (In progress):** Automated long-running sessions, basic telemetry (move counts, termination reason), and improved PGN metadata. Definition of done: nightly runs produce timestamped PGNs with minimal manual babysitting.
3. **Phase 3 – Fine-Tuning:** Export `training_data.pgn` to Vertex AI, swap in the fine-tuned model name, and validate against a fixed test suite of positions. ✅ Definition of done: baseline ELO/position tests recorded before and after swap.
4. **Phase 4 – UX & Sharing:** Provide a CLI flag for headless runs, optional web viewer for games, and wiki guides for contributors. ✅ Definition of done: one-command start and a contributor page with expectations.
