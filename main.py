import tkinter as tk
import json

# Görevleri kaydeden fonksiyon
def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)  # Görevleri tasks.json dosyasına yazar

# Görevleri yükleyen fonksiyon
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)  # tasks.json dosyasındaki görevleri okur
    except FileNotFoundError:
        return []  # Dosya bulunamazsa boş bir liste döndürür

# Görevleri önem sırasına göre otomatik olarak sıralayan fonksiyon
def sort_tasks_by_priority():
    tasks.sort(key=lambda x: x.get("Önem Sırası", ""))  # Görevleri öncelik sırasına göre otomatik olarak sıralar
    listbox_tasks.delete(0, tk.END)  # Listbox'taki görevleri temizler
    for task in tasks:
        task_display = f"{task.get('Görev Gir')} - {task.get('Ayrıntılar', '')} - {task.get('Önem Sırası', '')}"
        listbox_tasks.insert(tk.END, task_display)  # Görevleri Listbox'a ekler

# Görev ekleme fonksiyonu
def add_task():
    task_name = entry_task.get()  # Giriş kutusundan görev adı alınır
    task_details = entry_details.get()  # Giriş kutusundan görev ayrıntıları alınır
    task_priority = entry_priority.get()  # Giriş kutusundan görev önceliği alınır

    if not task_name or not task_details or not task_priority:
        # Eğer herhangi bir giriş alanı boşsa, hata mesajı verilir
        error_window = tk.Toplevel(root)
        error_window.title("Hata")
        label_error = tk.Label(error_window, text="Lütfen tüm alanları doldurun.", font=("Arial", 12))
        label_error.pack(padx=20, pady=20)
    else:
        new_task = {
            "Görev Gir": task_name,
            "Ayrıntılar": task_details if task_details else "",  # Boşsa varsayılan değer olarak boş string atanır
            "Önem Sırası": task_priority if task_priority else "",  # Boşsa varsayılan değer olarak boş string atanır
            "tamamlandi": False  # Yeni görevler için tamamlandi anahtarı eklendi
        }

        tasks.append(new_task)  # Görev listesine yeni görev eklenir
        sort_tasks_by_priority()  # Görevleri önem sırasına göre otomatik olarak sıralar
        entry_task.delete(0, tk.END)  # Görev giriş kutusunu temizler
        entry_details.delete(0, tk.END)  # Ayrıntı giriş kutusunu temizler
        entry_priority.delete(0, tk.END)  # Öncelik giriş kutusunu temizler
        save_tasks()  # Görevleri kaydeder

        # Yeni pencere oluşturulur ve görev eklendi mesajı gösterilir
        add_window = tk.Toplevel(root)
        add_window.title("Görev Eklendi")
        label_added = tk.Label(add_window, text=f"Görev '{task_name}' eklendi.", font=("Arial", 12))
        label_added.pack(padx=20, pady=20)

# Görev silme fonksiyonu
def delete_task():
    try:
        def on_confirm_delete():
            delete_window.destroy()
            task_index = listbox_tasks.curselection()[0]  # Seçili görevin indeksi alınır
            deleted_task_name = tasks[task_index]["Görev Gir"]  # Silinen görevin adı alınır
            listbox_tasks.delete(task_index)  # Listbox'tan görev silinir
            del tasks[task_index]  # Görev listesinden görev silinir
            save_tasks()  # Görevleri kaydeder

            # Yeni pencere oluşturulur ve görev silindi mesajı gösterilir
            delete_success_window = tk.Toplevel(root)
            delete_success_window.title("Görev Silindi")
            label_deleted_success = tk.Label(delete_success_window, text=f"Görev '{deleted_task_name}' silindi.", font=("Arial", 12))
            label_deleted_success.pack(padx=20, pady=20)

        def on_cancel_delete():
            delete_window.destroy()

        task_index = listbox_tasks.curselection()[0]  # Seçili görevin indeksi alınır
        deleted_task_name = tasks[task_index]["Görev Gir"]  # Silinecek görevin adı alınır

        delete_window = tk.Toplevel(root)
        delete_window.title("Görevi Sil")
        label_confirm_delete = tk.Label(delete_window, text=f"Görev '{deleted_task_name}' silmek istediğinizden emin misiniz?", font=("Arial", 12))
        label_confirm_delete.pack(padx=20, pady=20)

        confirm_button = tk.Button(delete_window, text="Evet", command=on_confirm_delete, bg="lightgreen")
        confirm_button.pack(side=tk.LEFT, padx=10, pady=10)

        cancel_button = tk.Button(delete_window, text="Hayır", command=on_cancel_delete, bg="lightcoral")
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

    except IndexError:
        pass

# Görev tamamlama fonksiyonu
def complete_task():
    try:
        task_index = listbox_tasks.curselection()[0]  # Seçili görevin indeksi alınır
        completed_task_name = tasks[task_index]["Görev Gir"]  # Tamamlanan görevin adı alınır
        tasks[task_index]["tamamlandi"] = True  # Görev "tamamlandi" olarak işaretlenir
        listbox_tasks.itemconfig(task_index, fg="green")  # Görev gri renge dönüştürülür
        save_tasks()  # Görevleri kaydeder

        # Yeni pencere oluşturulur ve görev tamamlandı mesajı gösterilir
        complete_window = tk.Toplevel(root)
        complete_window.title("Görev Tamamlandı")
        label_completed = tk.Label(complete_window, text=f"Görev '{completed_task_name}' tamamlandı.", font=("Arial", 12))
        label_completed.pack(padx=20, pady=20)

    except IndexError:
        pass

