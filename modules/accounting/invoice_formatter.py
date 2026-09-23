class InvoiceFormatter:
    @staticmethod
    def format_invoice_text(invoice_number: str, customer_name: str, customer_phone: str, item_name: str, item_type: str, details_table: list, total_amount: float, paid_amount: float):
        remaining = total_amount - paid_amount
        
        output = []
        output.append("=== فاتورة المبرزي للبصريات والسمعيات ===")
        output.append(f"رقم الفاتورة: {invoice_number}")
        output.append(f"اسم العميل: {customer_name}")
        output.append(f"رقم الجوال: {customer_phone}")
        output.append("-" * 35)
        output.append(f"اسم الصنف: {item_name}")
        output.append(f"نوع الصنف: {item_type}")
        output.append("=" * 35)
        output.append(f"{'البيان / التفاصيل':<20} | {'المبلغ':<10}")
        output.append("-" * 35)
        
        for item in details_table:
            output.append(f"{item.get('desc', ''):<20} | {item.get('price', 0):<10}")
            
        output.append("=" * 35)
        output.append(f"الإجمالي: {total_amount}")
        output.append(f"المدفوع: {paid_amount}")
        output.append(f"المتبقي: {remaining}")
        output.append("===================================")
        
        return "\n".join(output)
