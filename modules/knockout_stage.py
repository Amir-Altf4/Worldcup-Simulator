class KnockoutStage:
    """نماینده یک دور از مرحله حذفی جام جهانی.

    این کلاس مجموعه‌ای از مسابقات حذفی یک دور (مثلاً یک‌هشتم نهایی
    یا فینال) را مدیریت و نتایج آن را نمایش می‌دهد.
    """

    def __init__(self, matches, round_name):
        """یک دور حذفی جدید ایجاد می‌کند.

        Args:
            matches (list[Match]): لیست مسابقات این دور.
            round_name (str): نام دور (مثلاً «Quarterfinals»).
        """
        self.matches = matches
        self.round_name = round_name
    
    def play_round(self):
        """تمام مسابقات این دور حذفی را برگزار می‌کند.

        Returns:
            None
        """
        
        # اجرای تمام مسابقات این مرحله
        for match in self.matches:
            match.play()
            
    def get_winners(self):
        """برندگان تمام مسابقات این دور را برمی‌گرداند.

        Returns:
            list[Team]: لیست تیم‌های برنده به ترتیب مسابقات.
        """
        
        # لیست تیم‌های صعودکننده
        winners = []
        
        # اضافه کردن برنده هر مسابقه به لیست
        for match in self.matches:
            winners.append(match.winner)
            
        return winners
    
    def display_results(self):
        """نتایج مسابقات این دور را در خروجی چاپ می‌کند.
        """
        print(f"==={self.round_name}===")
        
        # نمایش نتیجه هر مسابقه
        for match in self.matches:
            
            # اگر تیم اول برنده شده باشد
            if match.team1 == match.winner:
                print(f"{match.winner.name} {match.goals1} , {match.goals2} {match.team2.name} => winner: {match.winner.name}")
                
            # اگر تیم دوم برنده شده باشد
            elif match.team2 == match.winner:
                print(f"{match.winner.name} {match.goals2} , {match.goals1} {match.team1.name} => winner: {match.winner.name}")