# Bütün görevleri silme fonksiyonu
def delete_all_tasks():
    def on_confirm_delete_all():
        delete_all_window.destroy()
        listbox_tasks.delete(0, tk.END)  # Listbox'taki bütün görevleri siler
        tasks.clear()  # Görev listesini temizler
        save_tasks()  # Görevleri kaydeder

        # Yeni pencere oluşturulur ve görevler silindi mesajı gösterilir
        delete_success_window = tk.Toplevel(root)
        delete_success_window.title("Tüm Görevler Silindi")
        label_delete_all_success = tk.Label(delete_success_window, text="Tüm görevler silindi.", font=("Arial", 12))
        label_delete_all_success.pack(padx=20, pady=20)

    def on_cancel_delete_all():
        delete_all_window.destroy()

    delete_all_window = tk.Toplevel(root)
    delete_all_window.title("Tüm Görevleri Sil")
    label_confirm_delete_all = tk.Label(delete_all_window, text="Tüm görevleri silmek istediğinizden emin misiniz?", font=("Arial", 12))
    label_confirm_delete_all.pack(padx=20, pady=20)

    confirm_button_all = tk.Button(delete_all_window, text="Evet", command=on_confirm_delete_all, bg="lightgreen")
    confirm_button_all.pack(side=tk.LEFT, padx=10, pady=10)

    cancel_button_all = tk.Button(delete_all_window, text="Hayır", command=on_cancel_delete_all, bg="lightcoral")
    cancel_button_all.pack(side=tk.RIGHT, padx=10, pady=10)

# Arayüz oluşturulması
root = tk.Tk()
root.title("To-Do List")  # Pencere başlığı ayarlanır

# Frame oluşturulur ve kök pencere içine yerleştirilir
frame_tasks = tk.Frame(root)
frame_tasks.pack()

# Görev adı girişi için Entry oluşturulur, üzerine etiket eklenir ve kök pencere içine yerleştirilir
label_task = tk.Label(root, text="Görev Gir")
label_task.pack()
entry_task = tk.Entry(root, width=100, font=("Arial", 12))  # Yazı fontunu büyüt
entry_task.pack()

# Görev ayrıntıları girişi için Entry oluşturulur, üzerine etiket eklenir ve kök pencere içine yerleştirilir
label_details = tk.Label(root, text="Ayrıntılar")
label_details.pack()
entry_details = tk.Entry(root, width=100, font=("Arial", 12))  # Yazı fontunu büyüt
entry_details.pack()

# Görev önceliği girişi için Entry oluşturulur, üzerine etiket eklenir ve kök pencere içine yerleştirilir
label_priority = tk.Label(root, text="Önem Sırası")
label_priority.pack()
entry_priority = tk.Entry(root, width=100, font=("Arial", 12))  # Yazı fontunu büyüt
entry_priority.pack()

# Listbox oluşturur, frame_tasks içine yerleştirilir ve özellikleri belirlenir
listbox_tasks = tk.Listbox(frame_tasks, height=20, width=100, borderwidth=4, font=("Arial", 12))  # Yazı fontunu büyüt
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

# Scrollbar oluşturur, frame_tasks içine sağ tarafa yerleştirilir ve fill=BOTH ile boyutlandırma ayarlanır
scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.BOTH)

# Listbox ve Scrollbar birbiriyle bağlanır
listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

# Görev ekleme butonu oluşturur, genişlik ve komutu belirtir, kök pencere içine yerleştirilir
button_add_task = tk.Button(root, text="Görev Ekle", width=135, command=add_task, bg="lightgreen")
button_add_task.pack()

# Görev silme butonu oluşturur, genişlik ve komutu belirtir, kök pencere içine yerleştirilir
button_delete_task = tk.Button(root, text="Görevi Sil", width=135, command=delete_task, bg="lightgreen")
button_delete_task.pack()

# Görev tamamlama butonu oluşturur, genişlik ve komutu belirtir, kök pencere içine yerleştirilir
button_complete_task = tk.Button(root, text="Görevi Bitir", width=135, command=complete_task, bg="lightgreen")
button_complete_task.pack()

# Görevleri silme butonu oluşturur, genişlik ve komutu belirtir, kök pencere içine yerleştirilir
button_delete_all_tasks = tk.Button(root, text="Tüm Görevleri Sil", width=135, command=delete_all_tasks, bg="lightgreen")
button_delete_all_tasks.pack()

tasks = load_tasks()  # Görevleri yükler
for task in tasks:
    task_display = f"{task.get('Görev Gir')} - {task.get('Ayrıntılar', '')} - {task.get('Önem Sırası', '')}"
    listbox_tasks.insert(tk.END, task_display)  # Görevleri Listbox'a ekler

    if 'tamamlandi' in task and task["tamamlandi"]:  # 'tamamlandi' anahtarı var mı ve değeri True mu kontrol edilir
        listbox_tasks.itemconfig(tasks.index(task), fg="green")  # Tamamlanmış görevleri gri renge dönüştürür

root.mainloop()
