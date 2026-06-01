import streamlit as st
from Bio.Seq import Seq
from Bio import SeqIO
import io  # Python ka internal tool string ko file memory mein badalne ke liye

# --- APPLICATION UI LAYOUT ---
st.set_page_config(page_title="ZEROv0.3.9", page_icon="🧬", layout="wide")

st.title("🧬 ZEROv0.3.9 : Personal Bio-Assistant")
st.subheader("Automated File-Driven Pipeline")

# Sidebar for Navigation
st.sidebar.title("🎛️ Control Panel")
choice = st.sidebar.selectbox("Select Analytical Tool:", [
    "DNA Length Calculator",
    "DNA Slicing (Codon Chopper)",
    "Perform DNA Transcription",
    "DNA Replication (Complement)",
    "Reverse Transcription",
    "Perform RNA Translation",
    "GC Content Calculator"
])

# --- FILE UPLOADER COMPONENT ---
st.write("### 📁 Upload your biological data sequence:")
uploaded_file = st.file_uploader("Drop a .fasta or .txt file here", type=["fasta", "txt"])

if uploaded_file is not None:
    # 1. Blank File Check (Efficiency check from your backend code)
    if uploaded_file.size == 0:
        st.error("❌ ERROR: The uploaded file is BLANK!")
    else:
        st.success("🎯 File Uploaded Successfully!")
        
        # 2. Conversion: Streamlit file stream ko text formats mein badalna
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        
        # 3. Processing Records
        records = list(SeqIO.parse(stringio, "fasta"))
        
        if len(records) == 0:
            st.warning("⚠️ Could not find valid FASTA headers (e.g., >Gene_ID). Processing raw sequence text instead.")
            # If no header, make a dummy record from raw file text
            raw_text = uploaded_file.getvalue().decode("utf-8").strip().upper()
            records = [Seq(raw_text)]
            is_fasta = False
        else:
            is_fasta = True

        # --- CORE ENGINE EXECUTION (Your logic adapted for UI) ---
        st.write("---")
        st.write(f"### 📊 Execution Results ({choice}):")

        for idx, record in enumerate(records):
            # Extract sequence and ID based on file structure
            seq_id = record.id if is_fasta else f"Raw_Sequence_{idx+1}"
            sequence_str = str(record.seq).upper().strip() if is_fasta else str(record).upper().strip()
            bio_seq = Seq(sequence_str)
            
            st.info(f"🧬 **Target:** {seq_id}")

            # 1. DNA Length Calculator
            if choice == "DNA Length Calculator":
                if not all(base in "ATCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Non-DNA characters detected.")
                else:
                    st.metric(label="Total Nucleotide Count", value=f"{len(sequence_str)} bp")

            # 2. DNA Slicing
            elif choice == "DNA Slicing (Codon Chopper)":
                if not all(base in "ATCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Non-DNA characters detected.")
                else:
                    chop = [sequence_str[i:i+3] for i in range(0, len(sequence_str), 3)]
                    st.write("**Codon Segments Matrix:**")
                    st.code(f"{chop}")

            # 3. DNA Transcription
            elif choice == "Perform DNA Transcription":
                if not all(base in "ATCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Non-DNA characters detected.")
                else:
                    st.write("**Resulting mRNA Strand (5' -> 3'):**")
                    st.code(f"{bio_seq.transcribe()}")

            # 4. DNA Replication
            elif choice == "DNA Replication (Complement)":
                if not all(base in "ATCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Non-DNA characters detected.")
                else:
                    st.write("**Complementary Template Strand (3' -> 5'):**")
                    st.code(f"{bio_seq.complement()}")

            # 5. Reverse Transcription
            elif choice == "Reverse Transcription":
                if not all(base in "AUCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Sequence must be RNA (A, U, C, G).")
                else:
                    st.write("**Back Transcribed Coding DNA Strand:**")
                    st.code(f"{bio_seq.back_transcribe()}")

            # 6. RNA Translation
            elif choice == "Perform RNA Translation":
                if not all(base in "AUCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Sequence must be RNA (A, U, C, G) for translation.")
                else:
                    st.write("**Synthesized Amino Acid Chain (Protein):**")
                    st.code(f"{bio_seq.translate()}")

            # 7. GC Content Calculator
            elif choice == "GC Content Calculator":
                if not all(base in "ATCG" for base in sequence_str):
                    st.error("❌ INVALID SEQUENCE: Non-DNA characters detected.")
                else:
                    g_count = sequence_str.count("G")
                    c_count = sequence_str.count("C")
                    gc_percent = (g_count + c_count) / len(sequence_str) * 100
                    st.metric(label="GC Ratio", value=f"{gc_percent:.2f} %")
                    st.progress(gc_percent / 100) # Cool visual loader bar

else:
    st.info("💡 Awaiting file upload. Drop your .fasta data file to trigger the computational engine.")

info = st.caption("*ZER0v0.3.9 is underdeveloping tool and can make mistakes. Sorry for inconvenience, if any. ")
