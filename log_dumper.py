
try:
    with open("verification_output_phase2_final2.txt", "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")
        with open("dump_log.txt", "w", encoding="utf-8") as out:
            out.write(content)
except Exception as e:
    print(e)
