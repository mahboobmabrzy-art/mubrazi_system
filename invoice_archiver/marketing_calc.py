# حاسبة عروض البصريات والسمعيات
product = input("أدخل اسم المنتج (مثلاً: نظارة إيطالية): ")
cost = float(input("سعر التكلفة: "))
price = float(input("سعر البيع المقترح: "))

profit = price - cost
discount_pct = 15  # نسبة خصم تسويقية مقترحة
offer_price = price * (1 - discount_pct/100)

print("\n--- تقرير المحاسب المسوق ---")
print(f"الربح الصافي بدون خصم: {profit}")
print(f"السعر بعد خصم {discount_pct}% هو: {offer_price}")
print("\n--- نص إعلاني مقترح لمشاركتة ---")
print(f"🔥 عرض خاص في صنعاء! احصل على {product} الآن بسعر {offer_price} بدلاً من {price}. الأناقة والدقة في مكان واحد!")

