from template import call_openai

if __name__ == "__main__":
    prompt = "Hãy kể cho tôi một sự thật thú vị về Việt Nam."
    temperatures = [0.0, 0.5, 1.0, 1.5]

    for temp in temperatures:
        response, latency = call_openai(prompt, temperature=temp, top_p=0.9, max_tokens=256)
        print(f"temperature={temp}")
        print(response.strip())
        print(f"latency={latency:.3f}s")
        print("---")
