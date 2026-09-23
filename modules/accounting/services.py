from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Customer, Invoice, Payment, Expense

class AccountingService:
    @staticmethod
    def create_customer(db: Session, name: str, phone: str = None, customer_type: str = 'regular'):
        customer = Customer(name=name, phone=phone, customer_type=customer_type)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def create_invoice(db: Session, customer_id: int, invoice_number: str, total_amount: float, profit: float = 0.0, item_type: str = 'optics', details: str = None, invoice_photo_path: str = None):
        invoice = Invoice(
            customer_id=customer_id,
            invoice_number=invoice_number,
            total_amount=total_amount,
            paid_amount=0.0,
            remaining_amount=total_amount,
            profit=profit,
            item_type=item_type,
            details=details,
            invoice_photo_path=invoice_photo_path
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    @staticmethod
    def add_payment(db: Session, customer_id: int, amount: float, invoice_id: int = None, receipt_number: str = None, payment_method: str = 'cash'):
        payment = Payment(
            customer_id=customer_id,
            invoice_id=invoice_id,
            receipt_number=receipt_number,
            amount=amount,
            payment_method=payment_method
        )
        db.add(payment)
        
        if invoice_id:
            invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
            if invoice:
                invoice.paid_amount += amount
                invoice.remaining_amount = max(0.0, invoice.total_amount - invoice.paid_amount)
        
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def add_expense(db: Session, title: str, amount: float, category: str = 'general'):
        expense = Expense(title=title, amount=amount, category=category)
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    @staticmethod
    def get_financial_report(db: Session):
        total_sales = db.query(func.sum(Invoice.total_amount)).scalar() or 0.0
        total_profit = db.query(func.sum(Invoice.profit)).scalar() or 0.0
        total_expenses = db.query(func.sum(Expense.amount)).scalar() or 0.0
        total_paid = db.query(func.sum(Payment.amount)).scalar() or 0.0
        
        net_profit = total_profit - total_expenses
        net_margin = (net_profit / total_sales * 100) if total_sales > 0 else 0.0

        return {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "total_expenses": total_expenses,
            "total_paid": total_paid,
            "net_profit": net_profit,
            "net_margin": round(net_margin, 2)
        }
