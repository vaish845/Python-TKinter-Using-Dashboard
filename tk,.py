import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Global dataframe
df = None

# ----------------------------
# Upload CSV File
# ----------------------------
def upload_file():
    global df

    file_path = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv")])

    if file_path:
        df = pd.read_csv(file_path)
        update_kpis()
        load_columns()


# ----------------------------
# KPI Cards Update
# ----------------------------
def update_kpis():
    global df

    if df is None:
        return

    total_rows = len(df)
    total_cols = len(df.columns)
    numeric_cols = len(df.select_dtypes(include='number').columns)
    missing = df.isnull().sum().sum()

    kpi_rows.config(text=f"Rows\n{total_rows}")
    kpi_cols.config(text=f"Columns\n{total_cols}")
    kpi_numeric.config(text=f"Numeric\n{numeric_cols}")
    kpi_missing.config(text=f"Missing\n{missing}")


# ----------------------------
# Load Columns for dropdown
# ----------------------------
def load_columns():
    columns = list(df.columns)

    x_combo['values'] = columns
    y_combo['values'] = columns
    filter_combo['values'] = columns


# ----------------------------
# Apply Filter
# ----------------------------
def apply_filter():
    global df

    if df is None:
        return

    column = filter_combo.get()
    value = filter_entry.get()

    if column and value:
        filtered = df[df[column].astype(str) == value]
        plot_chart(filtered)
    else:
        plot_chart(df)


# ----------------------------
# Plot Charts
# ----------------------------
def plot_chart(data):

    chart = chart_combo.get()
    x = x_combo.get()
    y = y_combo.get()

    if not x:
        return

    plt.figure(figsize=(7,5))

    if chart == "Bar":
        sns.barplot(x=data[x], y=data[y])

    elif chart == "Line":
        plt.plot(data[x], data[y])

    elif chart == "Scatter":
        plt.scatter(data[x], data[y])

    elif chart == "Histogram":
        plt.hist(data[x])

    elif chart == "Box":
        sns.boxplot(x=data[x], y=data[y])

    elif chart == "Heatmap":
        sns.heatmap(data.corr(), annot=True)

    elif chart == "Violin":
        sns.violinplot(x=data[x], y=data[y])

    elif chart == "Density":
        sns.kdeplot(data[x])

    elif chart == "Area":
        plt.fill_between(range(len(data[y])), data[y])

    elif chart == "Pie":
        data.groupby(x)[y].sum().plot.pie(autopct="%1.1f%%")

    plt.title(chart + " Chart")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ----------------------------
# Simple Chatbot
# ----------------------------
def chatbot():

    question = chat_entry.get().lower()

    if df is None:
        chat_box.insert(tk.END,"Upload dataset first\n")
        return

    if "rows" in question:
        answer = f"Total rows: {len(df)}"

    elif "columns" in question:
        answer = f"Total columns: {len(df.columns)}"

    elif "average" in question:
        answer = str(df.mean(numeric_only=True))

    elif "missing" in question:
        answer = f"Missing values: {df.isnull().sum().sum()}"

    else:
        answer = "Ask about rows, columns, average, or missing values."

    chat_box.insert(tk.END,"You: "+question+"\n")
    chat_box.insert(tk.END,"Bot: "+answer+"\n\n")

    chat_entry.delete(0,tk.END)


# ============================
# Main Window
# ============================
root = tk.Tk()
root.title("AI Data Analytics Dashboard")
root.geometry("1200x800")
root.configure(bg="#1e1e2f")


# ----------------------------
# Upload Button
# ----------------------------
upload_btn = tk.Button(root,
                       text="Upload CSV",
                       command=upload_file,
                       bg="#4CAF50",
                       fg="white",
                       font=("Arial",12,"bold"))

upload_btn.pack(pady=10)


# ----------------------------
# KPI Cards
# ----------------------------
kpi_frame = tk.Frame(root,bg="#1e1e2f")
kpi_frame.pack()

kpi_rows = tk.Label(kpi_frame,text="Rows",bg="#ff6b6b",fg="white",width=20,height=3,font=("Arial",10,"bold"))
kpi_rows.grid(row=0,column=0,padx=10,pady=5)

kpi_cols = tk.Label(kpi_frame,text="Columns",bg="#4ecdc4",fg="white",width=20,height=3,font=("Arial",10,"bold"))
kpi_cols.grid(row=0,column=1,padx=10,pady=5)

kpi_numeric = tk.Label(kpi_frame,text="Numeric",bg="#ffa502",fg="white",width=20,height=3,font=("Arial",10,"bold"))
kpi_numeric.grid(row=0,column=2,padx=10,pady=5)

kpi_missing = tk.Label(kpi_frame,text="Missing",bg="#6c5ce7",fg="white",width=20,height=3,font=("Arial",10,"bold"))
kpi_missing.grid(row=0,column=3,padx=10,pady=5)


# ----------------------------
# Filter Section
# ----------------------------
filter_frame = tk.Frame(root,bg="#1e1e2f")
filter_frame.pack(pady=20)

tk.Label(filter_frame,text="Filter Column",bg="#1e1e2f",fg="white").grid(row=0,column=0,padx=5)
filter_combo = ttk.Combobox(filter_frame,width=15)
filter_combo.grid(row=0,column=1)

filter_entry = tk.Entry(filter_frame,width=15)
filter_entry.grid(row=0,column=2,padx=5)

filter_btn = tk.Button(filter_frame,text="Apply Filter",command=apply_filter)
filter_btn.grid(row=0,column=3,padx=5)


# ----------------------------
# Axis Selection
# ----------------------------
tk.Label(filter_frame,text="X Axis",bg="#1e1e2f",fg="white").grid(row=1,column=0)

x_combo = ttk.Combobox(filter_frame,width=15)
x_combo.grid(row=1,column=1)

tk.Label(filter_frame,text="Y Axis",bg="#1e1e2f",fg="white").grid(row=1,column=2)

y_combo = ttk.Combobox(filter_frame,width=15)
y_combo.grid(row=1,column=3)


# ----------------------------
# Chart Selection
# ----------------------------
chart_combo = ttk.Combobox(filter_frame,width=15)

chart_combo['values'] = [
"Bar","Line","Scatter","Histogram","Box",
"Heatmap","Violin","Density","Area","Pie"
]

chart_combo.grid(row=2,column=1,pady=10)

plot_btn = tk.Button(filter_frame,text="Plot Chart",
                     command=lambda: plot_chart(df))
plot_btn.grid(row=2,column=2)


# ----------------------------
# Chatbot Section
# ----------------------------
chat_frame = tk.Frame(root,bg="#1e1e2f")
chat_frame.pack(pady=20)

chat_box = tk.Text(chat_frame,height=10,width=80)
chat_box.grid(row=0,column=0,columnspan=2)

chat_entry = tk.Entry(chat_frame,width=60)
chat_entry.grid(row=1,column=0,pady=5)

chat_btn = tk.Button(chat_frame,text="Ask Bot",command=chatbot)
chat_btn.grid(row=1,column=1)


root.mainloop()