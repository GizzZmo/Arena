"""
Cyberchess Arena: AI Chess Training Platform

This module implements a chess training arena where Google's Gemini AI plays against
Stockfish chess engine to learn and improve through gameplay. The system features:

- Real-time gameplay between AI agents
- Feedback loop for illegal move correction
- Automatic game data collection for future fine-tuning
- PGN (Portable Game Notation) export for training datasets

The project follows a multi-phase approach:
    Phase 1: Arena setup and gameplay mechanics
    Phase 2: Data collection from games
    Phase 3: Fine-tuning Gemini with collected data (future)
    Phase 4: Continuous improvement loop (future)

Dependencies:
    - python-chess: Chess game logic and board management
    - google-generativeai: Gemini AI model interface
    - stockfish: Chess engine binary (external)

Author: Jon Arve Ovesen
License: MIT
"""

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
# Configure the Gemini API with authentication
genai.configure(api_key=GOOGLE_API_KEY)
# Using Flash model for faster response times during gameplay
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_move(board, retries=3):
    """
    Request a chess move from Gemini AI with error handling and retry logic.
    
    This function sends the current board state to Gemini and requests a legal move.
    It implements in-context learning by providing feedback when Gemini makes mistakes,
    helping the AI learn from its errors within the same game.
    
    Args:
        board (chess.Board): The current chess board state
        retries (int, optional): Number of retry attempts for illegal moves. Defaults to 3.
    
    Returns:
        chess.Move: A valid chess move. Returns a random legal move if Gemini fails
                    after all retry attempts.
    
    Raises:
        None: Exceptions are caught and handled internally with fallback to random move.
    
    Notes:
        - Provides board FEN (Forsyth-Edwards Notation) for position understanding
        - Lists all legal moves to ground Gemini's reasoning and reduce hallucinations
        - Cleans up common formatting issues (markdown, whitespace)
        - Implements progressive feedback loop for illegal move correction
    """
    # Extract all legal moves in UCI (Universal Chess Interface) format
    legal_moves = [move.uci() for move in board.legal_moves]
    
    # Construct the initial prompt with board state and legal moves
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

    # Retry loop with progressive feedback
    for attempt in range(retries):
        try:
            # Request move from Gemini
            response = model.generate_content(prompt)
            move_str = response.text.strip().replace("\n", "").replace(" ", "")
            
            # Clean up common formatting issues if Gemini adds markdown
            move_str = move_str.replace("`", "") 

            # Parse the move string into a chess.Move object
            move = chess.Move.from_uci(move_str)

            # Validate that the move is legal
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
                # This helps Gemini understand its mistake and correct it
                prompt += f"\n\nERROR: {move_str} is not a legal move. Please choose strictly from the provided list."
        
        except Exception as e:
            print(f" > Error parsing Gemini response: {e}")
            # Provide format correction feedback
            prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."

    # Fallback: If Gemini fails after all retries, make a random move to keep the game going
            prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."

    # If Gemini fails 3 times, we make a random move to keep the game going (fallback)
    print(" > Gemini failed to produce a legal move. Making random move.")
    import random
    return random.choice(list(board.legal_moves))

