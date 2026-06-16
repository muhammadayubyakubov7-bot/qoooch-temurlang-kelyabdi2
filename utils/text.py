def generate_text(data):
    """Confirmation uchun text generator"""
    text = f"""
<b>FIO</b>: {data.get('fio')}
<b>YOSH</b>: {data.get('age')}
<b>KURS</b>: {data.get('course')}
<b>TELEFON RAQAM</b>: {data.get('contact')}
<b>O'QISH VAQTI</b>: {data.get('study_time')}

"""
    return text
