#!/usr/bin/env python3
"""
make_corpus.py  --  Generate U.S. Army field-manual-style PDFs for Edge Brain Mesh.
Writes 4 PDFs into corpus/:
    medic_TCCC.pdf
    repair_TM.pdf
    policy_ROE.pdf
    restricted_CBRN.pdf
"""
from pathlib import Path
from fpdf import FPDF

CORPUS_DIR = Path(__file__).parent / "corpus"
CORPUS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Doctrine data extracted verbatim from server.py BRAINS dict
# ---------------------------------------------------------------------------

DOCS = [
    {
        "filename": "medic_TCCC.pdf",
        "title": "TC 4-02.1 / TCCC GUIDELINES",
        "doc_number": "TC 4-02.1",
        "brain_name": "COMBAT CASUALTY CARE BRAIN",
        "header": "TACTICAL COMBAT CASUALTY CARE (TCCC) GUIDELINES",
        "chunks": [
            {
                "src": "TCCC Guidelines / TC 4-02.1, MARCH",
                "text": (
                    "Massive hemorrhage. Apply a CoTCCC tourniquet high and tight on the limb, "
                    "over the uniform, two to three inches above the wound. Tighten until bright "
                    "red bleeding stops and the distal pulse is gone. Mark the time on the "
                    "tourniquet. Do not loosen it."
                ),
            },
            {
                "src": "TCCC Guidelines / TC 4-02.1, MARCH",
                "text": (
                    "Airway. If unconscious, open the airway with a chin lift or insert a "
                    "nasopharyngeal airway and place the casualty in the recovery position. "
                    "Breathing. For a penetrating chest wound, apply a vented chest seal and "
                    "monitor for tension pneumothorax."
                ),
            },
            {
                "src": "ATP 4-25.13, 9-Line MEDEVAC",
                "text": (
                    "To request evacuation, transmit the nine line MEDEVAC: Line 1 location, "
                    "Line 2 your callsign and frequency, Line 3 number of patients by precedence, "
                    "Line 4 special equipment, Line 5 patients by type litter or ambulatory, "
                    "Line 6 security at pickup site, Line 7 method of marking, Line 8 patient "
                    "nationality, Line 9 terrain or CBRN contamination."
                ),
            },
            {
                "src": "TCCC Guidelines, Circulation / TXA",
                "text": (
                    "Circulation. If the casualty is in hemorrhagic shock, establish IV or IO "
                    "access and give tranexamic acid as soon as possible, ideally within one hour, "
                    "but not after three hours from injury. Prevent hypothermia: remove wet gear "
                    "and wrap the casualty in a warming blanket."
                ),
            },
        ],
    },
    {
        "filename": "repair_TM.pdf",
        "title": "EQUIPMENT & WEAPONS -- TM 9-SERIES",
        "doc_number": "TM 9-SERIES",
        "brain_name": "EQUIPMENT & WEAPONS REPAIR BRAIN",
        "header": "TECHNICAL MANUAL: OPERATOR / CREW MAINTENANCE & WEAPONS REPAIR",
        "chunks": [
            {
                "src": "TC 3-22.9, Immediate Action (SPORTS)",
                "text": (
                    "Weapon stoppage. Perform immediate action - SPORTS. Slap the bottom of the "
                    "magazine to seat it. Pull the charging handle to the rear. Observe for an "
                    "ejected round and chamber. Release the charging handle to chamber a fresh "
                    "round. Tap the forward assist. Squeeze the trigger to fire."
                ),
            },
            {
                "src": "TM 9-1005-313, M240 Stoppage",
                "text": (
                    "M240 stoppage. Pull and lock the charging handle to the rear and place the "
                    "weapon on safe. Open the feed tray cover and inspect for a ruptured cartridge "
                    "or a broken link. Clear the chamber, reload a fresh belt, close the cover, "
                    "and resume firing. For a runaway gun, break the belt to stop feeding."
                ),
            },
            {
                "src": "TM 9-2320, PMCS",
                "text": (
                    "Vehicle no-start. Run before-operation PMCS. Check the battery connections "
                    "are tight and not corroded, confirm the fuel shutoff is open and there is "
                    "fuel, and verify the master switch is on. If the engine cranks but will not "
                    "start, prime the fuel system and bleed air from the fuel filter."
                ),
            },
        ],
    },
    {
        "filename": "policy_ROE.pdf",
        "title": "POLICY & RULES OF ENGAGEMENT -- ATP 6-01.1 / GTA 21-08",
        "doc_number": "ATP 6-01.1 / GTA 21-08",
        "brain_name": "POLICY, ROE & REPORTING BRAIN",
        "header": "POLICY, RULES OF ENGAGEMENT & FIELD REPORTING GUIDE",
        "chunks": [
            {
                "src": "GTA 21-08, SALUTE Report",
                "text": (
                    "Report enemy activity with SALUTE: Size of the element, Activity they are "
                    "doing, Location grid, Unit or uniform identification, Time observed, and "
                    "Equipment they carry. Send it to higher immediately."
                ),
            },
            {
                "src": "Standing ROE / EOF",
                "text": (
                    "Rules of engagement. You always retain the right of self defense against a "
                    "hostile act or demonstrated hostile intent. Escalation of force: shout a "
                    "warning, show your weapon, shove or use a physical barrier, then fire only "
                    "as a last resort and only proportionally. Positively identify the target "
                    "before engaging."
                ),
            },
            {
                "src": "ATP 6-01.1, SITREP",
                "text": (
                    "Situation report. Transmit your callsign, current location, enemy situation, "
                    "your unit status and combat effectiveness, and any logistics or medical needs. "
                    "Keep it brief and end with any request for guidance."
                ),
            },
        ],
    },
    {
        "filename": "restricted_CBRN.pdf",
        "title": "ATP 3-11.32 / CBRN REACTION & COMSEC",
        "doc_number": "ATP 3-11.32",
        "brain_name": "CBRN & CONTROLLED CRYPTO BRAIN",
        "header": "CBRN DEFENSE AND CONTROLLED CRYPTOGRAPHIC ITEM PROCEDURES",
        "chunks": [
            {
                "src": "ATP 3-11.32, CBRN Reaction",
                "text": (
                    "CBRN attack. Stop breathing, don and clear your protective mask within nine "
                    "seconds, give the alarm by shouting Gas Gas Gas, and assume MOPP 4. Begin "
                    "immediate decontamination of exposed skin with the decon kit and report the "
                    "attack to higher."
                ),
            },
            {
                "src": "Controlled - COMSEC handling",
                "text": (
                    "COMSEC. Load the cryptographic key into the radio with the fill device, "
                    "verify the key with the receiving station, and zeroize the device if capture "
                    "is imminent. Handle and store keying material per controlled cryptographic "
                    "item procedures."
                ),
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------

def build_pdf(doc: dict) -> Path:
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ---- Page header / classification bar ----
    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 7, "UNCLASSIFIED // FOR OFFICIAL USE ONLY", align="C", fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)

    # ---- Department of the Army header ----
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "HEADQUARTERS, DEPARTMENT OF THE ARMY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, "Washington, DC", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # ---- Horizontal rule ----
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.8)
    lm = pdf.l_margin
    pw = pdf.epw
    pdf.line(lm, pdf.get_y(), lm + pw, pdf.get_y())
    pdf.ln(5)

    # ---- Document number ----
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, doc["doc_number"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ---- Main title ----
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 9, doc["header"], align="C")
    pdf.ln(2)

    # ---- Brain name subtitle ----
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 6, f"Edge Brain Mesh Node: {doc['brain_name']}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # ---- Distribution statement ----
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, "DISTRIBUTION: Approved for public release; distribution is unlimited.", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # ---- Thin rule before sections ----
    pdf.set_line_width(0.3)
    pdf.line(lm, pdf.get_y(), lm + pw, pdf.get_y())
    pdf.ln(6)

    # ---- Sections ----
    for idx, chunk in enumerate(doc["chunks"], start=1):
        # Section heading
        pdf.set_font("Helvetica", "B", 11)
        heading = f"Section {idx}.  {chunk['src']}"
        pdf.multi_cell(0, 6, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Body text
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, chunk["text"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

        # Light divider between sections
        if idx < len(doc["chunks"]):
            pdf.set_line_width(0.1)
            pdf.set_draw_color(160, 160, 160)
            pdf.line(lm, pdf.get_y(), lm + pw, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)

    # ---- Footer classification bar ----
    pdf.set_y(-15)
    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 7, "UNCLASSIFIED // FOR OFFICIAL USE ONLY", align="C", fill=True,
             new_x="LMARGIN", new_y="NEXT")

    out_path = CORPUS_DIR / doc["filename"]
    pdf.output(str(out_path))
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating corpus PDFs into:", CORPUS_DIR.resolve())
    print()
    results = []
    for doc in DOCS:
        path = build_pdf(doc)
        size = path.stat().st_size
        results.append((path, size))
        print(f"  WROTE  {path.name:30s}  {size:>7,} bytes")

    print()
    print("Done. All 4 PDFs generated.")

    # ---- Quick text-extraction check ----
    print()
    print("Text-extraction check (first PDF):")
    first_pdf = results[0][0]
    try:
        import importlib.util
        if importlib.util.find_spec("pypdf") is not None:
            from pypdf import PdfReader
            reader = PdfReader(str(first_pdf))
            text = reader.pages[0].extract_text() or ""
            print(f"  pypdf extracted {len(text)} chars from page 1 of {first_pdf.name}")
            print(f"  First 200 chars: {text[:200]!r}")
        else:
            # fallback: just confirm size
            size = first_pdf.stat().st_size
            print(f"  pypdf not installed; confirmed {first_pdf.name} is {size:,} bytes (> 1 KB: {size > 1024})")
    except Exception as e:
        size = first_pdf.stat().st_size
        print(f"  Text-check error ({e}); confirmed size {size:,} bytes.")
