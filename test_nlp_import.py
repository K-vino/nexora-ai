print("Starting import test...")
try:
    from nlp_engine.text_cleaning import TextCleaner
    print("Imported TextCleaner")
    tc = TextCleaner()
    print("Initialized TextCleaner")
    print(tc.clean_text("Hello World!"))
except Exception as e:
    print(f"Error: {e}")
print("Test Complete")
