import os
from pathlib import Path
from deep_translator import GoogleTranslator
import pyttsx3

MAX_CHARS = 4500  # limiet per vertaalstuk

def split_text(text, max_length=MAX_CHARS):
    """Knip lange tekst op in stukken van maximaal max_length tekens."""
    lines = text.splitlines()
    chunks = []
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 > max_length:
            chunks.append(current)
            current = ""
        current += line + "\n"
    if current:
        chunks.append(current)
    return chunks

def vertaal_bestanden(bronmap, doelmap, src_lang="en", target_lang="nl"):
    bronmap = Path(bronmap)
    doelmap = Path(doelmap)
    doelmap.mkdir(exist_ok=True)

    bestanden = list(bronmap.glob("*.txt"))
    print(f"📁 Gevonden {len(bestanden)} bestanden in {bronmap}")

    for bestand in bestanden:
        with open(bestand, "r", encoding="utf-8") as f:
            tekst = f.read()

        stukken = split_text(tekst)
        vertaalde_tekst = ""

        print(f"🔁 Vertalen: {bestand.name}")
        for stuk in stukken:
            vertaling = GoogleTranslator(source=src_lang, target=target_lang).translate(stuk)
            vertaalde_tekst += vertaling + "\n"

        doelpad = doelmap / bestand.name
        with open(doelpad, "w", encoding="utf-8") as f:
            f.write(vertaalde_tekst)
        print(f"✅ Opgeslagen vertaling: {doelpad}")

def lees_en_voor(bestandsmap):
    bestanden = list(Path(bestandsmap).glob("*.txt"))
    if not bestanden:
        print("❌ Geen vertaalde tekstbestanden gevonden.")
        return

    print("\n📃 Kies een bestand om voor te lezen:")
    for i, bestand in enumerate(bestanden):
        print(f"{i+1}. {bestand.name}")

    try:
        keuze = int(input("Nummer: ")) - 1
        if keuze < 0 or keuze >= len(bestanden):
            print("❌ Ongeldige keuze.")
            return
    except ValueError:
        print("❌ Ongeldige invoer.")
        return

    gekozen_bestand = bestanden[keuze]
    with open(gekozen_bestand, "r", encoding="utf-8") as f:
        tekst = f.read()

    print(f"\n🎙️ Voorlezen van: {gekozen_bestand.name}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # [0] = standaardstem, [1] = alternatieve stem als beschikbaar
    engine.say(tekst)
    engine.runAndWait()

def main():
    # Hardcoded pad naar jouw projectmap
    projectpad = Path("D:/Git/School/Translator")
    bronmap = projectpad / "teksten"
    doelmap = projectpad / "vertaald"

    vertaal_bestanden(bronmap, doelmap)
    lees_en_voor(doelmap)

if __name__ == "__main__":
    main()

