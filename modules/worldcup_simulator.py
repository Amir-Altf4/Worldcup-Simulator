import csv
from team import Team
from knockout_stage import KnockoutStage
import random
from group import Group
from match import Match



class WorldCupSimulator:
    """شبیه‌ساز کامل تورنمنت جام جهانی.

    این کلاس بارگذاری تیم‌ها، قرعه‌کشی گروه‌ها، اجرای مرحله گروهی
    و مرحله حذفی، و تحلیل آماری احتمال قهرمانی را هماهنگ می‌کند.
    """

    def __init__(self):
        """یک شبیه‌ساز جدید با وضعیت اولیه خالی ایجاد می‌کند."""
        self.teams = []
        self.groups = []
        # این مراحل ابتدا None هستند بعدا مقدار دهی می شوند.
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        
    def load_teams_from_csv(self, filename):
        """تیم‌ها را از فایل CSV بارگذاری می‌کند.

        Args:
            filename (str): نام فایل CSV.
        """
        # برای اینکه برای هر بار اجرا تیم ها خالی باشند.
        self.teams = []
        try:
            with open(filename) as f:
               reader = csv.DictReader(f)
               for row in reader:
                   new_team = Team((row["name"]), int(row["attack"]), int(row["defense"]), int(row["rank"]))
                   self.teams.append(new_team)
        except FileNotFoundError:
            print("File not found!")
            
          
    def seed_and_draw(self):
        """تیم‌ها را بر اساس رتبه سیدبندی می‌کند و گروه‌ها را قرعه‌کشی می‌کند.
        """
        # ریست می کنیم چون بعدا ۱۰۰۰ بار صدا زده می شود
        self.groups = []
        # مرتب کردن تیم‌ها بر اساس رتبه جهانی
        self.teams.sort(key = lambda t: t.rank)
        # تقسیم به ۴ سید ۸تایی بر اساس رنک
        seed1 = self.teams[0:8]
        seed2 = self.teams[8:16]
        seed3 = self.teams[16:24]
        seed4 = self.teams[24:32]
        
        group_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        # ساختن ۸ گروه خالی    
        for i in range(8):
            group_name = group_names[i]
            self.groups.append(Group(group_name, []))
         # قرعه‌کشی هر سید به صورت جداگانه
        for seed in [seed1, seed2, seed3, seed4]:
         random.shuffle(seed)
         # اختصاص هر تیم به یکی از گروه‌ها
         for i, team in enumerate(seed):
             # ثبت نام گروه برای تیم
             team.group = self.groups[i].name
             # اضافه کردن تیم به گروه مربوط
             self.groups[i].teams.append(team)
         
    def run_group_stage(self):
        """مرحله گروهی را اجرا می‌کند و نتایج را نمایش می‌دهد.
        """
        for group in self.groups:
            group.play_all_matches()
            print(f"=== {group.name} ===")
            ranking = group.get_ranking()
            for i, team in enumerate(ranking):
                print(f"{i+1}. {team.name}: {team.points} points GD {team.goal_difference()} GF {team.goals_for}")
                
    def setup_knockout_bracket(self):
        """مرحله حذفی را می سازد.
        """
        results = {}
        # تعیین تیم اول و دوم هر گروه
        for group in self.groups:
           first, second = group.advance_teams()
           results[group.name] = (first, second)
        # ساختن ۸ مسابقه یک‌هشتم نهایی
        match_r16 = [
        # تیم اول گروه A مقابل تیم دوم گروه B
        Match(results["A"][0], results["B"][1], is_knockout = True),
        # تیم اول گروه C مقابل تیم دوم گروه D
        Match(results["C"][0], results["D"][1], is_knockout = True),
        # تیم اول گروه E مقابل تیم دوم گروه F
        Match(results["E"][0], results["F"][1], is_knockout = True),
        # تیم اول گروه G مقابل تیم دوم گروه H
        Match(results["G"][0], results["H"][1], is_knockout = True),
        # تیم اول گروه B مقابل تیم دوم گروه A
        Match(results["B"][0], results["A"][1], is_knockout = True),
        # تیم اول گروه D مقابل تیم دوم گروه C
        Match(results["D"][0], results["C"][1], is_knockout = True),
        # تیم اول گروه F مقابل تیم دوم گروه E
        Match(results["F"][0], results["E"][1], is_knockout = True),
        # تیم اول گروه H مقابل تیم دوم گروه G
        Match(results["H"][0], results["G"][1], is_knockout = True),
    
           ]
        
        self.round_of_16 = KnockoutStage(match_r16, "round of 16")
    
    def run_knockout_stage(self):
        """مرحله حذفی را اجرا می‌کند."""
    
        self.round_of_16.play_round()
        # دریافت تیم‌های صعودکننده به یک‌چهارم نهایی
        winners_r16 = self.round_of_16.get_winners()
        # ساختن ۴ مسابقه یک‌چهارم نهایی
        match_qf = [
        Match(winners_r16[0], winners_r16[1], is_knockout=True),
        Match(winners_r16[2], winners_r16[3], is_knockout=True),
        Match(winners_r16[4], winners_r16[5], is_knockout=True),
        Match(winners_r16[6], winners_r16[7], is_knockout=True),
     ]
        # ایجاد و اجرای مرحله یک‌چهارم نهایی
        self.quarterfinals = KnockoutStage(match_qf, "Quarterfinals")
        self.quarterfinals.play_round()
        winners_qf = self.quarterfinals.get_winners()
        # ساخت مسابقات مرحله نیمه‌نهایی
        match_sf = [
        Match(winners_qf[0], winners_qf[1], is_knockout=True),
        Match(winners_qf[2], winners_qf[3], is_knockout=True),
     ]
        # ایجاد و اجرای مرحله نیمه‌نهایی
        self.semifinals = KnockoutStage(match_sf, "Semifinals")
        self.semifinals.play_round()
        # دریافت تیم‌های صعودکننده به فینال
        winners_sf = self.semifinals.get_winners()
        # ساختن مسابقه فینال
        match_f = [Match(winners_sf[0], winners_sf[1], is_knockout=True)]
        # ایجاد و اجرای مسابقه فینال
        self.final = KnockoutStage(match_f, "Final")
        self.final.play_round()
    
        self.champion = self.final.get_winners()[0] 
     
    def run_full_simulation(self):
        """مرحله گروهی و حذفی را اجرا می‌کند و نتایج را نمایش می‌دهد.
        """
        # بازنشانی آمار تمام تیم‌ها
        for team in self.teams:
            team.reset_stats()
        # قرعه‌کشی گروه‌ها
        self.seed_and_draw()
        # اجرای مرحله گروهی
        self.run_group_stage()
         # ساخت جدول مرحله حذفی
        self.setup_knockout_bracket()
         # ساخت جدول مرحله حذفی
        self.run_knockout_stage() 
         # قهرمان
        print(f"Champion: {self.champion.name}")
        
    def most_likely_champion(self, num_simulations=1000):
        """مرحله گروهی و حذفی را ۱۰۰۰ بار اجرا می‌کند و نتایج را نمایش می‌دهد.
        """
        # ساختن یک دیکشنری برای ذخیره نام تیم ها و تعداد برنده شدن آنها
        champions = {}
        # اجرای شبیه‌سازی
        for _ in range(num_simulations):
            self.run_full_simulation()
            # افزایش تعداد قهرمانی تیم برنده
            name = self.champion.name
            champions[name] = champions.get(name, 0) + 1
        # نمایش درصد قهرمانی هر تیم
        print(f"\nResults of {num_simulations} simulations:")
        for name, count in sorted(champions.items(), key=lambda x: x[1], reverse=True):
            print(f"{name}: {count/num_simulations*100:.1f}%")
        
    def display_bracket(self):
        """برگرداندن نتایج مرحله حذفی.
        """
        # نمایش نتایج
        print("=== Knockout Bracket ===")
        self.round_of_16.display_results()
        self.quarterfinals.display_results()
        self.semifinals.display_results()
        self.final.display_results()
        print(f"=== Champion : {self.champion.name}")