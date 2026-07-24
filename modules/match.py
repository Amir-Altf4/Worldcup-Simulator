class Match:
      """نماینده یک مسابقه بین دو تیم.

     این کلاس دو تیم را به هم متصل می‌کند، مسابقه را اجرا می‌کند
      و نتیجه را در آمار تیم‌ها ثبت می‌کند.
      """

      def __init__(self, team1, team2, is_knockout = False):
        """یک مسابقه جدید بین دو تیم ایجاد می‌کند.

        Args:
            team1 (Team): تیم اول.
            team2 (Team): تیم دوم.
            is_knockout (bool): اگر True باشد، مسابقه با قوانین
                مرحله حذفی برگزار می‌شود.
        """
        self.team1 = team1
        self.team2 = team2
        
        # مشخص کردن نوع مسابقه (گروهی یا حذفی)
        self.is_knockout = is_knockout
        self.goals1 = 0
        self.goals2 = 0
        self.winner = None
    
      def play(self):
        """مسابقه را برگزار می‌کند و آمار تیم‌ها را به‌روزرسانی می‌کند.

        نتیجه مسابقه را شبیه‌سازی کرده، گل‌ها و امتیازات (در مرحله
        گروهی) را به آمار هر دو تیم اضافه می‌کند.

        Returns:
            None
        """
        # شبیه‌سازی مسابقه و دریافت نتیجه
        self.goals1, self.goals2, self.winner = self.team1.simulate_match(self.team2, self.is_knockout)
         
         # آمار گل‌ها برای هر دو تیم آپدیت می‌شود
        self.team1.goals_for += self.goals1
        self.team2.goals_for += self.goals2
        self.team1.goals_against += self.goals2
        self.team2.goals_against += self.goals1

         # امتیاز فقط در مرحله گروهی داده می‌شود — حذفی امتیاز ندارد
        if not self.is_knockout:
            
            # برد تیم اول
            if self.goals1 > self.goals2:
                self.team1.points += 3
                
            # برد تیم دوم
            elif self.goals2 > self.goals1:
                self.team2.points += 3
                
            # تساوی؛ هر تیم یک امتیاز دریافت می‌کند    
            else: 
                
                self.team1.points += 1
                self.team2.points += 1    