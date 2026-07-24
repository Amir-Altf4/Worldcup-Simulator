import numpy as np
import random


class Team:
    """نماینده یک تیم فوتبال در شبیه‌ساز جام جهانی.

    این کلاس مشخصات تیم (نام، حمله، دفاع، رتبه) و آمار مسابقات
    (گل زده، گل خورده، امتیاز و گروه) را نگه می‌دارد و منطق
    شبیه‌سازی یک مسابقه را پیاده‌سازی می‌کند.
    """

    def __init__(self, name, attack, defense, rank):
        """یک تیم جدید با مشخصات پایه ایجاد می‌کند.

        Args:
            name (str): نام تیم.
            attack (int): قدرت حمله تیم (۰ تا ۱۰۰).
            defense (int): قدرت دفاع تیم (۰ تا ۱۰۰).
            rank (int): رتبه جهانی تیم برای سیدبندی.
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        # امار اولیه صفر است
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None
        
    def goal_difference(self):
        """تفاضل گل تیم را محاسبه می‌کند.

        Returns:
            int: تفاضل گل.
        """
        return self.goals_for - self.goals_against   
     
    def reset_stats(self):
        """آمار مسابقات تیم را برای شروع مجدد شبیه‌سازی صفر می‌کند."""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
    
    def simulate_match(self, opponent, is_knockout = False):
        """یک مسابقه را در برابر تیم حریف شبیه‌سازی می‌کند.

        در مرحله گروهی فقط ۹۰ دقیقه بازی می‌شود. در مرحله حذفی
        در صورت تساوی، وقت اضافه و در صورت نیاز ضربات پنالتی
        نیز شبیه‌سازی می‌شود.

        Args:
            opponent (Team): تیم حریف.
            is_knockout (bool): اگر True باشد، قوانین مرحله حذفی
                (وقت اضافه و پنالتی) اعمال می‌شود.

        Returns:
            tuple: سه‌تایی شامل (گل تیم، گل حریف، برنده).
                در مرحله گروهی در صورت تساوی، برنده None است.
        """
        
        # شبیه‌سازی نتیجه ۹۰ دقیقه مسابقه
        goals_self, goals_opp = self._play_90_minutes(opponent)
        # در مرحله گروهی مساوی مجاز است
        if not is_knockout: 
            winner = None
            if goals_self > goals_opp:
             winner = self
            elif goals_opp > goals_self:
             winner = opponent
            return goals_self, goals_opp, winner

        # در مرحله حذفی اگر مساوی شد وقت اضافه داریم
        if goals_self == goals_opp:
         et_self, et_opp = self._play_extra_time(opponent)
         goals_self += et_self
         goals_opp += et_opp
        # اگر باز مساوی شد پنالتی
        if goals_self == goals_opp:
            pen_self, pen_opp, winner = self._play_penalties(opponent)
        #گل های پنالتی به تعداد گل اضافه نمی شود
            return goals_self, goals_opp, winner

        winner = self if goals_self > goals_opp else opponent
        return goals_self, goals_opp, winner
    
    def _play_90_minutes(self, opponent):
        """
        ۹۰ دقیقه بازی را با توزیع پواسون شبیه‌سازی می‌کند.
 
        Returns:
            tuple: (گل تیم، گل حریف)
        """
        #میانگین گل مورد انتظار
        # هرچه حمله قوی تر و دفاع حریف ضعیف تر شانس گل بالاتر
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8
        
        # تولید تعداد گل‌ها با استفاده از توزیع پواسون
        goals_self = np.random.poisson(lambda_self)
        goals_opp = np.random.poisson(lambda_opponent)
        return goals_self, goals_opp
    
    def _play_extra_time(self, opponent):
        """
        ۳۰ دقیقه وقت اضافه را شبیه‌سازی می‌کند.
 
        Returns:
            tuple: (گل تیم، گل حریف) در وقت اضافه
        """
        # چون ۳۰ دقیقه است ضربدر ۰.۳۳ می شود
        lambda_self = ((self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8) * 0.33
        lambda_opponent = ((opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8) * 0.33
        # توزیع پواسون بر اساس لاندای تولید شده یک عدد تصادفی می دهد
        goals_self = np.random.poisson(lambda_self)
        goals_opp = np.random.poisson (lambda_opponent)
        
        return goals_self, goals_opp
    
    def _play_penalties(self, opponent):
        """
        ضربات پنالتی را شبیه‌سازی می‌کند.
        ابتدا ۵ ضربه برای هر تیم، سپس پنالتی ناگهانی.
 
        Returns:
            tuple: (گل تیم، گل حریف، برنده)
        """


        def take_penalty(attacker, defender):
            """ یک ضربه پنالتی را شبیه سازی می کند """
            
            # محاسبه احتمال گل بر اساس قدرت حمله و دفاع
            P = 0.75 + (attacker.attack - defender.defense) / 250
            # محدود کردن احتمال گل بین ۶۰ تا ۹۰ درصد
            P = max(0.6, min(0.9, P))
            # تعیین گل شدن یا نشدن ضربه
            return random.random() < P
        
        # شمارش گل‌های تیم اول در پنج ضربه ابتدایی
        score_self = 0
        for _ in range(5):
            if take_penalty(self, opponent):
                score_self += 1
                
        # شمارش گل‌های تیم دوم در پنج ضربه ابتدایی
        score_opponent = 0
        for _ in range(5):
            if take_penalty(opponent, self):
                score_opponent += 1
                
        # اجرای پنالتی ناگهانی تا زمانی که برنده مشخص شود
        while score_self == score_opponent:
            if take_penalty(self, opponent):
                score_self += 1
            if take_penalty(opponent, self):
                score_opponent += 1
            if score_self != score_opponent:
                break
            
        # تعیین برنده ضربات پنالتی
        winner = self if score_self > score_opponent else opponent

        return score_self, score_opponent, winner