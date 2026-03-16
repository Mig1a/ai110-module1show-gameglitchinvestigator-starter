# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The game loaded but immediately felt broken. The difficulty settings didn't behave as expected — selecting "Hard" was actually easier than "Normal" because its range was only 1–50 while Normal went to 100. The attempt counter also started at 1 instead of 0, so the very first guess wasn't counted, and the attempts-left display never updated until the next action.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
    1.  Hard range was 1–50 — easier than Normal (1–100)
    2.  Hint messages were backwards — "Too High" said Go 
    3.  HIGHER, "Too Low" said Go LOWER On even attempts, secret was converted to a str, breaking comparisons with int guesses
    4.  No range validation — guesses outside the difficulty range were accepted
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  I used Claude Code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude correctly identified that the hint messages in check_guess were swapped — when the guess was too high, the message said "Go HIGHER!" and vice versa. It suggested flipping the return strings on lines 41–43 of app.py. I verified this by reading the logic myself: if guess > secret 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  Claude's first fix for the attempt counter not registering the first guess was to change the initialization from 1 to 0. That alone didn't fully solve the problem — the st.info display still showed a stale count because it rendered before the submit block ran. It took two more follow-up fixes (moving the increment inside the valid-guess block, then using st.empty() as a placeholder) before the counter updated correctly. I verified the real issue by tracing the Streamlit render order myself and confirming the count only changed after pressing submit a second time

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  
  By playing around with the app and by running a test that would have caught the original bug.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
   
    The most concrete verification came from the pytest suite Claude helped generate in tests/test_game_logic.py. One specific test targeted the update_score bug where attempt_number + 1 caused the first attempt to score 80 instead of 90:

- Did AI help you design or understand any tests? How?

    Yes — Claude generated the full test file and explained the reasoning behind each test group. For example, it pointed out that the original tests in the file were already broken because they compared check_guess(...) directly to a string like "Win", but the function actually returns a tuple (outcome, message). 
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

  Every time I clicked a button, typed a guess, or changed the difficulty, Streamlit threw away everything and re-ran the entire app.py script from line 1. That means random.randint(low, high) would run again and pick a brand new number — so the target kept shifting underneath the mid-game.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  I would explain it by imagine writing guess on a whiteboard, but every time you blink, someone erases the whole board and rewrites it from scratch.

- What change did you make that finally gave the game a stable secret number?

  The guard at the top of the app this means the secret is only ever generated once — on the very first load. Every rerun after that skips it because the key already exists in session state. The same pattern was applied to attempts, score, status, and history to keep all game data stable across interactions.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  - This could be a testing habit, a prompting strategy, or a way you used Git.

  One habit or strategy to reuse writing pytest tests that are specifically tied to each bug — not just general "does it work" tests, but tests named after the exact failure.

- What is one thing you would do differently next time you work with AI on a coding task?
  NONE
- In one or two sentences, describe how this project changed the way you think about AI generated code.

    AI-generated code can look completely correct and still contain subtle logic bugs that only show up at runtime — like hints pointing the wrong direction or a secret silently changing type — so treating AI output as a first draft that always needs human review, not a finished product, is the only safe approach.