def play_game():
    """
    Execute a complete chess game between Stockfish and Gemini AI.
    
    This function orchestrates a full game where:
    - Stockfish (White) plays as the teacher with limited skill level
    - Gemini (Black) plays as the student learning from gameplay
    - Moves are printed to console for observation
    - The game continues until checkmate, stalemate, or draw
    
    Returns:
        chess.Board: The final board state after game completion, used for
                     data collection and analysis.
    
    Game Configuration:
        - Stockfish Skill Level: 5 (out of 20) - balanced for learning
        - Stockfish Time Limit: 0.1 seconds per move - ensures fast gameplay
        - Board Display: Console ASCII representation after each move
    
    Notes:
        - All moves are recorded for potential training data
        - Game result includes checkmate, stalemate, or draw conditions
        - Engine is properly closed after game completion
    """
    # Initialize a new chess board at starting position
    board = chess.Board()
    # Start the Stockfish engine process
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
    # Set Stockfish skill level (Lower it initially so Gemini has a chance)
    # Skill level 0 is weak, 20 is Grandmaster. Starting at 5 for balanced learning.
    # Initialize Board and Stockfish
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
    # Set Stockfish skill level (Lower it initially so Gemini has a chance)
    # Skill level 0 is weak, 20 is Grandmaster. Let's start at 5.
    engine.configure({"Skill Level": 5})

    print("--- CYBERCHESS: Stockfish (White) vs Gemini (Black) ---")
    
    # Track all moves made during the game (for future analysis)
    game_moves = []
    
    # Main game loop - continues until game ends
    while not board.is_game_over():
        # Display current move number and board state
    game_moves = []
    
    while not board.is_game_over():
        print(f"\nMove {board.fullmove_number}")
        print(board)
        
        if board.turn == chess.WHITE:
            # --- STOCKFISH TURN (Teacher) ---
            print("Stockfish is thinking...")
            # Limit Stockfish to 0.1 seconds so it plays fast and games don't take too long
            # --- STOCKFISH TURN ---
            print("Stockfish is thinking...")
            # Limit Stockfish to 0.1 seconds so it plays fast
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
            print(f"Stockfish played: {result.move.uci()}")
            game_moves.append(result.move)
            
        else:
            # --- GEMINI TURN (Student) ---
            # --- GEMINI TURN ---
            print("Gemini is thinking...")
            move = get_gemini_move(board)
            board.push(move)
            print(f"Gemini played: {move.uci()}")
            game_moves.append(move)

    # --- GAME OVER ---
    # Display final result (1-0 = White wins, 0-1 = Black wins, 1/2-1/2 = Draw)
    print("\n--- GAME OVER ---")
    print(f"Result: {board.result()}")
    
    # Properly shutdown the Stockfish engine
    print("\n--- GAME OVER ---")
    print(f"Result: {board.result()}")
    
    engine.quit()
    return board

def save_game_data(board):
    """
    Save completed game data to a PGN file for future model training.
    
    This function exports the game to PGN (Portable Game Notation) format,
    which is the standard format for chess games. The accumulated games in
    this file will be used to fine-tune Gemini in Phase 3 of the project.
    
    Args:
        board (chess.Board): The completed game board state containing full move history
    
    Output:
        Creates or appends to 'training_data.pgn' in the current directory.
        Each game includes metadata headers and the complete move sequence.
    
    PGN Headers:
        - Event: "Cyberchess Dojo" - identifies the training context
        - White: "Stockfish Level 5" - the teacher engine
        - Black: "Gemini 1.5 Flash" - the student model
        - Date: Current date in YYYY.MM.DD format
    
    Notes:
        - File is opened in append mode to accumulate multiple games
        - Each game is separated by double newline for parsing
        - Accumulate 1000+ games before attempting fine-tuning
    """
    # Convert the board state to PGN format with full move history
    pgn_game = chess.pgn.Game.from_board(board)
    # Add metadata headers for dataset organization
    Saves the game to a PGN file. 
    This is the dataset we will use later to FINE TUNE Gemini.
    """
    pgn_game = chess.pgn.Game.from_board(board)
    pgn_game.headers["Event"] = "Cyberchess Dojo"
    pgn_game.headers["White"] = "Stockfish Level 5"
    pgn_game.headers["Black"] = "Gemini 1.5 Flash"
    pgn_game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")

    # Append game to training dataset file
    with open("training_data.pgn", "a") as f:
        f.write(str(pgn_game) + "\n\n")
    print("Game saved to 'training_data.pgn'")

if __name__ == "__main__":
    """
    Main execution entry point.
    
    Current Mode: Single game execution
    
    For continuous training, modify to run in a loop:
        while True:
            finished_board = play_game()
            save_game_data(finished_board)
    
    This will accumulate games overnight for dataset building.
    """
    # Play a single game and save the results
    # In a real app, you would loop this: while True: play_game()
    finished_board = play_game()
    save_game_data(finished_board)
