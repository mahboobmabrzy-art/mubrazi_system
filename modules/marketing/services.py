import os
from telegram import Bot
from database.models import MarketingCampaign
from sqlalchemy.orm import Session

class MarketingService:
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)

    async def send_broadcast(self, db: Session, title: str, content: str, chat_ids: list):
        """
        إرسال عرض تسويقي لجميع العملاء المسجلين عبر Telegram.
        """
        # حفظ الحملة في قاعدة البيانات
        campaign = MarketingCampaign(title=title, content=content, target_audience='all')
        db.add(campaign)
        db.commit()

        results = {"success": 0, "failed": 0}
        for chat_id in chat_ids:
            try:
                await self.bot.send_message(chat_id=chat_id, text=f"📢 {title}\n\n{content}")
                results["success"] += 1
            except Exception as e:
                print(f"فشل الإرسال إلى {chat_id}: {e}")
                results["failed"] += 1
        
        return results

    @staticmethod
    def generate_offer_text(product_type: str, discount: int):
        """
        توليد نص عرض تسويقي تلقائي.
        """
        if product_type == 'optics':
            return f"احصل على خصم {discount}% على جميع إطارات النظارات الطبية والشمسية لدى المبرزي للبصريات!"
        elif product_type == 'audiology':
            return f"عرض خاص: فحص سمع مجاني وخصم {discount}% على أحدث السماعات الطبية لدى المبرزي للسمعيات!"
        return f"عروض حصرية من المبرزي للبصريات والسمعيات بخصم يصل إلى {discount}%!"
