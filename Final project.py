import tkinter as tk
from tkinter import filedialog, messagebox
from Bio import SeqIO
from io import StringIO
from Bio.Seq import Seq




def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("FASTA Files", "*.fasta")])
    if file_path:
        fasta_text.delete(1.0, tk.END)  # Clear the text area
        with open(file_path, "r") as fasta_file:
            # insert from end of old text(zerooo)
            fasta_text.insert(tk.END, fasta_file.read())


def read_record():
    fasta_data = fasta_text.get(1.0, tk.END)
    record_id = entry_record_id.get()
    if record_id:
        fasta_file = StringIO(fasta_data)
        records = SeqIO.parse(fasta_file, "fasta")
        for record in records:
            if record.id == record_id or record.name == record_id:
                display_record(record)
                break
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Record not found.")


def modify_record():
    fasta_file = filedialog.askopenfilename(title="Select FASTA file")
    if fasta_file:
        record_id = entry_record_id.get()
        description = modify_description_entry.get()
        sequence = modify_sequence_entry.get()

        records = list(SeqIO.parse(fasta_file, "fasta"))
        for record in records:
            if record.id == record_id:
                record.description = description
                record.seq = Seq(sequence)
        output_file = filedialog.asksaveasfilename(defaultextension=".fasta", title="Save modified FASTA file")
        if output_file:
            SeqIO.write(records, output_file, "fasta")
            tk.messagebox.showinfo("Success", "Records modified and saved successfully!")


def display_record(record):
    gc_content = (record.seq.count('G') + record.seq.count('C')) / len(record.seq) * 100
    reverse_complement = record.seq.reverse_complement()
    rna = record.seq.transcribe()

    # Clear both output areas
    id_output_text.delete(1.0, tk.END)  # Changed from left_output_text to id_output_text
    GC_output_text.delete(1.0, tk.END)
    R_output_text.delete(1.0, tk.END)

    # Display general information on the left side
    id_output_text.insert(tk.END, f"ID: {record.id}\n")
    id_output_text.insert(tk.END, f"Name: {record.name}\n")
    id_output_text.insert(tk.END, f"Description: {record.description}\n")
    id_output_text.insert(tk.END, f"Sequence: {record.seq}\n")

    # Display specific details on the right side
    GC_output_text.insert(tk.END, f"GC Content: {gc_content:.2f}%\n")
    R_output_text.insert(tk.END, f"Reverse Complement: {reverse_complement}\n")
    R_output_text.insert(tk.END, f"RNA: {rna}\n")



root = tk.Tk()
root.title("Bioinformatics Tool")
root.geometry("1200x600")  # Adjust the window size as needed
root.configure(bg="#F2EBDC")  # Set the background color of the root window

# Left Frame for general information
left_frame = tk.Frame(root, bg="#F2EBDC")  # Set the background color of the left frame
left_frame.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8)

# Right Frame for specific details
GC_frame = tk.Frame(root, bg="#F2EBDC")  # Set the background color of the GC frame
GC_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.4)

# RNA Frame for specific details
R_frame = tk.Frame(root, bg="#F2EBDC")  # Set the background color of the R frame
R_frame.place(relx=0.55, rely=0.3, relwidth=0.4, relheight=0.4)

# Modify Frame
modify_frame = tk.Frame(root, bg="#F2EBDC")  # Set the background color of the modify frame
modify_frame.place(relx=0.55, rely=0.6, relwidth=0.4, relheight=0.4)

# Upload area
upload_label = tk.Label(left_frame, text="FASTA File Content", bg="#F2EBDC")  # Set the background color of the label
upload_label.pack(pady=(20, 5))
fasta_text = tk.Text(left_frame, height=10, width=50, bg="white")  # Set the background color of the text area
fasta_text.pack()
upload_button = tk.Button(left_frame, text="Upload FASTA File", command=upload_file, bg="#F2EBDC")  # Set the background color of the button
upload_button.pack(pady=(5, 10))

# Entry field to input record ID
entry_record_id = tk.Entry(left_frame, bg="white")  # Set the background color of the entry field
entry_record_id.pack()
read_button = tk.Button(left_frame, text="Read Record", command=read_record, bg="yellow", relief=tk.RAISED, bd=3)  # Set the background color of the button
read_button.pack(pady=(5, 10))

# Modify Frame
modify_description_label = tk.Label(modify_frame, text="New Description:", bg="#F2EBDC")  # Set the background color of the label
modify_description_label.pack(pady=(10, 5))
modify_description_entry = tk.Entry(modify_frame, width=50, bg="white")  # Set the background color of the entry field
modify_description_entry.pack()

modify_sequence_label = tk.Label(modify_frame, text="New Sequence:", bg="#F2EBDC")  # Set the background color of the label
modify_sequence_label.pack(pady=(5, 5))
modify_sequence_entry = tk.Entry(modify_frame, width=50, bg="white")  # Set the background color of the entry field
modify_sequence_entry.pack()

modify_button = tk.Button(modify_frame, text="Modify Record", command=modify_record, bg="#F2EBDC")  # Set the background color of the button
modify_button.pack(pady=(5, 10))

# Output area for general information
id_output_text = tk.Text(left_frame, height=20, width=60, bg="white")  # Set the background color of the text area
id_output_text.pack()

# Output area for specific details
GC_output_text = tk.Text(GC_frame, height=5, width=30, bg="white")  # Set the background color of the text area
GC_output_text.pack()

# Output area for id and name information
R_output_text = tk.Text(R_frame, height=10, width=60, bg="white")  # Set the background color of the text area
R_output_text.pack()

# Adjusting the position of the GC frame to align GC Content box more with center right
GC_frame.grid_propagate(False)
GC_frame.grid_rowconfigure(0, weight=1)
GC_frame.grid_columnconfigure(0, weight=1)

# Adjusting the position of the R frame to align RNA box more with center right
R_frame.grid_propagate(False)
R_frame.grid_rowconfigure(0, weight=1)
R_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
