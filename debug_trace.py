
try:
    with open("verification_output_phase2_final2.txt", "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")
        print(content[-2000:])
except Exception as e:
    print(e)
