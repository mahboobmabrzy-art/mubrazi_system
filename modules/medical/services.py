class MedicalService:
    @staticmethod
    def format_optics_prescription(sph_r: float, cyl_r: float, axis_r: int, sph_l: float, cyl_l: float, axis_l: int, pd: float, add_val: float = 0.0) -> str:
        """تنسيق مقاسات فحص النظر للبصريات"""
        prescription = (
            f"فحص النظر:\n"
            f"العين اليمنى (R): SPH: {sph_r}, CYL: {cyl_r}, AXIS: {axis_r}°\n"
            f"العين اليسرى (L): SPH: {sph_l}, CYL: {cyl_l}, AXIS: {axis_l}°\n"
            f"البعد بين الحدقتين (PD): {pd} mm | الإضافة (ADD): {add_val}"
        )
        return prescription

    @staticmethod
    def format_audiology_details(brand: str, model: str, serial_number: str, ear_side: str, warranty_years: int = 1) -> str:
        """تنسيق تفاصيل المعينات والفرع السمعي"""
        details = (
            f"معينة سمعية:\n"
            f"الماركة: {brand} | الموديل: {model}\n"
            f"الجهة: {ear_side} | الرقم التسلسلي: {serial_number}\n"
            f"الضمان: {warranty_years} سنة"
        )
        return details
