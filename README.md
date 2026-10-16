# Python shaxmat

Pygame orqali bot bilan yoki bitta kompyuterda ikki kishi o'ynaydigan shaxmat.
Python 3.10 yoki yangiroq versiya kerak.

Grafika uchun `pygame-ce` ishlatiladi; kodda u `import pygame` orqali yuklanadi.
Bu paket Python 3.14 uchun ham tayyor macOS paketlarini taqdim etadi.

## Ishga tushirish

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows'da muhitni faollashtirish: `.venv\Scripts\activate`.

Oldin oddiy `pygame` o'rnatilgan bo'lsa, `pygame-ce` bilan to'qnashmasligi uchun
avval `python -m pip uninstall pygame` buyrug'ini bajaring.

Donani va keyin boradigan katakni bosing. Mumkin bo'lgan yurishlar yashil
belgilanadi. Piyoda oxirgi qatorga yetganda yangi donani tanlang.

Boshlang'ich menyuda **Bot bilan** yoki **Duo (2 kishi)** rejimini tanlang.
Bot rejimida oq/qora tomonni va darajani tanlash mumkin. Qora tanlansa,
doska aylanadi va bot birinchi yuradi.

- **Oson**: tasodifiy qonuniy yurishlar.
- **O'rtacha**: ikki yarim yurishgacha qidiruv, taxminan 0.3 soniya vaqt chegarasi.
- **Qiyin**: to'rt yarim yurishgacha qidiruv, taxminan 1 soniya vaqt chegarasi.

Bot oddiy ichki algoritm; Stockfish yoki qo'shimcha dastur kerak emas.
Darajalar Elo reytingini anglatmaydi.

- `R`: yangi o'yin.
- `U`: oxirgi yurishni qaytarish.
- Bot rejimida `U` sizning oxirgi yurishingiz va bot javobini qaytaradi;
  bot o'ylayotgan paytda sizning yurishingizni qaytaradi.
- `M`: rejim va darajani tanlash menyusiga qaytish.
- `Esc`: tanlovni bekor qilish.

Rokirovka, en passant, shoh, mot va durang qoidalari `python-chess` orqali
tekshiriladi. Talab qilinishi mumkin bo'lgan uch karra takrorlash va 50 yurish
duranglari avtomatik qabul qilinadi. Onlayn o'yin yo'q.
Shaxmat belgilarini qo'llaydigan tizim shrifti bo'lmasa, donalar harflar bilan ko'rsatiladi.
